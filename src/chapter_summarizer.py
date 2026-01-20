"""
Chapter Summarizer for CoverageSummarizer.

Generates structured summaries per chapter with specific details, examples, and citations.

Gate Z5: Pipeline robusto com chunking, extração, Recall Set, auditoria e loop de regeneração.
"""
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
import asyncio
import logging
import re
import sys

logger = logging.getLogger(__name__)


@dataclass
class ChapterSummary:
    """Resumo estruturado de um capítulo."""
    numero: str
    titulo: str
    palavras: int              # Palavras do texto original
    palavras_resumo: int         # Palavras do resumo gerado
    paginas: List[int]
    resumo: str              # 300-500 palavras com detalhes específicos
    pontos_chave: List[str]  # 5-8 pontos principais
    citacoes: List[str]      # Citações marcantes do autor
    exemplos: List[str]      # Exemplos concretos mencionados


@dataclass
class StructuredSummary:
    """Resumo completo estruturado por capítulos."""
    resumo_executivo: Dict[str, str]  # {'curto': ..., 'medio': ...}
    estrutura_detectada: Dict[str, any]
    capitulos: List[ChapterSummary]
    bullets_gerais: List[str]
    total_palavras: int
    total_capitulos: int


class ChapterSummarizer:
    """
    Processa resumos estruturados por capítulo.

    Gera resumos detalhados e específicos para cada capítulo individualmente,
    depois combina em um resumo executivo do livro completo.
    """

    def __init__(self, metadata_collector=None):
        """
        Inicializa o ChapterSummarizer.
        
        Args:
            metadata_collector: Coletor de metadados do processo (opcional)
        """
        # Import here to avoid circular import
        from summarizer import AsyncOpenAIClient
        self.client = AsyncOpenAIClient()
        self.metadata_collector = metadata_collector

    async def summarize_chapter(
        self,
        chapter: 'Chapter',
        full_text: str
    ) -> ChapterSummary:
        """
        Cria resumo detalhado de um capítulo específico.

        Args:
            chapter: Objeto Chapter com metadados
            full_text: Texto completo do livro (para extrair o trecho)

        Returns:
            ChapterSummary com resumo estruturado e específico
        """
        chapter_text = full_text[chapter.start_pos:chapter.end_pos]

        logger.info(f"Resumindo Capítulo {chapter.number}: {chapter.title} ({chapter.word_count} palavras)")

        # Prompt otimizado para capítulo - DEMANDA ESPECIFICIDADE
        prompt = f"""Você está resumindo o Capítulo {chapter.number}: "{chapter.title}"

Texto do capítulo ({chapter.word_count} palavras):
{chapter_text}

Crie um resumo estruturado com:

1. **RESUMO** (300-500 palavras):
   - Argumento central do capítulo
   - Exemplos ESPECÍFICOS mencionados (nomes próprios, casos, estudos)
   - Dados ou estatísticas citados
   - Citações marcantes do autor
   - NÃO use frases genéricas como "o capítulo discute..." ou "o autor fala sobre..."
   - Seja CONCRETO: cite nomes, números, casos reais mencionados no texto

2. **PONTOS-CHAVE** (5-8 pontos):
   - Ideias principais em forma de lista
   - Seja ESPECÍFICO (não genérico)
   - Inclua detalhes mencionados no capítulo

3. **CITAÇÕES** (2-4 citações):
   - Frases marcantes do autor copiadas EXATAMENTE do texto
   - Entre aspas
   - Escolha citações que resumem ideias centrais

4. **EXEMPLOS** (2-5 exemplos):
   - Casos, pacientes, estudos, pessoas mencionadas
   - Nomes próprios e detalhes específicos
   - Experimentos ou pesquisas citadas

**IMPORTANTE**: Seja ESPECÍFICO. Cite nomes, números, casos concretos que aparecem no texto.
Evite abstrações. Se o autor menciona "Dr. Smith" ou "estudo de 2019", CITE isso.

Formato de resposta:
RESUMO:
[seu resumo aqui]

PONTOS-CHAVE:
• [ponto 1]
• [ponto 2]
...

CITAÇÕES:
"[citação 1]"
"[citação 2]"

EXEMPLOS:
• [exemplo 1]
• [exemplo 2]
"""

        # Import here to avoid circular import
        from summarizer import SummarySpecs

        response = await self.client.complete(
            system_message=SummarySpecs.BASE_SYSTEM_MESSAGE,
            user_message=prompt,
            max_output_tokens=1500,
            temperature=0.4
        )

        # Parse response estruturada
        parsed = self._parse_structured_response(response)

        # Calcular palavras do resumo
        palavras_resumo = len(parsed['resumo'].split())
        
        logger.debug(f"  ✓ Cap {chapter.number}: {len(parsed['resumo'])} chars, "
                    f"{len(parsed['pontos_chave'])} pontos, "
                    f"{len(parsed['citacoes'])} citações, "
                    f"{palavras_resumo} palavras no resumo")

        return ChapterSummary(
            numero=chapter.number,
            titulo=chapter.title,
            palavras=chapter.word_count,
            palavras_resumo=palavras_resumo,
            paginas=chapter.page_markers,
            resumo=parsed['resumo'],
            pontos_chave=parsed['pontos_chave'],
            citacoes=parsed['citacoes'],
            exemplos=parsed['exemplos']
        )

    async def summarize_all_chapters(
        self,
        chapters: List['Chapter'],
        full_text: str
    ) -> StructuredSummary:
        """
        Processa TODOS os capítulos EM PARALELO.

        Args:
            chapters: Lista de capítulos detectados
            full_text: Texto completo do livro

        Returns:
            StructuredSummary com resumo executivo + resumos por capítulo
        """
        logger.info(f"🚀 Iniciando resumo paralelo de {len(chapters)} capítulos")

        # 1. Resumir todos os capítulos em paralelo
        chapter_summaries = await asyncio.gather(*[
            self.summarize_chapter(ch, full_text)
            for ch in chapters
        ])

        logger.info(f"✅ Todos os {len(chapter_summaries)} capítulos resumidos!")

        # 2. Gerar resumo executivo baseado nos capítulos
        logger.info("Gerando resumo executivo do livro completo...")

        combined_summaries = "\n\n".join([
            f"Capítulo {cs.numero} - {cs.titulo}:\n{cs.resumo[:300]}..."
            for cs in chapter_summaries
        ])

        executive_curto = await self._generate_executive(
            combined_summaries, target_words=200, chapter_summaries=chapter_summaries
        )
        executive_medio = await self._generate_executive(
            combined_summaries, target_words=500, chapter_summaries=chapter_summaries
        )

        # 3. Extrair bullets gerais (top pontos de cada capítulo)
        all_points = []
        for cs in chapter_summaries:
            # Pegar os 2 primeiros pontos de cada capítulo
            all_points.extend(cs.pontos_chave[:2])

        logger.info("✅ Resumo executivo gerado!")

        return StructuredSummary(
            resumo_executivo={
                'curto': executive_curto,
                'medio': executive_medio
            },
            estrutura_detectada={
                'total_capitulos': len(chapters),
                'metodo': chapters[0].pattern_matched if chapters else None,
                'confianca_media': sum(ch.confidence for ch in chapters) / len(chapters)
            },
            capitulos=chapter_summaries,
            bullets_gerais=all_points[:15],  # Top 15 pontos
            total_palavras=sum(cs.palavras for cs in chapter_summaries),
            total_capitulos=len(chapter_summaries)
        )

    async def _generate_executive(
        self,
        combined: str,
        target_words: int,
        chapter_summaries: List[ChapterSummary]
    ) -> str:
        """
        Gera resumo executivo do livro todo baseado nos capítulos.

        Args:
            combined: Resumos de todos os capítulos concatenados
            target_words: Tamanho alvo do resumo (200 ou 500 palavras)
            chapter_summaries: Lista de resumos de capítulos

        Returns:
            Resumo executivo do livro completo
        """
        # Extrair alguns exemplos concretos dos capítulos
        exemplos_destaque = []
        for cs in chapter_summaries[:5]:  # Primeiros 5 capítulos
            if cs.exemplos:
                exemplos_destaque.append(cs.exemplos[0])

        exemplos_text = "\n".join(f"- {ex}" for ex in exemplos_destaque[:3])

        prompt = f"""Baseado nos resumos de todos os capítulos abaixo, crie um resumo executivo de aproximadamente {target_words} palavras do livro completo.

Resumos dos capítulos:
{combined}

Alguns exemplos concretos mencionados no livro:
{exemplos_text}

**IMPORTANTE**:
- Seja ESPECÍFICO, não genérico
- Mencione exemplos concretos do livro
- Não use frases vagas como "o livro explora..." ou "discute questões..."
- Se o livro menciona casos, estudos, pessoas - CITE-OS
- Foque no argumento central e evidências apresentadas

Resumo executivo (~{target_words} palavras):"""

        # Import here to avoid circular import
        from summarizer import SummarySpecs

        response = await self.client.complete(
            system_message=SummarySpecs.BASE_SYSTEM_MESSAGE,
            user_message=prompt,
            max_output_tokens=target_words * 3,
            temperature=0.4
        )

        return response.strip()

    def _parse_structured_response(self, response: str) -> Dict:
        """
        Parse resposta estruturada em seções.

        Args:
            response: Resposta do LLM com seções marcadas

        Returns:
            Dict com 'resumo', 'pontos_chave', 'citacoes', 'exemplos'
        """
        sections = {
            'resumo': '',
            'pontos_chave': [],
            'citacoes': [],
            'exemplos': []
        }

        # Lógica de parsing por seções
        current_section = None
        resumo_lines = []

        for line in response.split('\n'):
            line_upper = line.upper().strip()

            # Detectar mudança de seção
            if 'RESUMO:' in line_upper:
                current_section = 'resumo'
                continue
            elif 'PONTOS-CHAVE:' in line_upper or 'PONTOS CHAVE:' in line_upper:
                current_section = 'pontos_chave'
                continue
            elif 'CITAÇÕES:' in line_upper or 'CITACOES:' in line_upper or 'QUOTES:' in line_upper:
                current_section = 'citacoes'
                continue
            elif 'EXEMPLOS:' in line_upper or 'EXAMPLES:' in line_upper:
                current_section = 'exemplos'
                continue

            # Processar conteúdo da seção
            if not current_section:
                continue

            cleaned = line.strip()
            if not cleaned:
                continue

            if current_section == 'resumo':
                resumo_lines.append(line)
            elif cleaned.startswith('•') or cleaned.startswith('-'):
                # Item de lista
                item = cleaned[1:].strip()
                if item:
                    sections[current_section].append(item)
            elif cleaned.startswith('"') and cleaned.endswith('"'):
                # Citação com aspas
                sections['citacoes'].append(cleaned.strip('"'))
            elif current_section == 'citacoes' and ('"' in cleaned or '"' in cleaned):
                # Citação com aspas tipográficas
                quote = cleaned.strip('"').strip('"').strip('"')
                if quote:
                    sections['citacoes'].append(quote)
            elif current_section in ['pontos_chave', 'exemplos']:
                # Item sem marcador
                sections[current_section].append(cleaned)

        # Juntar resumo
        sections['resumo'] = '\n'.join(resumo_lines).strip()

        # Validação mínima
        if not sections['resumo']:
            logger.warning("Resumo vazio após parsing - usando resposta completa")
            sections['resumo'] = response

        if not sections['pontos_chave']:
            logger.warning("Nenhum ponto-chave extraído")

        return sections

    # ============ Gate Z5: Pipeline Robusto ============

    def _chunk_chapter(self, chapter_text: str, chapter_number: str, chunk_word_target: int = 1000, overlap_words: int = 100) -> List[Dict]:
        """
        Divide capítulo em chunks numerados.
        
        Gate Z5: Cada chunk recebe chunk_id único.
        
        Args:
            chapter_text: Texto do capítulo
            chapter_number: Número do capítulo
            chunk_word_target: Tamanho alvo de chunks em palavras
            overlap_words: Overlap entre chunks em palavras
            
        Returns:
            Lista de dicionários com chunks:
            [
                {
                    'chunk_id': 'cap_1_chunk_0',
                    'text': '...',
                    'words': 1000
                },
                ...
            ]
        """
        words = chapter_text.split()
        chunks = []
        chunk_idx = 0
        i = 0
        
        while i < len(words):
            chunk_words = words[i:i + chunk_word_target]
            chunk_text = ' '.join(chunk_words)
            chunk_id = f"cap_{chapter_number}_chunk_{chunk_idx}"
            
            chunks.append({
                'chunk_id': chunk_id,
                'text': chunk_text,
                'words': len(chunk_words),
                'start_word': i,
                'end_word': i + len(chunk_words)
            })
            
            chunk_idx += 1
            # Avançar com overlap
            i += chunk_word_target - overlap_words
            
        return chunks

    async def _extract_from_chunks(self, chunks: List[Dict]) -> List[Dict]:
        """
        Extrai ideias, conceitos, afirmações e exemplos de cada chunk.
        
        Gate Z5: Extração primária por chunk (pode mockar LLM nos testes).
        
        Args:
            chunks: Lista de chunks retornada por _chunk_chapter()
            
        Returns:
            Lista de extrações:
            [
                {
                    'chunk_id': 1,
                    'concepts': ['conceito1', 'conceito2'],
                    'ideas': ['ideia1'],
                    'is_heading': False
                },
                ...
            ]
        """
        extractions = []
        
        for chunk in chunks:
            chunk_id_num = int(chunk['chunk_id'].split('_')[-1])
            chunk_text = chunk['text']
            is_heading = chunk_text.strip().startswith('#') or len(chunk_text.strip().split('\n')) < 3
            
            # Prompt para extração
            prompt = f"""Extraia do seguinte texto:
- Conceitos principais (nomes, termos técnicos, definições)
- Ideias centrais (afirmações do autor)
- Exemplos mencionados

Texto:
{chunk_text[:2000]}

Formato JSON:
{{
    "concepts": ["conceito1", "conceito2"],
    "ideas": ["ideia1", "ideia2"],
    "examples": ["exemplo1"]
}}"""

            try:
                from summarizer import SummarySpecs
                response = await self.client.complete(
                    system_message="Você é um extrator de informações estruturadas. Retorne apenas JSON válido.",
                    user_message=prompt,
                    max_output_tokens=500,
                    temperature=0.2
                )
                
                # Parse JSON (simplificado - em produção usar json.loads com tratamento de erro)
                import json
                try:
                    extracted = json.loads(response)
                except:
                    # Fallback: extrair conceitos simples
                    extracted = {
                        'concepts': [w for w in chunk_text.split() if len(w) > 5 and w[0].isupper()][:5],
                        'ideas': [],
                        'examples': []
                    }
                
                extractions.append({
                    'chunk_id': chunk_id_num,
                    'concepts': extracted.get('concepts', []),
                    'ideas': extracted.get('ideas', []),
                    'examples': extracted.get('examples', []),
                    'is_heading': is_heading
                })
            except Exception as e:
                logger.warning(f"Erro na extração do chunk {chunk_id_num}: {e}")
                extractions.append({
                    'chunk_id': chunk_id_num,
                    'concepts': [],
                    'ideas': [],
                    'examples': [],
                    'is_heading': is_heading
                })
        
        return extractions

    async def _generate_summary_with_markers(
        self,
        chapter: 'Chapter',
        recall_set: 'RecallSet',
        full_text: str
    ) -> str:
        """
        Gera resumo incluindo marcadores [[RS:capX:hash|chunks:N,M]].
        
        Gate Z5: Prompt deve exigir marcadores explícitos.
        
        Args:
            chapter: Objeto Chapter
            recall_set: RecallSet do capítulo
            full_text: Texto completo do livro
            
        Returns:
            Texto do resumo com marcadores
        """
        chapter_text = full_text[chapter.start_pos:chapter.end_pos]
        
        # Construir lista de itens críticos para o prompt
        critical_items_list = []
        for item in recall_set.critical_items:
            chunks_str = ','.join(map(str, item.source_chunks))
            critical_items_list.append(
                f"- {item.content} [[RS:cap{chapter.number}:{item.item_id.split(':')[-1]}|chunks:{chunks_str}]]"
            )
        
        critical_items_text = '\n'.join(critical_items_list)
        
        prompt = f"""Você está resumindo o Capítulo {chapter.number}: "{chapter.title}"

Texto do capítulo ({chapter.word_count} palavras):
{chapter_text[:5000]}

**CRÍTICO E OBRIGATÓRIO**: Você DEVE incluir TODOS os {len(recall_set.critical_items)} itens críticos abaixo no resumo, cada um COM seu marcador EXATO:

{critical_items_text}

**REGRAS ABSOLUTAS**:
1. TODOS os {len(recall_set.critical_items)} itens críticos acima DEVEM aparecer no resumo
2. Cada item DEVE ter seu marcador EXATO no formato: [[RS:cap{chapter.number}:hash|chunks:N,M]]
3. Nenhum item crítico pode ser omitido
4. Os marcadores são obrigatórios e devem estar no formato exato mostrado acima
5. Gere um resumo de 300-500 palavras que incorpore naturalmente TODOS esses marcadores

**VERIFICAÇÃO**: Antes de finalizar, confirme que TODOS os {len(recall_set.critical_items)} marcadores estão presentes no resumo.

RESUMO:"""

        from summarizer import SummarySpecs
        
        response = await self.client.complete(
            system_message=SummarySpecs.BASE_SYSTEM_MESSAGE,
            user_message=prompt,
            max_output_tokens=2000,  # Aumentar para dar mais espaço aos marcadores
            temperature=0.3  # Reduzir temperatura para ser mais determinístico
        )
        
        return response.strip()

    def _build_addendum_items_list(
        self,
        chapter: 'Chapter',
        missing_items: List['RecallSetItem']
    ) -> str:
        """
        Constrói lista formatada de itens faltantes para o prompt do addendum.
        
        Clean Code: Função pequena e focada, extraída para melhorar legibilidade.
        
        Args:
            chapter: Objeto Chapter
            missing_items: Lista de RecallSetItem que faltam marcadores
            
        Returns:
            String formatada com lista de itens
        """
        items_list = []
        for item in missing_items:
            chunks_str = ','.join(map(str, item.source_chunks))
            item_hash = item.item_id.split(':')[-1]
            items_list.append(
                f"- {item.content} [[RS:cap{chapter.number}:{item_hash}|chunks:{chunks_str}]]"
            )
        return '\n'.join(items_list)

    def _build_addendum_prompt(
        self,
        missing_items: List['RecallSetItem'],
        items_text: str,
        attempt_number: int = 1
    ) -> str:
        """
        Constrói prompt melhorado para geração de addendum.
        
        Clean Code: Função pequena e focada, separa construção de prompt.
        Melhora: Prompt mais específico e direto, com exemplos explícitos.
        
        Args:
            missing_items: Lista de itens faltantes
            items_text: Texto formatado com lista de itens
            attempt_number: Número da tentativa (para estratégias diferentes)
            
        Returns:
            String do prompt formatado
        """
        if attempt_number == 1:
            # Estratégia 1: Prompt direto e específico
            prompt = f"""Você DEVE gerar EXATAMENTE {len(missing_items)} bullets abaixo.
Cada bullet DEVE conter o marcador EXATO mostrado.

**FORMATO OBRIGATÓRIO** (copie exatamente):
{items_text}

**REGRAS CRÍTICAS**:
1. Gere EXATAMENTE {len(missing_items)} bullets (um por item acima)
2. Cada bullet DEVE ter o marcador EXATO: [[RS:cap...|chunks:...]]
3. Cada bullet DEVE começar com "- " (hífen e espaço)
4. NÃO altere os marcadores, apenas copie-os exatamente como mostrado
5. Adicione uma frase curta (10-20 palavras) sobre o item ANTES do marcador

**EXEMPLO CORRETO**:
- A dopamina é importante. [[RS:cap2:09d6f1|chunks:1,2]]

BULLETS (um por linha):"""
        else:
            # Estratégia 2 (fallback): Ainda mais simples e direto
            prompt = f"""COPIE EXATAMENTE os {len(missing_items)} bullets abaixo, incluindo os marcadores EXATOS:

{items_text}

**INSTRUÇÃO SIMPLES**: Copie cada linha acima, adicione uma frase curta antes do marcador, e retorne.

BULLETS:"""
        
        return prompt

    async def _generate_missing_markers_addendum(
        self,
        chapter: 'Chapter',
        missing_items: List['RecallSetItem'],
        full_text: str,
        attempt_number: int = 1
    ) -> str:
        """
        Gera addendum com marcadores apenas para itens faltantes.
        
        Estratégia A (melhorada): Prompt mais específico e direto, com fallback.
        Gate Z10: Clean Code - função pequena, responsabilidade única.
        
        Args:
            chapter: Objeto Chapter
            missing_items: Lista de RecallSetItem que faltam marcadores
            full_text: Texto completo do livro (não usado, mas mantido para compatibilidade)
            attempt_number: Número da tentativa (1 = normal, 2+ = fallback)
            
        Returns:
            Texto do addendum com bullets e marcadores
        """
        if not missing_items:
            return ""
        
        # Construir lista de itens faltantes
        items_text = self._build_addendum_items_list(chapter, missing_items)
        
        # Construir prompt melhorado
        prompt = self._build_addendum_prompt(missing_items, items_text, attempt_number)
        
        # System message mais específico
        system_message = (
            "Você é um gerador de bullets concisos. "
            "Sua única tarefa é retornar bullets com marcadores EXATOS no formato solicitado. "
            "NÃO adicione texto explicativo, apenas os bullets."
        )
        
        logger.info(
            f"Gerando addendum (tentativa {attempt_number}) para capítulo {chapter.number} "
            f"com {len(missing_items)} itens faltantes: {[item.item_id for item in missing_items]}"
        )
        
        from summarizer import SummarySpecs
        response = await self.client.complete(
            system_message=system_message,
            user_message=prompt,
            max_output_tokens=500,
            temperature=0.1 if attempt_number == 1 else 0.0  # Mais determinístico no fallback
        )
        
        addendum_text = response.strip()
        
        # Log detalhado para debug
        logger.debug(
            f"Addendum gerado (tentativa {attempt_number}) para capítulo {chapter.number}:\n"
            f"{addendum_text[:200]}..."  # Primeiros 200 chars para não poluir logs
        )
        
        return addendum_text

    def _validate_addendum_contains_markers(
        self,
        addendum_text: str,
        missing_item_ids: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Valida se o addendum gerado contém os marcadores esperados.
        
        Clean Code: Função pequena e focada, validação separada.
        Gate Z10: Teste antes de usar (validação explícita).
        
        Args:
            addendum_text: Texto do addendum gerado
            missing_item_ids: Lista de item_ids que devem estar no addendum
            
        Returns:
            Tupla (is_valid, missing_in_addendum)
        """
        import re
        marker_pattern = r'\[\[RS:cap\d+:([a-f0-9]{6})\|chunks:[^\]]+\]\]'
        found_hashes = set(re.findall(marker_pattern, addendum_text))
        
        expected_hashes = {item_id.split(':')[-1] for item_id in missing_item_ids}
        missing_in_addendum = expected_hashes - found_hashes
        
        is_valid = len(missing_in_addendum) == 0
        
        if not is_valid:
            logger.warning(
                f"Addendum não contém todos os marcadores esperados. "
                f"Faltando: {list(missing_in_addendum)} (esperado: {list(expected_hashes)})"
            )
        
        return is_valid, list(missing_in_addendum)

    async def _audit_and_regenerate(
        self,
        chapter: 'Chapter',
        recall_set: 'RecallSet',
        full_text: str,
        max_attempts: int = 3,
        max_addendums: int = 2
    ) -> Tuple[str, int, int]:
        """
        Loop de regeneração com auditoria + addendum incremental.
        
        Estratégia A (Gate Z8):
        1. Tenta gerar resumo completo (até max_attempts)
        2. Se ainda faltam marcadores, gera addendum apenas para faltantes
        3. Anexa addendum e re-audita
        4. Repete addendum até max_addendums se necessário
        
        Args:
            chapter: Objeto Chapter
            recall_set: RecallSet do capítulo
            full_text: Texto completo do livro
            max_attempts: Máximo de tentativas de resumo completo (padrão: 3)
            max_addendums: Máximo de tentativas de addendum (padrão: 2)
            
        Returns:
            Tupla (summary_text, regeneration_count, addendum_count)
            
        Raises:
            CoverageError: Se falhar após max_attempts + max_addendums
        """
        from src.recall_auditor import RecallAuditor
        from src.exceptions import CoverageError
        
        auditor = RecallAuditor()
        recall_set_dict = {
            'critical_items': [
                {
                    'item_id': item.item_id,
                    'source_chunks': item.source_chunks
                }
                for item in recall_set.critical_items
            ]
        }
        
        regeneration_count = 0
        addendum_count = 0
        summary_text = ""
        audit_result = None
        
        # Fase 1: Tentar gerar resumo completo
        for attempt in range(1, max_attempts + 1):
            logger.info(f"Tentativa {attempt}/{max_attempts} de gerar resumo para capítulo {chapter.number}")
            
            summary_text = await self._generate_summary_with_markers(chapter, recall_set, full_text)
            audit_result = auditor.audit_summary(summary_text, recall_set_dict, chapter.number)
            
            if audit_result.passed:
                logger.info(f"✓ Resumo do capítulo {chapter.number} aprovado na tentativa {attempt}")
                return (summary_text, regeneration_count, addendum_count)
            
            logger.warning(f"✗ Resumo do capítulo {chapter.number} falhou na tentativa {attempt}: {len(audit_result.missing_markers)} marcadores faltando")
            regeneration_count = attempt
        
        # Fase 2: Se ainda faltam marcadores, gerar addendum incremental
        if audit_result and audit_result.missing_markers:
            initial_missing_count = len(audit_result.missing_markers)
            logger.info(
                f"Gerando addendum para capítulo {chapter.number} com {initial_missing_count} itens faltantes: "
                f"{audit_result.missing_markers}"
            )
            
            # Mapear missing_markers para RecallSetItem
            missing_items = [
                item for item in recall_set.critical_items
                if item.item_id in audit_result.missing_markers
            ]
            
            for addendum_attempt in range(1, max_addendums + 1):
                addendum_count = addendum_attempt  # Rastrear quantos addendums foram usados
                
                logger.info(
                    f"Tentativa {addendum_attempt}/{max_addendums} de addendum para capítulo {chapter.number}. "
                    f"Itens faltantes: {[item.item_id for item in missing_items]}"
                )
                
                addendum = await self._generate_missing_markers_addendum(
                    chapter, missing_items, full_text, attempt_number=addendum_attempt
                )
                
                # Validação prévia: verificar se addendum contém marcadores esperados
                is_valid, missing_in_addendum = self._validate_addendum_contains_markers(
                    addendum, [item.item_id for item in missing_items]
                )
                
                # Determinar estratégia e temperatura baseado no número da tentativa
                prompt_strategy = "direct" if addendum_attempt == 1 else "fallback"
                temperature = 0.1 if addendum_attempt == 1 else 0.0
                
                if not is_valid and addendum_attempt < max_addendums:
                    logger.warning(
                        f"Addendum {addendum_attempt} não contém todos os marcadores esperados. "
                        f"Faltando no addendum: {missing_in_addendum}. Tentando novamente..."
                    )
                
                # Coletar dados do addendum (antes de anexar)
                if self.metadata_collector:
                    self.metadata_collector.log_addendum_attempt(
                        chapter_number=chapter.number,
                        attempt_number=addendum_attempt,
                        missing_item_ids=[item.item_id for item in missing_items],
                        addendum_content=addendum,
                        prompt_strategy=prompt_strategy,
                        temperature=temperature,
                        validation_passed=is_valid,
                        validation_missing=missing_in_addendum,
                        result="pending"  # Será atualizado após auditoria
                    )
                
                # Anexar addendum ao resumo
                summary_with_addendum = f"""{summary_text}

## Cobertura (itens críticos)

{addendum}"""
                
                # Re-auditar
                audit_result = auditor.audit_summary(
                    summary_with_addendum, recall_set_dict, chapter.number
                )
                
                if audit_result.passed:
                    logger.info(
                        f"✓ Addendum {addendum_attempt} fechou cobertura 100% para capítulo {chapter.number}"
                    )
                    # Atualizar resultado do addendum no coletor
                    if self.metadata_collector:
                        chapter_data = self.metadata_collector.get_chapter_data(chapter.number)
                        if chapter_data.addendum_attempts:
                            chapter_data.addendum_attempts[-1].result = "passed"
                        self.metadata_collector.finalize_chapter(
                            chapter.number, regeneration_count, addendum_count, []
                        )
                    return (summary_with_addendum, regeneration_count, addendum_count)
                
                # Se ainda faltam, atualizar missing_items para próxima tentativa
                if audit_result.missing_markers:
                    missing_items = [
                        item for item in recall_set.critical_items
                        if item.item_id in audit_result.missing_markers
                    ]
                    logger.warning(
                        f"✗ Addendum {addendum_attempt} para capítulo {chapter.number} ainda faltam "
                        f"{len(missing_items)} marcadores: {audit_result.missing_markers}"
                    )
                else:
                    # Se não há mais missing_markers mas audit não passou, pode ser outro problema
                    logger.warning(
                        f"✗ Addendum {addendum_attempt} para capítulo {chapter.number} não passou auditoria, "
                        f"mas não há missing_markers. Erros: {audit_result.errors}"
                    )
        
        # Falhou após todas as tentativas
        final_missing = audit_result.missing_markers if audit_result else []
        if self.metadata_collector:
            self.metadata_collector.finalize_chapter(
                chapter.number, regeneration_count, addendum_count, final_missing
            )
            # Atualizar resultado final dos addendums que falharam
            chapter_data = self.metadata_collector.get_chapter_data(chapter.number)
            if chapter_data.addendum_attempts:
                for attempt in chapter_data.addendum_attempts:
                    if attempt.result == "pending":
                        attempt.result = "failed"
        
        if audit_result:
            raise CoverageError(
                f"Capítulo {chapter.number}: Cobertura não atingiu 100% após {max_attempts} tentativas de resumo "
                f"e {max_addendums} tentativas de addendum. Erros: {audit_result.errors}"
            )
        else:
            raise CoverageError(
                f"Capítulo {chapter.number}: Cobertura não atingiu 100% após {max_attempts} tentativas."
            )

    async def summarize_chapter_robust(
        self,
        chapter: 'Chapter',
        full_text: str,
        use_robust_pipeline: bool = True
    ) -> ChapterSummary:
        """
        Pipeline robusto completo: chunking → extração → recall set → resumo → auditoria → regeneração.
        
        Gate Z5: Implementação completa do pipeline robusto.
        
        Args:
            chapter: Objeto Chapter
            full_text: Texto completo do livro
            use_robust_pipeline: Se True, usa pipeline robusto (padrão: True)
            
        Returns:
            ChapterSummary com resumo estruturado
            
        Raises:
            CoverageError: Se cobertura não atingir 100% após max tentativas
        """
        if not use_robust_pipeline:
            # Fallback para método antigo
            return await self.summarize_chapter(chapter, full_text)
        
        chapter_text = full_text[chapter.start_pos:chapter.end_pos]
        logger.info(f"Resumindo Capítulo {chapter.number} com pipeline robusto ({chapter.word_count} palavras)")
        
        # 1. Chunking
        chunks = self._chunk_chapter(chapter_text, chapter.number)
        logger.debug(f"  → {len(chunks)} chunks criados")
        
        # 2. Extração
        chunk_extractions = await self._extract_from_chunks(chunks)
        logger.debug(f"  → {len(chunk_extractions)} extrações concluídas")
        
        # 3. Gerar Recall Set
        from src.recall_set import generate_recall_set
        recall_set = generate_recall_set(chunk_extractions, chapter.number)
        logger.debug(f"  → Recall Set: {len(recall_set.critical_items)} críticos, {len(recall_set.supporting_items)} suporte")
        
        # 4. Gerar resumo com marcadores + Auditoria + Regeneração
        summary_text, regeneration_count, addendum_count = await self._audit_and_regenerate(
            chapter, recall_set, full_text, max_attempts=3
        )
        
        if regeneration_count > 0:
            logger.info(f"  → Regenerações: {regeneration_count}")
        
        # 5. Parsear resumo (reutilizar método existente)
        parsed = self._parse_structured_response(summary_text)
        
        palavras_resumo = len(parsed['resumo'].split())
        
        return ChapterSummary(
            numero=chapter.number,
            titulo=chapter.title,
            palavras=chapter.word_count,
            palavras_resumo=palavras_resumo,
            paginas=chapter.page_markers,
            resumo=parsed['resumo'],
            pontos_chave=parsed['pontos_chave'],
            citacoes=parsed['citacoes'],
            exemplos=parsed['exemplos']
        )
