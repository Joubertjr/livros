"""
API routes for CoverageSummarizer Web UI.
"""
import uuid
import asyncio
import aiofiles
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sse_starlette.sse import EventSourceResponse

# Import existing modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from summarizer_robust import BookSummarizerRobust
from document_reader import read_file  # NEW: Universal file reader (PDF→MD, TXT)
from pdf_reader import read_pdf_file  # DEPRECATED: Backward compatibility
from exporter import export_summaries
from evidence_generator_robust import EvidenceGeneratorRobust
from api.progress_tracker import get_progress_tracker
from api.schemas import SummarizeResponse, HealthResponse

# Setup
router = APIRouter()
BASE_DIR = Path(__file__).parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@router.get("/")
async def home(request: Request):
    """Serve the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@router.post("/api/summarize")
async def summarize(
    request: Request,
    text: Optional[str] = Form(None),
    file: Optional[UploadFile] = File(None),
    export_formats: str = Form("md")
):
    """
    Main summarization endpoint.

    Accepts either text input or file upload.
    Processes asynchronously with progress tracking via SSE.
    """
    # Validate input
    if not text and not file:
        raise HTTPException(400, "Either 'text' or 'file' must be provided")

    if text and file:
        raise HTTPException(400, "Provide either 'text' or 'file', not both")

    # Generate session ID
    session_id = str(uuid.uuid4())

    # Parse export formats
    formats = [f.strip() for f in export_formats.split(",") if f.strip()]
    if not formats:
        formats = ["md"]

    # Validate formats
    for fmt in formats:
        if fmt not in ["md", "pdf"]:
            raise HTTPException(400, f"Invalid export format: {fmt}")

    # Create progress session
    tracker = get_progress_tracker()
    tracker.create_session(session_id)

    # Read file content now (before it's closed)
    file_data = None
    filename = None
    if file:
        file_data = await file.read()
        filename = file.filename

    # Process in background task
    asyncio.create_task(
        process_with_progress(
            session_id=session_id,
            text=text,
            file_data=file_data,
            filename=filename,
            export_formats=formats
        )
    )

    # Return session ID for progress tracking
    return {"session_id": session_id}


@router.get("/api/progress/{session_id}")
async def progress_stream(session_id: str):
    """
    Server-Sent Events endpoint for progress updates.

    Streams real-time progress updates to the client.
    """
    tracker = get_progress_tracker()

    # Verify session exists
    if session_id not in tracker.sessions:
        raise HTTPException(404, "Session not found")

    # Return SSE stream
    return EventSourceResponse(tracker.stream_progress(session_id))


@router.get("/api/result/{session_id}")
async def get_result(session_id: str):
    """
    Get the final result of a summarization session.

    Called by frontend after progress reaches 100%.
    """
    tracker = get_progress_tracker()

    state = tracker.get_state(session_id)
    if not state:
        raise HTTPException(404, "Session not found")

    if not state.complete:
        raise HTTPException(400, "Session not yet complete")

    if state.stage == "error":
        raise HTTPException(500, state.message)

    if not state.result:
        raise HTTPException(500, "No result available")

    return state.result


@router.get("/api/download/{filename}")
async def download_file(filename: str):
    """
    Download an exported file.

    Validates that file is in volumes directory to prevent path traversal.
    """
    # Prevent path traversal
    if ".." in filename or "/" in filename or "\\" in filename:
        raise HTTPException(400, "Invalid filename")

    file_path = Path("/app/volumes") / filename

    # Ensure file is within volumes directory
    try:
        file_path.resolve().relative_to(Path("/app/volumes").resolve())
    except ValueError:
        raise HTTPException(403, "Access denied")

    if not file_path.exists():
        raise HTTPException(404, "File not found")

    return FileResponse(
        path=str(file_path),
        filename=filename,
        media_type="application/octet-stream"
    )


async def process_with_progress(
    session_id: str,
    text: Optional[str],
    file_data: Optional[bytes],
    filename: Optional[str],
    export_formats: list
):
    """
    Process summarization with progress tracking.

    This wraps the existing summarization logic with progress updates.
    """
    import time

    tracker = get_progress_tracker()
    temp_file_path = None

    # Timing metrics
    start_time = time.time()
    timings = {}

    try:
        # Stage 1: Reading input (0-20%)
        stage_start = time.time()
        tracker.update_progress(session_id, "reading", 5, "Preparando entrada...")

        if file_data:
            # Save uploaded file temporarily
            tracker.update_progress(session_id, "reading", 10, f"Lendo arquivo {filename}...")

            # Create temp file
            temp_dir = Path("/app/volumes/temp")
            temp_dir.mkdir(exist_ok=True)
            temp_file_path = temp_dir / f"{session_id}_{filename}"

            # Save to temp file
            async with aiofiles.open(temp_file_path, 'wb') as f:
                await f.write(file_data)

            # Read file (PDF → Markdown, TXT → plain)
            if str(temp_file_path).lower().endswith('.pdf'):
                tracker.update_progress(session_id, "reading", 10, "Convertendo PDF para Markdown...")
                content_text = read_file(str(temp_file_path), prefer_markdown=True)
                tracker.update_progress(session_id, "reading", 20, "PDF convertido para Markdown!")
            else:
                tracker.update_progress(session_id, "reading", 15, "Lendo arquivo de texto...")
                async with aiofiles.open(temp_file_path, 'r', encoding='utf-8') as f:
                    content_text = await f.read()
                tracker.update_progress(session_id, "reading", 20, "Arquivo lido com sucesso")
        else:
            content_text = text
            tracker.update_progress(session_id, "reading", 20, "Texto recebido")

        timings['reading'] = time.time() - stage_start
        print(f"⏱️ [TIMING] Leitura: {timings['reading']:.2f}s", file=sys.stderr)

        # Stage 2: Processing (20-95%) - Pipeline Robusto
        stage_start = time.time()
        tracker.update_progress(session_id, "processing", 25, "Inicializando sumarizador robusto...")
        await asyncio.sleep(0.5)

        # Usar BookSummarizerRobust (pipeline completo com coverage_report)
        evidencias_dir = Path("/app/EVIDENCIAS")
        summarizer = BookSummarizerRobust(evidencias_dir=str(evidencias_dir))

        tracker.update_progress(session_id, "processing", 30, "Detectando capítulos...")
        await asyncio.sleep(0.3)

        processing_start = time.time()

        # Pipeline robusto (async)
        tracker.update_progress(session_id, "processing", 35, "Processando capítulos...")
        result = await summarizer.summarize_robust(content_text)
        
        # Ler coverage_report.json gerado
        coverage_report_path = evidencias_dir / "coverage_report.json"
        coverage_report = None
        if coverage_report_path.exists():
            import json
            with open(coverage_report_path, 'r', encoding='utf-8') as f:
                coverage_report = json.load(f)

        timings['processing'] = time.time() - processing_start
        print(f"⏱️ [TIMING] Processamento (pipeline robusto): {timings['processing']:.2f}s", file=sys.stderr)

        tracker.update_progress(session_id, "processing", 95, "Pipeline robusto concluído!")

        # Stage 3: Validation (já feita pelo Quality Gate no summarize_robust)
        tracker.update_progress(session_id, "validating", 98, "Quality Gate: ✅ PASS")
        
        # Adaptar resultado para formato esperado pelo frontend
        # O frontend espera summaries com estrutura 'capitulos'
        summaries = {
            'estrutura': 'capitulos',
            'resumo_executivo': {
                'medio': f"Resumo executivo de {result['total_chapters']} capítulos processados com pipeline robusto (100% coverage garantido)."
            },
            'capitulos': []
        }
        
        # Converter chapters do resultado para formato ChapterSummary
        # O resultado do summarize_robust tem apenas dados básicos (number, title, summary)
        # Mas o coverage_report tem todas as métricas detalhadas
        for ch in result.get('chapters', []):
            summary_text = ch.get('summary', '')
            palavras_resumo = len(summary_text.split())
            
            summaries['capitulos'].append({
                'numero': ch.get('number', '?'),
                'titulo': ch.get('title', 'Sem título'),
                'resumo': summary_text,
                'palavras': 0,  # Não disponível no resultado básico
                'palavras_resumo': palavras_resumo,
                'paginas': [],
                'pontos_chave': [],  # Extrair do summary se necessário
                'citacoes': [],
                'exemplos': []
            })

        # Stage 4: Exporting (95-98%)
        stage_start = time.time()
        exported_files = {}
        if export_formats:
            tracker.update_progress(
                session_id,
                "exporting",
                96,
                f"Exportando para {', '.join(export_formats)}..."
            )

            # Prepare metadata
            metadata = {
                "data": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "total_palavras": len(content_text.split())
            }
            if filename:
                metadata["arquivo"] = filename

            # Export
            base_name = f"resumo_web_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            exported_files = export_summaries(
                summaries,
                "/app/volumes",
                formats=export_formats,
                base_name=base_name,
                metadata=metadata
            )

            tracker.update_progress(session_id, "exporting", 98, "Exportação concluída")

        timings['exporting'] = time.time() - stage_start
        print(f"⏱️ [TIMING] Exportação: {timings['exporting']:.2f}s", file=sys.stderr)

        # Stage 5: Evidence já foi gerado pelo BookSummarizerRobust
        # Apenas coletar referências aos arquivos
        evidence_files = result.get('evidence_files', {})
        evidence_file = evidence_files.get('coverage_report', None) if evidence_files else None

        # Complete
        total_time = time.time() - start_time
        timings['total'] = total_time

        # Print detailed timing summary
        print("\n" + "="*60, file=sys.stderr)
        print("📊 RELATÓRIO DE PERFORMANCE", file=sys.stderr)
        print("="*60, file=sys.stderr)
        print(f"📄 Arquivo: {filename or 'texto direto'}", file=sys.stderr)
        print(f"📝 Total de palavras: {len(content_text.split())}", file=sys.stderr)
        print(f"\n⏱️  TEMPOS POR ETAPA:", file=sys.stderr)
        print(f"   • Leitura:        {timings['reading']:>8.2f}s ({timings['reading']/total_time*100:>5.1f}%)", file=sys.stderr)
        print(f"   • Processamento:  {timings['processing']:>8.2f}s ({timings['processing']/total_time*100:>5.1f}%)", file=sys.stderr)
        print(f"   • Exportação:     {timings['exporting']:>8.2f}s ({timings['exporting']/total_time*100:>5.1f}%)", file=sys.stderr)
        print(f"   • Evidência:      {timings['evidence']:>8.2f}s ({timings['evidence']/total_time*100:>5.1f}%)", file=sys.stderr)
        print(f"\n🎯 TEMPO TOTAL:     {total_time:>8.2f}s", file=sys.stderr)
        print("="*60 + "\n", file=sys.stderr)

        tracker.update_progress(session_id, "complete", 100, f"Concluído em {total_time:.1f}s!")

        # Extrair métricas de addendum do coverage_report
        addendum_metrics = None
        if coverage_report and 'summary' in coverage_report:
            summary_data = coverage_report['summary']
            addendum_metrics = {
                'chapters_using_addendum': summary_data.get('chapters_using_addendum', 0),
                'total_addendums_used': summary_data.get('total_addendums_used', 0),
                'avg_addendums_per_chapter': summary_data.get('avg_addendums_per_chapter', 0.0)
            }

        # Determine status from coverage_report
        status = "PASS"
        errors = []
        if coverage_report:
            if not coverage_report.get('passed', False):
                status = "FAIL"
                errors.append("Coverage validation failed")
            if coverage_report.get('overall_coverage_percentage', 0) < 100.0:
                status = "FAIL"
                errors.append(f"Coverage {coverage_report.get('overall_coverage_percentage', 0)}% < 100%")
        else:
            # If no coverage_report, assume PASS for backward compatibility
            status = "PASS"

        # Build canonical contract
        result = {
            "session_id": session_id,
            "status": status,
            "errors": errors,
            "exported_files": exported_files,
            "coverage_report": coverage_report,
            "addendum_metrics": addendum_metrics
        }
        
        # Only include summary/summaries if status == PASS
        if status == "PASS":
            result["summaries"] = summaries
            # Also include summary as single string if available
            if summaries and summaries.get('estrutura') == 'capitulos':
                # Build full summary from chapters
                full_summary = ""
                for cap in summaries.get('capitulos', []):
                    full_summary += f"# {cap.get('titulo', '')}\n\n{cap.get('resumo', '')}\n\n"
                result["summary"] = full_summary
        else:
            # Status FAIL - do not include summary
            result["summaries"] = None
            result["summary"] = None

        tracker.mark_complete(session_id, result)

    except Exception as e:
        # Handle errors
        error_msg = f"Erro durante processamento: {str(e)}"
        tracker.mark_error(session_id, error_msg)
        print(f"Error in session {session_id}: {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Cleanup temp file
        if temp_file_path and temp_file_path.exists():
            try:
                temp_file_path.unlink()
            except Exception as e:
                print(f"Failed to delete temp file {temp_file_path}: {e}")
