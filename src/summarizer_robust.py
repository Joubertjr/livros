"""
Gate Z7 - Summarizer Robusto (integração final).

Orquestra pipeline completo:
- Pipeline robusto por capítulo
- Geração de evidências
- Quality Gate (lendo só coverage_report.json)
- Se FAIL → levanta exceção clara
- Se PASS → retorna resultado final

F4: Persistência progressiva e retomada segura
- Carrega checkpoints conforme F3
- Pula capítulos já processados
- Cria checkpoints nos pontos definidos em F2
"""

import asyncio
import logging
from typing import Dict, List, Optional
from pathlib import Path
from datetime import datetime

from src.chapter_detector import ChapterDetector, Chapter
from src.markdown_parser import MarkdownParser
from src.chapter_summarizer import ChapterSummarizer, ChapterSummary
from src.evidence_generator_robust import EvidenceGeneratorRobust
from src.quality_gate import QualityGate
from src.exceptions import CoverageError
from src.storage.checkpoint_manager import CheckpointManager
# Importar generate_recall_set no nível do módulo para permitir mock
from src.recall_set import generate_recall_set as _generate_recall_set

logger = logging.getLogger(__name__)


class BookSummarizerRobust:
    """
    Summarizer robusto que orquestra pipeline completo (Gate Z7).
    
    Pipeline:
    1. Detectar capítulos
    2. Processar cada capítulo com pipeline robusto
    3. Coletar extrações
    4. Gerar evidências (coverage_report.json, extractions, report.md)
    5. Validar com Quality Gate
    6. Se falhar → levantar CoverageError
    7. Se passar → retornar resultado
    """
    
    def __init__(
        self,
        evidencias_dir: str = "EVIDENCIAS",
        use_chapters: bool = True,
        metadata_collector=None,
        session_id: Optional[str] = None
    ):
        """
        Inicializa o summarizer robusto.
        
        Args:
            evidencias_dir: Diretório para salvar evidências
            use_chapters: Se True, detecta capítulos antes de processar
            metadata_collector: Coletor de metadados do processo (opcional)
            session_id: ID da sessão para retomada (opcional)
        """
        self.evidencias_dir = Path(evidencias_dir)
        self.evidencias_dir.mkdir(parents=True, exist_ok=True)
        self.use_chapters = use_chapters
        self.metadata_collector = metadata_collector
        self.session_id = session_id
        
        # Inicializar componentes
        self.markdown_parser = MarkdownParser()
        self.chapter_detector = ChapterDetector()
        self.chapter_summarizer = ChapterSummarizer(metadata_collector=metadata_collector)
        self.evidence_generator = EvidenceGeneratorRobust(output_dir=str(self.evidencias_dir))
        self.quality_gate = QualityGate()
        
        # F4: Inicializar gerenciador de checkpoints
        self.checkpoint_manager = CheckpointManager()
        
        # F4: Metadados de processamento (inicializados na primeira execução)
        self.process_metadata = None
    
    async def summarize_robust(self, text: str) -> Dict:
        """
        Pipeline robusto completo (Gate Z7) com persistência progressiva (F4).
        
        Args:
            text: Texto completo do livro
            
        Returns:
            Dicionário com resumos dos capítulos e resumo executivo
            
        Raises:
            CoverageError: Se quality gate falhar (coverage < 100%)
        """
        logger.info("🚀 Iniciando pipeline robusto (Gate Z7) com persistência progressiva (F4)")
        
        # F4: Gerar session_id se não fornecido
        if not self.session_id:
            import uuid
            self.session_id = str(uuid.uuid4())
            logger.info(f"  → Session ID gerado: {self.session_id}")
        else:
            logger.info(f"  → Session ID fornecido: {self.session_id}")
        
        # F4: Carregar checkpoints válidos conforme F3
        last_checkpoint = self.checkpoint_manager.find_last_valid_checkpoint(self.session_id)
        processed_chapters = []
        if last_checkpoint:
            logger.info(f"  ✅ Checkpoint válido encontrado: capítulo {last_checkpoint.chapter_number}")
            processed_chapters = last_checkpoint.metadata.get('capitulos_processados', [])
            logger.info(f"  → Capítulos já processados: {processed_chapters}")
            # Restaurar metadados de processamento
            self.process_metadata = last_checkpoint.metadata.copy()
        else:
            logger.info(f"  ℹ️ Nenhum checkpoint válido encontrado, iniciando do zero")
            # Inicializar metadados de processamento
            self.process_metadata = {
                'session_id': self.session_id,
                'timestamp_inicio': datetime.now().isoformat(),
                'capitulos_processados': [],
                'chunks_processados_por_capitulo': {},
                'total_chunks_por_capitulo': {}
            }
        
        # 1. Detectar capítulos
        chapters = await self._detect_chapters(text)
        logger.info(f"  → {len(chapters)} capítulos detectados")
        
        # 2. Processar cada capítulo com pipeline robusto
        chapter_summaries = []
        all_extractions = {}
        
        for chapter in chapters:
            # F4: Pular capítulos já processados conforme F3
            if chapter.number in processed_chapters:
                logger.info(f"  ⏭️ Capítulo {chapter.number} já processado, restaurando do checkpoint...")
                # Carregar checkpoint do capítulo
                checkpoint = self.checkpoint_manager.load_checkpoint(self.session_id, chapter.number)
                if checkpoint:
                    # Restaurar dados do capítulo do checkpoint
                    chapter_data = {
                        'chapter_number': checkpoint.chapter_number,
                        'chapter_title': checkpoint.chapter_summary['titulo'],
                        'summary_text': checkpoint.chapter_summary['resumo'],
                        'summary_object': checkpoint.chapter_summary,
                        'recall_set': checkpoint.coverage_report.get('recall_set', {}),
                        'audit_result': checkpoint.coverage_report.get('audit_result', {}),
                        'total_chunks': checkpoint.coverage_report.get('total_chunks', 0),
                        'processed_chunks': checkpoint.coverage_report.get('processed_chunks', 0)
                    }
                    chapter_summaries.append(chapter_data)
                    logger.info(f"  ✅ Capítulo {chapter.number} restaurado do checkpoint")
                    continue
                else:
                    logger.warning(f"  ⚠️ Checkpoint do capítulo {chapter.number} não encontrado, reprocessando...")
                    # Se checkpoint não encontrado, remover da lista e reprocessar
                    processed_chapters.remove(chapter.number)
            
            logger.info(f"  📖 Processando Capítulo {chapter.number}: {chapter.title}")
            logger.info(f"  📖 Processando Capítulo {chapter.number}: {chapter.title}")
            
            # Processar capítulo e coletar dados do pipeline
            # Precisamos acessar recall_set e extrações do pipeline
            # Vamos modificar summarize_chapter_robust para retornar também esses dados
            summary, pipeline_data = await self._summarize_chapter_with_data(
                chapter, text
            )
            
            # Coletar dados para evidências
            # Garantir que recall_set tem estrutura correta
            recall_set_data = pipeline_data.get('recall_set', {})
            
            # Debug: verificar se recall_set está vazio
            if not recall_set_data:
                logger.warning(f"  ⚠️ Recall Set vazio no pipeline_data para capítulo {chapter.number}")
                recall_set_data = {
                    'critical_items': [],
                    'supporting_items': []
                }
            elif not recall_set_data.get('critical_items'):
                logger.warning(f"  ⚠️ Recall Set sem critical_items para capítulo {chapter.number} (recall_set_data keys: {list(recall_set_data.keys())})")
                logger.warning(f"  ⚠️ pipeline_data keys: {list(pipeline_data.keys())}")
                logger.warning(f"  ⚠️ pipeline_data['recall_set'] type: {type(pipeline_data.get('recall_set'))}")
                # Tentar usar recall_set do summary se disponível
                # Por enquanto, manter estrutura vazia
            
            # Construir coverage_report parcial conforme F2
            coverage_report_partial = {
                'chapter_number': chapter.number,
                'chapter_title': chapter.title,
                'total_chunks': pipeline_data.get('total_chunks', 0),
                'processed_chunks': pipeline_data.get('processed_chunks', 0),
                'chunk_coverage_percentage': (pipeline_data.get('processed_chunks', 0) / pipeline_data.get('total_chunks', 1)) * 100.0 if pipeline_data.get('total_chunks', 0) > 0 else 0.0,
                'recall_set': recall_set_data,
                'audit_result': pipeline_data.get('audit_result', {
                    'passed': True,
                    'regeneration_count': 0,
                    'addendum_count': 0,
                    'missing_markers': [],
                    'invalid_chunks': []
                })
            }
            
            chapter_data = {
                'chapter_number': summary.numero,
                'chapter_title': chapter.title,
                'summary_text': summary.resumo,
                # Dados completos do ChapterSummary para persistência
                'summary_object': {
                    'numero': summary.numero,
                    'titulo': summary.titulo,
                    'palavras': summary.palavras,
                    'palavras_resumo': summary.palavras_resumo,
                    'paginas': summary.paginas,
                    'resumo': summary.resumo,
                    'pontos_chave': summary.pontos_chave,
                    'citacoes': summary.citacoes,
                    'exemplos': summary.exemplos
                },
                'recall_set': recall_set_data,
                'audit_result': pipeline_data.get('audit_result', {
                    'passed': True,
                    'regeneration_count': 0,
                    'missing_markers': [],
                    'invalid_chunks': []
                }),
                'total_chunks': pipeline_data.get('total_chunks', 0),
                'processed_chunks': pipeline_data.get('processed_chunks', 0)
            }
            chapter_summaries.append(chapter_data)
            
            # F4: Criar checkpoint após processamento completo do capítulo (F2)
            # Checkpoint criado no ponto definido em F2: após processamento completo de cada capítulo
            try:
                # Atualizar metadados de processamento
                self.process_metadata['capitulos_processados'] = list(set(self.process_metadata.get('capitulos_processados', []) + [chapter.number]))
                self.process_metadata['chunks_processados_por_capitulo'][chapter.number] = pipeline_data.get('processed_chunks', 0)
                self.process_metadata['total_chunks_por_capitulo'][chapter.number] = pipeline_data.get('total_chunks', 0)
                self.process_metadata['timestamp_ultimo_checkpoint'] = datetime.now().isoformat()
                
                # Salvar checkpoint atomicamente conforme F3
                checkpoint_path = self.checkpoint_manager.save_checkpoint(
                    session_id=self.session_id,
                    chapter_number=chapter.number,
                    chapter_summary=chapter_data['summary_object'],
                    coverage_report=coverage_report_partial,
                    metadata=self.process_metadata
                )
                logger.info(f"  ✅ Checkpoint salvo: {checkpoint_path}")
            except Exception as e:
                logger.error(f"  ❌ Erro ao salvar checkpoint do capítulo {chapter.number}: {e}")
                # Não falhar o processamento se checkpoint falhar, mas logar erro
                import traceback
                traceback.print_exc()
            
            # Coletar extrações
            all_extractions[f'chapter_{chapter.number}'] = pipeline_data.get('extractions', {})
        
        # 3. Gerar evidências
        logger.info("  📊 Gerando evidências...")
        evidence_files = self.evidence_generator.generate_robust_evidence(
            chapter_summaries=chapter_summaries,
            extractions=all_extractions
        )
        logger.info(f"  ✅ Evidências geradas: {evidence_files['coverage_report']}")
        
        # 4. Validar com Quality Gate
        coverage_report_path = self.evidencias_dir / "coverage_report.json"
        logger.info("  🔍 Validando com Quality Gate...")
        passed, errors = self.quality_gate.validate_from_coverage_report(
            str(coverage_report_path)
        )
        
        if not passed:
            error_msg = f"Quality Gate falhou:\n" + "\n".join(f"  - {e}" for e in errors)
            logger.error(f"  ❌ {error_msg}")
            raise CoverageError(error_msg)
        
        logger.info("  ✅ Quality Gate passou!")
        
        # 5. Construir resultado final
        # Incluir dados completos dos capítulos para persistência
        result = {
            'chapters': [
                {
                    'number': cs['chapter_number'],
                    'title': cs['chapter_title'],
                    'summary': cs['summary_text'],
                    # Dados completos do ChapterSummary (se disponível)
                    'summary_object': cs.get('summary_object')
                }
                for cs in chapter_summaries
            ],
            'total_chapters': len(chapter_summaries),
            'evidence_files': evidence_files,
            # Manter chapter_summaries completo para uso na API
            'chapter_summaries': chapter_summaries
        }
        
        return result
    
    async def _detect_chapters(self, text: str) -> List:
        """
        Detecta capítulos no texto.
        
        Args:
            text: Texto completo
            
        Returns:
            Lista de objetos Chapter
        """
        if not self.use_chapters:
            # Fallback: criar um único "capítulo" com todo o texto
            return [Chapter(
                number="1",
                title="Full Text",
                word_count=len(text.split()),
                start_pos=0,
                end_pos=len(text),
                page_markers=[]
            )]
        
        # Tentar Markdown primeiro
        if self.markdown_parser.is_markdown(text):
            chapters = self.markdown_parser.parse_chapters(text)
            if chapters:
                return chapters
        
        # Fallback para detector de capítulos
        chapters = self.chapter_detector.detect_chapters(text)
        
        # Se ainda não detectou, criar um único capítulo com todo o texto (fallback final)
        if not chapters:
            logger.warning("  ⚠️ Nenhum capítulo detectado, usando fallback: 1 capítulo com todo o texto")
            chapters = [Chapter(
                number="1",
                title="Full Text",
                word_count=len(text.split()),
                start_pos=0,
                end_pos=len(text),
                page_markers=[],
                start_line=0,
                pattern_matched="fallback",
                confidence=0.0
            )]
        
        return chapters
    
    async def _summarize_chapter_with_data(self, chapter, full_text) -> tuple:
        """
        Processa capítulo e retorna summary + dados do pipeline.
        
        Returns:
            Tupla (summary, pipeline_data) onde pipeline_data contém:
            - recall_set
            - audit_result
            - total_chunks
            - processed_chunks
            - extractions
        """
        # Obter texto do capítulo
        chapter_text = full_text[chapter.start_pos:chapter.end_pos]
        
        # 1. Chunking
        chunks = self.chapter_summarizer._chunk_chapter(chapter_text, chapter.number)
        total_chunks = len(chunks)
        
        # 2. Extração
        chunk_extractions = await self.chapter_summarizer._extract_from_chunks(chunks)
        processed_chunks = len(chunk_extractions)
        
        # 3. Gerar Recall Set
        # Usar função importada no nível do módulo (permite mock)
        # IMPORTANTE: Acessar através de sys.modules para permitir patch
        import sys
        # Tentar ambos os nomes de módulo (src.summarizer_robust ou summarizer_robust)
        module_name = None
        for name in ['src.summarizer_robust', 'summarizer_robust', __name__]:
            if name in sys.modules:
                module_name = name
                break
        if not module_name:
            module_name = __name__
        current_module = sys.modules[module_name]
        recall_set = getattr(current_module, '_generate_recall_set')(chunk_extractions, chapter.number)
        logger.debug(f"  → Recall Set: {len(recall_set.critical_items)} críticos, {len(recall_set.supporting_items)} suporte")
        
        # Debug: verificar se recall_set foi gerado
        if not recall_set.critical_items:
            logger.warning(f"  ⚠️ Recall Set gerado está vazio para capítulo {chapter.number} (extractions: {len(chunk_extractions)})")
        
        # 4. Gerar resumo com marcadores + Auditoria + Regeneração + Addendum
        # Estratégia A (Gate Z8): 5 tentativas de resumo + 2 tentativas de addendum
        summary_text, regeneration_count, addendum_count = await self.chapter_summarizer._audit_and_regenerate(
            chapter, recall_set, full_text, max_attempts=5, max_addendums=2
        )
        
        # 5. Obter resultado da auditoria final
        from src.recall_auditor import RecallAuditor
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
        final_audit = auditor.audit_summary(summary_text, recall_set_dict, chapter.number)
        
        # 6. Parsear summary
        parsed = self.chapter_summarizer._parse_structured_response(summary_text)
        palavras_resumo = len(parsed['resumo'].split())
        
        summary = ChapterSummary(
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
        
        pipeline_data = {
            'recall_set': recall_set_dict,
            'audit_result': {
                'passed': final_audit.passed,
                'regeneration_count': regeneration_count,
                'addendum_count': addendum_count,  # NOVO: rastreamento de addendum
                'missing_markers': final_audit.missing_markers,
                'invalid_chunks': final_audit.invalid_chunks
            },
            'total_chunks': total_chunks,
            'processed_chunks': processed_chunks,
            'extractions': {
                'chunks': [
                    {
                        'chunk_id': i,
                        'extraction': ext
                    }
                    for i, ext in enumerate(chunk_extractions)
                ]
            }
        }
        
        return (summary, pipeline_data)
