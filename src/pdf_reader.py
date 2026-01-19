#!/usr/bin/env python3
"""
CoverageSummarizer - Leitor de PDF
INCR-2: Processamento de arquivos PDF
"""

import sys
from pathlib import Path

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


def read_pdf_pdfplumber(file_path: str) -> str:
    """
    Lê conteúdo de PDF usando pdfplumber (método preferido).
    
    Args:
        file_path: Caminho para o arquivo PDF
    
    Returns:
        Texto extraído do PDF
    """
    text_parts = []
    
    try:
        with pdfplumber.open(file_path) as pdf:
            for page_num, page in enumerate(pdf.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Página {page_num} ---\n{text}\n")
    except Exception as e:
        raise Exception(f"Erro ao ler PDF com pdfplumber: {e}")
    
    return "\n".join(text_parts)


def read_pdf_pypdf2(file_path: str) -> str:
    """
    Lê conteúdo de PDF usando PyPDF2 (fallback).
    
    Args:
        file_path: Caminho para o arquivo PDF
    
    Returns:
        Texto extraído do PDF
    """
    text_parts = []
    
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page_num, page in enumerate(pdf_reader.pages, 1):
                text = page.extract_text()
                if text:
                    text_parts.append(f"--- Página {page_num} ---\n{text}\n")
    except Exception as e:
        raise Exception(f"Erro ao ler PDF com PyPDF2: {e}")
    
    return "\n".join(text_parts)


def read_pdf_file(file_path: str) -> str:
    """
    Lê conteúdo de um arquivo PDF.
    Tenta usar pdfplumber primeiro, depois PyPDF2 como fallback.
    
    Args:
        file_path: Caminho para o arquivo PDF
    
    Returns:
        Texto extraído do PDF
    
    Raises:
        Exception: Se nenhuma biblioteca estiver disponível ou se houver erro
    """
    path = Path(file_path)
    
    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    
    if not path.suffix.lower() == '.pdf':
        raise ValueError(f"Arquivo não é um PDF: {file_path}")
    
    # Tentar pdfplumber primeiro (melhor qualidade)
    if PDFPLUMBER_AVAILABLE:
        try:
            return read_pdf_pdfplumber(str(path))
        except Exception as e:
            print(f"Aviso: Erro com pdfplumber, tentando PyPDF2... ({e})", file=sys.stderr)
    
    # Fallback para PyPDF2
    if PYPDF2_AVAILABLE:
        try:
            return read_pdf_pypdf2(str(path))
        except Exception as e:
            raise Exception(f"Erro ao ler PDF: {e}")
    
    # Nenhuma biblioteca disponível
    raise ImportError(
        "Nenhuma biblioteca de PDF disponível. "
        "Instale pdfplumber ou PyPDF2: pip install pdfplumber PyPDF2"
    )
