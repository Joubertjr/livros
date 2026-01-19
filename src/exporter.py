#!/usr/bin/env python3
"""
CoverageSummarizer - Módulo de Exportação
INCR-5: Exportação para Markdown e PDF
"""

import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

try:
    from reportlab.lib.pagesizes import letter, A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
    from reportlab.pdfbase import pdfmetrics
    from reportlab.pdfbase.ttfonts import TTFont
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


def generate_filename(base_name: str = "resumo", extension: str = "md") -> str:
    """
    Gera nome de arquivo único e descritivo.
    
    Args:
        base_name: Nome base do arquivo
        extension: Extensão do arquivo (md ou pdf)
    
    Returns:
        Nome de arquivo formatado
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{base_name}_{timestamp}.{extension}"


def export_to_markdown(summaries: Dict, output_path: str, metadata: Optional[Dict] = None) -> str:
    """
    Exporta resumos para formato Markdown.
    
    Args:
        summaries: Dicionário com os resumos gerados
        output_path: Caminho onde salvar o arquivo
        metadata: Metadados adicionais (data, livro, etc.)
    
    Returns:
        Caminho do arquivo salvo
    """
    output = []
    
    # Cabeçalho
    output.append("# Resumos Gerados - CoverageSummarizer")
    output.append("")
    
    # Metadados
    if metadata:
        output.append("## Informações")
        output.append("")
        if metadata.get("data"):
            output.append(f"- **Data**: {metadata['data']}")
        if metadata.get("livro"):
            output.append(f"- **Livro**: {metadata['livro']}")
        if metadata.get("total_palavras"):
            output.append(f"- **Total de palavras**: {metadata['total_palavras']}")
        output.append("")
    
    # Informações de rastreabilidade
    if "tracker_info" in summaries:
        info = summaries["tracker_info"]
        output.append("## Informações do Texto Original")
        output.append("")
        output.append(f"- **Total de palavras**: {info.get('total_palavras', 'N/A')}")
        output.append(f"- **Total de segmentos**: {info.get('total_segmentos', 'N/A')}")
        output.append("")
    
    # Resumo Curto
    if "curto" in summaries:
        output.append("---")
        output.append("## 📝 Resumo Curto (até 100 palavras)")
        output.append("")
        output.append(summaries["curto"])
        output.append("")
        
        # Referências
        if "referencias" in summaries and summaries["referencias"].get("curto"):
            output.append("### Referências no Texto Original")
            output.append("")
            from tracker import format_references
            for key, refs in list(summaries["referencias"]["curto"].items())[:3]:
                output.append(f"**{key[:80]}...**")
                output.append(format_references(refs))
                output.append("")
    
    # Resumo Médio
    if "medio" in summaries:
        output.append("---")
        output.append("## 📄 Resumo Médio (até 300 palavras)")
        output.append("")
        output.append(summaries["medio"])
        output.append("")
        
        # Referências
        if "referencias" in summaries and summaries["referencias"].get("medio"):
            output.append("### Referências no Texto Original")
            output.append("")
            from tracker import format_references
            for key, refs in list(summaries["referencias"]["medio"].items())[:5]:
                output.append(f"**{key[:80]}...**")
                output.append(format_references(refs))
                output.append("")
    
    # Resumo Longo
    if "longo" in summaries:
        output.append("---")
        output.append("## 📚 Resumo Longo (até 500 palavras)")
        output.append("")
        output.append(summaries["longo"])
        output.append("")
        
        # Referências
        if "referencias" in summaries and summaries["referencias"].get("longo"):
            output.append("### Referências no Texto Original")
            output.append("")
            from tracker import format_references
            for key, refs in list(summaries["referencias"]["longo"].items())[:7]:
                output.append(f"**{key[:80]}...**")
                output.append(format_references(refs))
                output.append("")
    
    # Bullet Points
    if "bullets" in summaries:
        output.append("---")
        output.append("## 🔹 Bullet Points Principais")
        output.append("")
        output.append(summaries["bullets"])
        output.append("")
        
        # Referências
        if "referencias" in summaries and summaries["referencias"].get("bullets"):
            output.append("### Referências no Texto Original")
            output.append("")
            from tracker import format_references
            for key, refs in list(summaries["referencias"]["bullets"].items())[:5]:
                output.append(f"**{key[:80]}...**")
                output.append(format_references(refs))
                output.append("")
    
    # Quality Gate Report
    if "validation_report" in summaries:
        output.append("---")
        output.append("## Quality Gate - Relatório de Validação")
        output.append("")
        # Converter relatório de texto para markdown
        report_lines = summaries["validation_report"].split("\n")
        for line in report_lines:
            if line.startswith("="):
                output.append("")
            elif "✅" in line or "❌" in line:
                output.append(f"### {line}")
            elif line.strip() and not line.startswith("─"):
                output.append(line)
        output.append("")
    
    # Rodapé
    output.append("---")
    output.append("")
    output.append(f"*Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}*")
    
    # Salvar arquivo
    content = "\n".join(output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return output_path


def export_to_pdf(summaries: Dict, output_path: str, metadata: Optional[Dict] = None) -> str:
    """
    Exporta resumos para formato PDF.
    
    Args:
        summaries: Dicionário com os resumos gerados
        output_path: Caminho onde salvar o arquivo
        metadata: Metadados adicionais
    
    Returns:
        Caminho do arquivo salvo
    
    Raises:
        ImportError: Se reportlab não estiver disponível
    """
    if not REPORTLAB_AVAILABLE:
        raise ImportError("reportlab não está instalado. Instale com: pip install reportlab")
    
    # Criar documento PDF
    doc = SimpleDocTemplate(output_path, pagesize=A4)
    story = []
    styles = getSampleStyleSheet()
    
    # Estilos customizados
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor='#1a1a1a',
        spaceAfter=12,
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=14,
        textColor='#2c3e50',
        spaceAfter=10,
        spaceBefore=12,
    )
    
    # Título
    story.append(Paragraph("Resumos Gerados - CoverageSummarizer", title_style))
    story.append(Spacer(1, 0.2*inch))
    
    # Metadados
    if metadata:
        story.append(Paragraph("<b>Informações</b>", styles['Heading3']))
        meta_text = []
        if metadata.get("data"):
            meta_text.append(f"<b>Data:</b> {metadata['data']}")
        if metadata.get("livro"):
            meta_text.append(f"<b>Livro:</b> {metadata['livro']}")
        if metadata.get("total_palavras"):
            meta_text.append(f"<b>Total de palavras:</b> {metadata['total_palavras']}")
        
        for meta in meta_text:
            story.append(Paragraph(meta, styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Informações de rastreabilidade
    if "tracker_info" in summaries:
        story.append(Paragraph("<b>Informações do Texto Original</b>", styles['Heading3']))
        info = summaries["tracker_info"]
        story.append(Paragraph(f"<b>Total de palavras:</b> {info.get('total_palavras', 'N/A')}", styles['Normal']))
        story.append(Paragraph(f"<b>Total de segmentos:</b> {info.get('total_segmentos', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))
    
    # Função auxiliar para adicionar resumo
    def add_summary(title: str, content: str, references: Optional[Dict] = None, max_refs: int = 3):
        story.append(PageBreak())
        story.append(Paragraph(title, heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        # Dividir conteúdo em parágrafos
        paragraphs = content.split('\n\n')
        for para in paragraphs:
            if para.strip():
                story.append(Paragraph(para.strip().replace('\n', '<br/>'), styles['Normal']))
                story.append(Spacer(1, 0.1*inch))
        
        # Referências
        if references:
            story.append(Spacer(1, 0.1*inch))
            story.append(Paragraph("<b>Referências no Texto Original</b>", styles['Heading4']))
            for i, (key, refs) in enumerate(list(references.items())[:max_refs]):
                story.append(Paragraph(f"<i>{key[:80]}...</i>", styles['Normal']))
                for ref in refs[:2]:  # Limitar a 2 referências por frase
                    story.append(Paragraph(f"  • {ref}", styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
    
    # Resumo Curto
    if "curto" in summaries:
        refs = summaries.get("referencias", {}).get("curto")
        add_summary("📝 Resumo Curto (até 100 palavras)", summaries["curto"], refs, max_refs=3)
    
    # Resumo Médio
    if "medio" in summaries:
        refs = summaries.get("referencias", {}).get("medio")
        add_summary("📄 Resumo Médio (até 300 palavras)", summaries["medio"], refs, max_refs=5)
    
    # Resumo Longo
    if "longo" in summaries:
        refs = summaries.get("referencias", {}).get("longo")
        add_summary("📚 Resumo Longo (até 500 palavras)", summaries["longo"], refs, max_refs=7)
    
    # Bullet Points
    if "bullets" in summaries:
        refs = summaries.get("referencias", {}).get("bullets")
        add_summary("🔹 Bullet Points Principais", summaries["bullets"], refs, max_refs=5)
    
    # Quality Gate Report
    if "validation_report" in summaries:
        story.append(PageBreak())
        story.append(Paragraph("Quality Gate - Relatório de Validação", heading_style))
        story.append(Spacer(1, 0.1*inch))
        
        report_lines = summaries["validation_report"].split("\n")
        for line in report_lines:
            if line.strip() and not line.startswith("=") and not line.startswith("─"):
                if "✅" in line or "❌" in line:
                    story.append(Paragraph(line, styles['Heading4']))
                else:
                    story.append(Paragraph(line, styles['Normal']))
                story.append(Spacer(1, 0.05*inch))
    
    # Rodapé
    story.append(PageBreak())
    story.append(Spacer(1, 0.5*inch))
    story.append(Paragraph(f"<i>Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</i>", styles['Normal']))
    
    # Construir PDF
    doc.build(story)
    
    return output_path


def export_to_markdown_chapters(summaries: Dict, output_path: str, metadata: Optional[Dict] = None) -> str:
    """
    Exporta resumos estruturados por capítulos para Markdown.

    Args:
        summaries: Dicionário com resumos estruturados (formato de capítulos)
        output_path: Caminho onde salvar o arquivo
        metadata: Metadados adicionais

    Returns:
        Caminho do arquivo salvo
    """
    output = []

    # Cabeçalho
    titulo = metadata.get("livro", "Resumo Estruturado por Capítulos") if metadata else "Resumo Estruturado por Capítulos"
    output.append(f"# {titulo}")
    output.append("")

    # Metadados gerais
    if metadata:
        output.append("## 📋 Informações Gerais")
        output.append("")
        if metadata.get("data"):
            output.append(f"- **Data**: {metadata['data']}")
        if metadata.get("arquivo"):
            output.append(f"- **Arquivo**: {metadata['arquivo']}")
        if metadata.get("total_palavras"):
            output.append(f"- **Total de palavras**: {metadata['total_palavras']:,}")
        output.append("")

    # Estrutura detectada
    if "metadados" in summaries:
        meta = summaries["metadados"]
        output.append("## 📊 Estrutura do Livro")
        output.append("")
        output.append(f"- **Total de capítulos**: {meta.get('total_capitulos', 'N/A')}")
        output.append(f"- **Total de palavras**: {meta.get('total_palavras', 0):,}")
        if "estrutura_detectada" in meta:
            est = meta["estrutura_detectada"]
            output.append(f"- **Método de detecção**: {est.get('metodo', 'N/A')}")
            output.append(f"- **Confiança média**: {est.get('confianca_media', 0):.1%}")
        output.append("")

    # Índice de capítulos (TOC)
    if "capitulos" in summaries and summaries["capitulos"]:
        output.append("## 📚 Índice de Capítulos")
        output.append("")
        for cap in summaries["capitulos"]:
            output.append(f"- [Capítulo {cap['numero']}: {cap['titulo']}](#capítulo-{cap['numero']}-{cap['titulo'].lower().replace(' ', '-')})")
        output.append("")

    # Resumo Executivo
    if "resumo_executivo" in summaries:
        output.append("---")
        output.append("## 📖 Resumo Executivo")
        output.append("")
        output.append(summaries["resumo_executivo"].get("medio", ""))
        output.append("")

    # Resumos por capítulo
    if "capitulos" in summaries:
        output.append("---")
        output.append("## 📑 Resumos Detalhados por Capítulo")
        output.append("")

        for cap in summaries["capitulos"]:
            # Cabeçalho do capítulo
            output.append(f"### Capítulo {cap['numero']}: {cap['titulo']}")
            output.append("")

            # Metadados do capítulo
            info = []
            if cap.get('palavras'):
                info.append(f"**{cap['palavras']:,} palavras**")
            if cap.get('paginas'):
                pages = ', '.join(map(str, cap['paginas']))
                info.append(f"**Páginas**: {pages}")

            if info:
                output.append(" | ".join(info))
                output.append("")

            # Resumo do capítulo
            if cap.get('resumo'):
                output.append("#### 📝 Resumo")
                output.append("")
                output.append(cap['resumo'])
                output.append("")

            # Pontos-chave
            if cap.get('pontos_chave'):
                output.append("#### 🔑 Pontos-Chave")
                output.append("")
                for ponto in cap['pontos_chave']:
                    output.append(f"- {ponto}")
                output.append("")

            # Citações
            if cap.get('citacoes') and cap['citacoes']:
                output.append("#### 💬 Citações")
                output.append("")
                for citacao in cap['citacoes']:
                    output.append(f"> \"{citacao}\"")
                output.append("")

            # Exemplos
            if cap.get('exemplos') and cap['exemplos']:
                output.append("#### 🔬 Exemplos Mencionados")
                output.append("")
                for exemplo in cap['exemplos']:
                    output.append(f"- {exemplo}")
                output.append("")

            output.append("---")
            output.append("")

    # Bullets gerais
    if "bullets_gerais" in summaries and summaries["bullets_gerais"]:
        output.append("## 🔹 Pontos Principais do Livro")
        output.append("")
        for bullet in summaries["bullets_gerais"]:
            output.append(f"- {bullet}")
        output.append("")

    # Rodapé
    output.append("---")
    output.append("")
    output.append(f"*Gerado em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} usando CoverageSummarizer*")
    output.append("")
    output.append("*Resumo estruturado por capítulos com detecção automática*")

    # Salvar arquivo
    content = "\n".join(output)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)

    return output_path


def export_summaries(summaries: Dict, output_dir: str, formats: list = ["md", "pdf"],
                     base_name: str = "resumo", metadata: Optional[Dict] = None) -> Dict[str, str]:
    """
    Exporta resumos em múltiplos formatos.

    Detecta automaticamente se é formato estruturado (com capítulos) ou formato simples.

    Args:
        summaries: Dicionário com os resumos gerados
        output_dir: Diretório onde salvar os arquivos
        formats: Lista de formatos a exportar (md, pdf)
        base_name: Nome base para os arquivos
        metadata: Metadados adicionais

    Returns:
        Dicionário com caminhos dos arquivos exportados
    """
    output_dir_path = Path(output_dir)
    output_dir_path.mkdir(parents=True, exist_ok=True)

    exported_files = {}

    # Preparar metadados
    if metadata is None:
        metadata = {}
    if "data" not in metadata:
        metadata["data"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Detectar formato (com capítulos vs simples)
    is_chapter_format = summaries.get("estrutura") == "capitulos"

    # Exportar Markdown
    if "md" in formats:
        md_filename = generate_filename(base_name, "md")
        md_path = output_dir_path / md_filename
        try:
            if is_chapter_format:
                export_to_markdown_chapters(summaries, str(md_path), metadata)
            else:
                export_to_markdown(summaries, str(md_path), metadata)
            exported_files["markdown"] = str(md_path)
        except Exception as e:
            print(f"Erro ao exportar Markdown: {e}", file=os.sys.stderr)
            import traceback
            traceback.print_exc()

    # Exportar PDF
    if "pdf" in formats:
        pdf_filename = generate_filename(base_name, "pdf")
        pdf_path = output_dir_path / pdf_filename
        try:
            # PDF sempre usa formato simples por enquanto
            # (pode ser expandido no futuro para suportar capítulos)
            export_to_pdf(summaries, str(pdf_path), metadata)
            exported_files["pdf"] = str(pdf_path)
        except Exception as e:
            print(f"Erro ao exportar PDF: {e}", file=os.sys.stderr)
            import traceback
            traceback.print_exc()

    return exported_files
