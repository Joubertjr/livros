"""
Markdown Parser for CoverageSummarizer.

Parses Markdown structure to extract chapters and sections.
Replaces complex regex-based chapter detection with simple Markdown parsing.
"""
from dataclasses import dataclass
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)


# Reuse Chapter dataclass from chapter_detector for compatibility
from src.chapter_detector import Chapter


class MarkdownParser:
    """
    Parse Markdown headers to extract chapter structure.

    Much simpler and more reliable than regex patterns on plain text.
    """

    def __init__(self, min_headers: int = 2):
        """
        Initialize parser.

        Args:
            min_headers: Minimum number of headers required to consider structure valid
        """
        self.min_headers = min_headers

    def parse_chapters(self, md_text: str) -> List[Chapter]:
        """
        Extract chapters from Markdown text based on headers.

        Intelligent multi-level strategy:
        1. Try level-2 (##) first
        2. If < 5 valid headers, try level-3 (###)
        3. Choose best level based on header count (5-20 = sweet spot)
        4. Filter out artifacts (—, empty, single chars)
        5. Create Chapter objects

        Args:
            md_text: Markdown text

        Returns:
            List of Chapter objects, or empty list if structure invalid
        """
        lines = md_text.split('\n')

        # Extract headers from all levels
        h2_candidates = self._extract_headers_by_level(lines, level=2)
        h3_candidates = self._extract_headers_by_level(lines, level=3)
        h1_candidates = self._extract_headers_by_level(lines, level=1)

        logger.info(f"📊 Headers encontrados: level-1={len(h1_candidates)}, level-2={len(h2_candidates)}, level-3={len(h3_candidates)}")

        # Intelligent level selection
        header_candidates, pattern_name = self._select_best_level(h1_candidates, h2_candidates, h3_candidates)

        if not header_candidates:
            logger.warning(f"Nenhum header válido encontrado em nenhum nível")
            return []

        logger.info(f"✅ Usando {pattern_name} com {len(header_candidates)} capítulos")

        # Validate structure
        if len(header_candidates) < self.min_headers:
            logger.warning(f"Apenas {len(header_candidates)} headers encontrados (mínimo: {self.min_headers})")
            return []

        # Convert to Chapter objects
        chapters = []
        for i, candidate in enumerate(header_candidates):
            # Calculate end position
            if i + 1 < len(header_candidates):
                end_line = header_candidates[i + 1]['line_num']
            else:
                end_line = len(lines)

            # Extract chapter content
            chapter_lines = lines[candidate['line_num']:end_line]
            chapter_text = '\n'.join(chapter_lines)

            # Count words
            word_count = len(chapter_text.split())

            # Extract page markers if present (format: --- Página N ---)
            page_markers = self._extract_page_markers(chapter_text)

            chapters.append(Chapter(
                number=str(i + 1),
                title=candidate['title'],
                start_pos=candidate['start_pos'],
                end_pos=sum(len(l) + 1 for l in lines[:end_line]),
                start_line=candidate['line_num'],
                page_markers=page_markers,
                word_count=word_count,
                pattern_matched=pattern_name,
                confidence=0.95  # High confidence for Markdown headers
            ))

        logger.info(f"✅ Extraídos {len(chapters)} capítulos via {pattern_name}")
        for ch in chapters:
            logger.info(f"  - Capítulo {ch.number}: {ch.title} ({ch.word_count:,} palavras)")

        return chapters

    def _extract_headers_by_level(self, lines: List[str], level: int) -> List[dict]:
        """
        Extract headers of a specific level from Markdown lines.

        Args:
            lines: List of text lines
            level: Header level (1, 2, or 3)

        Returns:
            List of header candidates with line_num, title, start_pos
        """
        if level == 1:
            prefix = '# '
            exclude_prefix = '## '
            strip_len = 2
        elif level == 2:
            prefix = '## '
            exclude_prefix = '### '
            strip_len = 3
        elif level == 3:
            prefix = '### '
            exclude_prefix = '#### '
            strip_len = 4
        else:
            return []

        header_candidates = []
        for i, line in enumerate(lines):
            if line.startswith(prefix) and not line.startswith(exclude_prefix):
                title = line[strip_len:].strip()
                
                # Remove Markdown formatting (**bold**, _italic_, etc.)
                import re
                title_clean = re.sub(r'\*\*([^*]+)\*\*', r'\1', title)  # Remove **bold**
                title_clean = re.sub(r'\*([^*]+)\*', r'\1', title_clean)  # Remove *italic*
                title_clean = re.sub(r'_([^_]+)_', r'\1', title_clean)  # Remove _italic_
                title_clean = title_clean.strip()

                # Filter artifacts (use cleaned title for validation)
                if self._is_valid_header(title_clean):
                    # But keep original title for display (remove markdown for cleaner display)
                    candidate_title = title_clean if title_clean != title else title
                    header_candidates.append({
                        'line_num': i,
                        'title': candidate_title,
                        'start_pos': sum(len(l) + 1 for l in lines[:i])
                    })

        return header_candidates

    def _select_best_level(self, h1: List[dict], h2: List[dict], h3: List[dict]) -> tuple:
        """
        Select the best header level to use for chapters.

        Strategy:
        - Prefer level-2 if it has >= 5 valid headers
        - Otherwise try level-3 if it has 5-20 headers
        - Otherwise use whichever has most headers (>= min_headers)

        Args:
            h1: Level-1 header candidates
            h2: Level-2 header candidates
            h3: Level-3 header candidates

        Returns:
            Tuple of (selected_headers, pattern_name)
        """
        # Count valid headers
        count_h1 = len(h1)
        count_h2 = len(h2)
        count_h3 = len(h3)

        # Strategy 1: Level-2 with >= 5 headers (typical book structure)
        if count_h2 >= 5:
            logger.info(f"🎯 Estratégia: level-2 (##) com {count_h2} capítulos")
            return h2, 'markdown_h2'

        # Strategy 2: Level-3 with 5-20 headers (detailed chapters)
        if 5 <= count_h3 <= 20:
            logger.info(f"🎯 Estratégia: level-3 (###) com {count_h3} capítulos (level-2 tinha apenas {count_h2})")
            return h3, 'markdown_h3'

        # Strategy 3: Level-3 with > 20 headers but level-2 too few
        if count_h3 > 20 and count_h2 >= self.min_headers:
            logger.info(f"🎯 Estratégia: level-2 (##) com {count_h2} capítulos (level-3 muito fragmentado: {count_h3})")
            return h2, 'markdown_h2'

        # Strategy 4: Use level-3 if it has more than level-2
        if count_h3 >= self.min_headers and count_h3 > count_h2:
            logger.info(f"🎯 Estratégia: level-3 (###) com {count_h3} capítulos")
            return h3, 'markdown_h3'

        # Strategy 5: Use level-2 if valid
        if count_h2 >= self.min_headers:
            logger.info(f"🎯 Estratégia: level-2 (##) com {count_h2} capítulos")
            return h2, 'markdown_h2'

        # Strategy 6: Try level-1 as last resort
        if count_h1 >= self.min_headers:
            logger.info(f"🎯 Estratégia: level-1 (#) com {count_h1} capítulos (fallback)")
            return h1, 'markdown_h1'

        # No valid structure found
        logger.warning(f"❌ Nenhum nível válido: h1={count_h1}, h2={count_h2}, h3={count_h3}")
        return [], 'none'

    def _is_valid_header(self, title: str) -> bool:
        """
        Check if header title is valid (not an artifact or table of contents).

        Filters out:
        - Empty strings
        - Single characters
        - Just dashes/symbols (—, -, etc.)
        - Very short titles (< 3 chars)
        - Table of contents headers (CONTENTS, ÍNDICE, etc.)
        """
        if not title or len(title) < 3:
            return False

        # Filter common artifacts
        if title in ['—', '-', '–', '*', '•']:
            return False

        # Must contain at least one letter
        if not any(c.isalpha() for c in title):
            return False

        # Filter table of contents / index headers
        title_upper = title.upper().strip()
        toc_keywords = [
            'CONTENTS',
            'TABLE OF CONTENTS',
            'ÍNDICE',
            'SUMÁRIO',
            'CONTENT',
            'TABLE DES MATIÈRES',
            'INHALTSVERZEICHNIS'
        ]
        
        # Check if title is exactly a TOC keyword or starts with it
        if title_upper in toc_keywords:
            logger.debug(f"Filtrando header de índice: {title}")
            return False
        
        # Check if title starts with TOC keywords (e.g., "CONTENTS Page 1")
        for keyword in toc_keywords:
            if title_upper.startswith(keyword):
                logger.debug(f"Filtrando header que começa com índice: {title}")
                return False

        return True

    def _extract_page_markers(self, text: str) -> List[int]:
        """
        Extract page numbers from text.

        Looks for markers in format: --- Página N ---

        Args:
            text: Chapter text

        Returns:
            List of page numbers found
        """
        import re
        page_numbers = []
        for match in re.finditer(r'---\s*Página\s+(\d+)\s*---', text, re.IGNORECASE):
            page_numbers.append(int(match.group(1)))

        return sorted(set(page_numbers))  # Remove duplicates and sort

    def is_markdown(self, text: str) -> bool:
        """
        Detect if text has Markdown structure.

        Args:
            text: Text to check

        Returns:
            True if text appears to be Markdown
        """
        lines = text.split('\n')

        # Count headers
        header_count = sum(
            1 for line in lines
            if line.strip().startswith('#')
        )

        # If >= 3 headers, probably Markdown
        return header_count >= 3
