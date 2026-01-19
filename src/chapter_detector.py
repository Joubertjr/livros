"""
Chapter Detection for CoverageSummarizer.

Detects chapter structure in extracted PDF text using multi-pattern regex matching.
"""
from dataclasses import dataclass
from typing import List, Optional, Tuple
import re
import logging

logger = logging.getLogger(__name__)


@dataclass
class Chapter:
    """Represents a detected chapter in the book."""
    number: str           # "1", "I", "One"
    title: str           # "The Pleasure-Pain Balance"
    start_pos: int       # Position inicial no texto
    end_pos: int         # Position final no texto
    start_line: int      # Linha inicial
    page_markers: List[int]  # Páginas contidas no capítulo
    word_count: int      # Total de palavras
    pattern_matched: str # Padrão que detectou este capítulo
    confidence: float    # 0.0-1.0 (confiança na detecção)


class ChapterDetector:
    """
    Detecta capítulos em texto extraído de PDFs.

    Usa múltiplos padrões regex com scoring de confiança para identificar
    estruturas de capítulos em inglês e português.
    """

    # Padrões de detecção com suas respectivas confianças
    PATTERNS = {
        # Inglês - MAIÚSCULAS (alta confiança)
        'en_caps': (
            r'^CHAPTER\s+([0-9IVXLC]+|ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN|ELEVEN|TWELVE)\s*[:\-]?\s*(.*)$',
            0.95
        ),
        # Inglês - Title Case (média confiança)
        'en_title': (
            r'^Chapter\s+([0-9IVXLC]+|One|Two|Three|Four|Five|Six|Seven|Eight|Nine|Ten)\s*[:\-]?\s*(.*)$',
            0.85
        ),
        # Português - MAIÚSCULAS
        'pt_caps': (
            r'^CAPÍTULO\s+([0-9IVXLC]+|UM|DOIS|TRÊS|QUATRO|CINCO|SEIS|SETE|OITO|NOVE|DEZ)\s*[:\-]?\s*(.*)$',
            0.95
        ),
        # Português - Title Case
        'pt_title': (
            r'^Capítulo\s+([0-9IVXLC]+|Um|Dois|Três|Quatro|Cinco)\s*[:\-]?\s*(.*)$',
            0.85
        ),
        # Numérico genérico (CH. 1, CAP. 1, etc)
        'numeric': (
            r'^(?:CH|CAP)\.?\s*(\d+)\s*[:\-]?\s*(.*)$',
            0.75
        ),
        # Apenas número + título grande (menos confiável)
        'large_title': (
            r'^(\d+)\s+[A-Z][A-Za-z\s]{20,}$',
            0.70
        ),
        # Romano standalone (I., II., III., etc)
        'roman': (
            r'^([IVXLC]+)\.\s+[A-Z][A-Za-z\s]{10,}$',
            0.80
        )
    }

    def detect_chapters(self, text: str) -> List[Chapter]:
        """
        Detecta capítulos usando multi-pattern matching com scoring.

        Args:
            text: Texto completo extraído do PDF

        Returns:
            Lista de objetos Chapter detectados, ou lista vazia se não
            detectar estrutura válida (< 3 capítulos).
        """
        candidates = []
        lines = text.split('\n')

        logger.info(f"Iniciando detecção de capítulos em {len(lines)} linhas de texto")

        # 1. Buscar matches de todos os padrões
        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped or len(stripped) < 5:
                continue

            for pattern_name, (pattern, confidence) in self.PATTERNS.items():
                match = re.match(pattern, stripped, re.IGNORECASE)
                if match:
                    candidates.append({
                        'line_num': i,
                        'line_text': stripped,
                        'pattern': pattern_name,
                        'confidence': confidence,
                        'chapter_num': match.group(1),
                        'title': match.group(2).strip() if match.lastindex >= 2 else '',
                        'start_pos': sum(len(l) + 1 for l in lines[:i])
                    })
                    logger.debug(f"Candidato detectado (linha {i}, padrão {pattern_name}): {stripped[:60]}")

        logger.info(f"Total de candidatos encontrados: {len(candidates)}")

        # 2. Validar estrutura
        if not self._is_valid_structure(candidates):
            logger.warning("Estrutura de capítulos não validada. Usando fallback para chunks.")
            return []

        logger.info(f"✅ Estrutura validada! Detectados {len(candidates)} capítulos.")

        # 3. Converter em objetos Chapter
        chapters = []
        for i, candidate in enumerate(candidates):
            end_pos = candidates[i+1]['start_pos'] if i+1 < len(candidates) else len(text)
            chapter_text = text[candidate['start_pos']:end_pos]

            chapters.append(Chapter(
                number=candidate['chapter_num'],
                title=candidate['title'],
                start_pos=candidate['start_pos'],
                end_pos=end_pos,
                start_line=candidate['line_num'],
                page_markers=self._extract_page_markers(chapter_text),
                word_count=len(chapter_text.split()),
                pattern_matched=candidate['pattern'],
                confidence=candidate['confidence']
            ))

        # Log resumo
        for ch in chapters:
            logger.info(f"  Cap {ch.number}: {ch.title[:40]}... ({ch.word_count} palavras)")

        return chapters

    def _is_valid_structure(self, candidates: List[dict]) -> bool:
        """
        Valida se candidatos formam estrutura válida de capítulos.

        Critérios:
        - Mínimo 3 capítulos
        - Numeração sequencial (com tolerância a pulos)
        - Espaçamento adequado entre capítulos (mínimo 20 linhas)
        """
        if len(candidates) < 3:
            logger.warning(f"Apenas {len(candidates)} candidatos encontrados (mínimo: 3)")
            return False

        # Verificar numeração sequencial
        numbers = [c['chapter_num'] for c in candidates]

        try:
            nums = [self._parse_chapter_number(n) for n in numbers]

            # Verificar se é crescente (com tolerância a pulos de até 2)
            for i in range(len(nums) - 1):
                if nums[i] > nums[i+1] or nums[i+1] - nums[i] > 3:
                    logger.warning(f"Numeração não sequencial: {nums[i]} -> {nums[i+1]}")
                    return False

        except ValueError as e:
            logger.warning(f"Erro ao parsear números de capítulos: {e}")
            return False

        # Verificar distribuição (capítulos não devem estar muito próximos)
        line_nums = [c['line_num'] for c in candidates]
        gaps = [line_nums[i+1] - line_nums[i] for i in range(len(line_nums) - 1)]
        min_gap = min(gaps)

        if min_gap < 20:  # Menos de 20 linhas = provável falso positivo
            logger.warning(f"Capítulos muito próximos (gap mínimo: {min_gap} linhas)")
            return False

        avg_gap = sum(gaps) / len(gaps)
        logger.info(f"Gaps entre capítulos: min={min_gap}, avg={avg_gap:.1f}, max={max(gaps)}")

        return True

    def _parse_chapter_number(self, num_str: str) -> int:
        """
        Converte número de capítulo (árabe, romano, texto) em int.

        Args:
            num_str: String contendo número do capítulo

        Returns:
            Número do capítulo como inteiro

        Raises:
            ValueError: Se não conseguir parsear
        """
        num_str = num_str.strip().upper()

        # Árabe
        if num_str.isdigit():
            return int(num_str)

        # Romano
        roman_chars = set('IVXLC')
        if all(c in roman_chars for c in num_str):
            return self._roman_to_int(num_str)

        # Texto (One, Two, etc.)
        text_map = {
            # Inglês
            'ONE': 1, 'TWO': 2, 'THREE': 3, 'FOUR': 4, 'FIVE': 5,
            'SIX': 6, 'SEVEN': 7, 'EIGHT': 8, 'NINE': 9, 'TEN': 10,
            'ELEVEN': 11, 'TWELVE': 12,
            # Português
            'UM': 1, 'DOIS': 2, 'TRÊS': 3, 'QUATRO': 4, 'CINCO': 5,
            'SEIS': 6, 'SETE': 7, 'OITO': 8, 'NOVE': 9, 'DEZ': 10
        }

        if num_str in text_map:
            return text_map[num_str]

        raise ValueError(f"Não foi possível parsear número de capítulo: {num_str}")

    def _roman_to_int(self, s: str) -> int:
        """
        Converte número romano para inteiro.

        Args:
            s: String com número romano (ex: "XIV")

        Returns:
            Número inteiro equivalente
        """
        roman_map = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100}
        total = 0
        prev_value = 0

        for c in reversed(s):
            value = roman_map.get(c, 0)
            if value < prev_value:
                total -= value
            else:
                total += value
            prev_value = value

        return total

    def _extract_page_markers(self, text: str) -> List[int]:
        """
        Extrai números de página do texto.

        Busca por marcadores no formato: --- Página N ---

        Args:
            text: Texto do capítulo

        Returns:
            Lista de números de página encontrados
        """
        page_numbers = []
        for match in re.finditer(r'---\s*Página\s+(\d+)\s*---', text, re.IGNORECASE):
            page_numbers.append(int(match.group(1)))

        return sorted(set(page_numbers))  # Remove duplicatas e ordena
