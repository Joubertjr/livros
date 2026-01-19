#!/usr/bin/env python3
"""
CoverageSummarizer - Document Reader (Universal)
Supports PDF, TXT, and Markdown files with PDF→Markdown conversion
"""

import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

# Try to import PDF libraries
try:
    import pymupdf4llm
    PYMUPDF4LLM_AVAILABLE = True
except ImportError:
    PYMUPDF4LLM_AVAILABLE = False

try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False

try:
    import PyPDF2
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False


def read_pdf_to_markdown(file_path: str) -> str:
    """
    Convert PDF to Markdown using PyMuPDF4LLM.

    This is the PREFERRED method for PDF processing as it:
    - Preserves document structure (headers, lists, tables)
    - Detects headings via font sizing
    - Maintains formatting (bold, italic)
    - Enables easy chapter detection

    Args:
        file_path: Path to PDF file

    Returns:
        Markdown-formatted text

    Raises:
        ImportError: If pymupdf4llm not available
        Exception: If conversion fails
    """
    if not PYMUPDF4LLM_AVAILABLE:
        raise ImportError(
            "pymupdf4llm not installed. Install with: pip install pymupdf4llm"
        )

    try:
        logger.info(f"Converting PDF to Markdown: {file_path}")
        md_text = pymupdf4llm.to_markdown(file_path)
        logger.info(f"✅ PDF→MD conversion successful: {len(md_text)} chars")
        return md_text
    except Exception as e:
        raise Exception(f"Error converting PDF to Markdown: {e}")


def read_pdf_plain_text(file_path: str) -> str:
    """
    Read PDF as plain text (fallback method).

    Uses pdfplumber (preferred) or PyPDF2 (fallback).
    This is the OLD method - kept for compatibility.

    Args:
        file_path: Path to PDF file

    Returns:
        Plain text extracted from PDF
    """
    # Try pdfplumber first
    if PDFPLUMBER_AVAILABLE:
        try:
            return _read_pdf_pdfplumber(file_path)
        except Exception as e:
            logger.warning(f"pdfplumber failed, trying PyPDF2... ({e})")

    # Fallback to PyPDF2
    if PYPDF2_AVAILABLE:
        try:
            return _read_pdf_pypdf2(file_path)
        except Exception as e:
            raise Exception(f"Error reading PDF: {e}")

    raise ImportError(
        "No PDF library available. Install pdfplumber or PyPDF2: "
        "pip install pdfplumber PyPDF2"
    )


def _read_pdf_pdfplumber(file_path: str) -> str:
    """Read PDF using pdfplumber (internal helper)."""
    text_parts = []

    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Página {page_num} ---\n{text}\n")
    except Exception as e:
        raise Exception(f"Error reading PDF with pdfplumber: {e}")

    return "\n".join(text_parts)


def _read_pdf_pypdf2(file_path: str) -> str:
    """Read PDF using PyPDF2 (internal helper)."""
    text_parts = []

    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Página {page_num} ---\n{text}\n")
    except Exception as e:
        raise Exception(f"Error reading PDF with PyPDF2: {e}")

    return "\n".join(text_parts)


def read_file(file_path: str, prefer_markdown: bool = True) -> str:
    """
    Universal file reader: PDF, TXT, MD.

    Args:
        file_path: Path to file
        prefer_markdown: If True, convert PDF to Markdown (RECOMMENDED).
                         If False, extract plain text.

    Returns:
        File content (Markdown for PDF, plain text for TXT/MD)

    Raises:
        FileNotFoundError: If file doesn't exist
        ValueError: If file format not supported
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()

    # PDF: Convert to Markdown (preferred) or plain text
    if ext == '.pdf':
        if prefer_markdown and PYMUPDF4LLM_AVAILABLE:
            try:
                return read_pdf_to_markdown(str(path))
            except Exception as e:
                logger.warning(f"PDF→MD failed, using plain text extraction: {e}")
                return read_pdf_plain_text(str(path))
        else:
            return read_pdf_plain_text(str(path))

    # TXT or MD: Read directly
    elif ext in ['.txt', '.md', '.markdown']:
        try:
            return path.read_text(encoding='utf-8')
        except Exception as e:
            raise Exception(f"Error reading text file: {e}")

    else:
        raise ValueError(
            f"Unsupported file format: {ext}. "
            f"Supported: .pdf, .txt, .md"
        )


# Backward compatibility aliases
read_pdf_file = read_pdf_plain_text  # Old function name
