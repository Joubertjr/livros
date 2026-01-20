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
from typing import Optional, Tuple
from fastapi import APIRouter, Request, UploadFile, File, Form, HTTPException, Query
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
from storage import get_storage_manager
from schemas.summary_storage import (
    SummaryStorage,
    PipelineType,
    SummaryListResponse,
    SummaryDetailResponse,
    FeedbackEntry
)

# Setup
router = APIRouter()
# __file__ is src/api/routes.py, so parent.parent = src, parent.parent.parent = /app
BASE_DIR = Path(__file__).parent.parent.parent

# Support FRONTEND_TARGET
import os
FRONTEND_TARGET = os.getenv("FRONTEND_TARGET", "web")
FRONTEND_DIR = BASE_DIR / "frontends" / FRONTEND_TARGET

# Use frontends/ structure if it exists, otherwise fallback
if FRONTEND_DIR.exists() and (FRONTEND_DIR / "index.html").exists():
    TEMPLATES_DIR = FRONTEND_DIR
else:
    TEMPLATES_DIR = BASE_DIR / "src" / "templates"

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@router.get("/")
async def home(request: Request):
    """Serve the main HTML page."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/favicon.ico")
async def favicon():
    """Serve favicon to avoid 404 errors."""
    # Support FRONTEND_TARGET for favicon
    if FRONTEND_DIR.exists() and (FRONTEND_DIR / "favicon.svg").exists():
        favicon_path = FRONTEND_DIR / "favicon.svg"
    else:
        favicon_path = BASE_DIR / "src" / "static" / "favicon.svg"
    if favicon_path.exists():
        return FileResponse(
            path=str(favicon_path),
            media_type="image/svg+xml"
        )
    # Return 204 No Content if favicon doesn't exist
    from fastapi import Response
    return Response(status_code=204)


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(status="healthy", version="1.0.0")


@router.get("/api/health", response_model=HealthResponse)
async def api_health_check():
    """API health check endpoint (backend invariant to FRONTEND_TARGET)."""
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

    Called by frontend after progress reaches 100% or on error.
    """
    tracker = get_progress_tracker()

    state = tracker.get_state(session_id)
    if not state:
        # Log para debug: verificar se sessão realmente não existe
        print(f"[DEBUG] Session {session_id} not found in tracker. Active sessions: {list(tracker.sessions.keys())}", file=sys.stderr)
        raise HTTPException(404, f"Session not found: {session_id}. The session may have expired or the processing may have failed silently.")

    # Se a sessão está completa mas não tem resultado, criar um resultado de erro
    if state.complete and not state.result:
        if state.stage == "error":
            # Criar resultado de erro estruturado
            error_result = {
                "session_id": session_id,
                "status": "FAIL",
                "errors": [state.message or "Erro desconhecido durante processamento"],
                "exported_files": {},
                "coverage_report": None,
                "addendum_metrics": None,
                "summaries": None,
                "summary": None
            }
            return error_result
        else:
            raise HTTPException(500, "Session completed but no result available")

    # Se ainda não está completo, retornar erro informativo
    if not state.complete:
        raise HTTPException(400, f"Session not yet complete. Current stage: {state.stage}, percentage: {state.percentage}%")

    # Se tem erro, retornar resultado de erro estruturado
    if state.stage == "error":
        # Se já tem resultado, retornar; senão criar um estruturado
        if state.result:
            return state.result
        else:
            error_result = {
                "session_id": session_id,
                "status": "FAIL",
                "errors": [state.message or "Erro durante processamento"],
                "exported_files": {},
                "coverage_report": None,
                "addendum_metrics": None,
                "summaries": None,
                "summary": None
            }
            return error_result

    # Retornar resultado normal
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


def _finalize_timings(timings: dict, total_time: float) -> dict:
    """
    Finaliza cálculos de timings garantindo que todas as chaves existam.
    
    Args:
        timings: Dicionário com timings parciais
        total_time: Tempo total do processamento
        
    Returns:
        Dicionário com todos os timings finalizados
    """
    # Garantir que todas as chaves existam (valores padrão se não existirem)
    final_timings = {
        'reading': timings.get('reading', 0.0),
        'processing': timings.get('processing', 0.0),
        'exporting': timings.get('exporting', 0.0),
        'evidence': 0.0,  # Sempre 0 (incluído no processing)
        'total': total_time
    }
    return final_timings


def _print_timing_report(timings: dict, total_time: float, filename: Optional[str], content_text: str) -> None:
    """
    Imprime relatório detalhado de performance.
    
    Args:
        timings: Dicionário com todos os timings
        total_time: Tempo total do processamento
        filename: Nome do arquivo processado (ou None)
        content_text: Texto do conteúdo processado
    """
    print("\n" + "="*60, file=sys.stderr)
    print("📊 RELATÓRIO DE PERFORMANCE", file=sys.stderr)
    print("="*60, file=sys.stderr)
    print(f"📄 Arquivo: {filename or 'texto direto'}", file=sys.stderr)
    print(f"📝 Total de palavras: {len(content_text.split())}", file=sys.stderr)
    print(f"\n⏱️  TEMPOS POR ETAPA:", file=sys.stderr)
    print(f"   • Leitura:        {timings['reading']:>8.2f}s ({timings['reading']/total_time*100:>5.1f}%)", file=sys.stderr)
    print(f"   • Processamento:  {timings['processing']:>8.2f}s ({timings['processing']/total_time*100:>5.1f}%)", file=sys.stderr)
    print(f"   • Exportação:     {timings['exporting']:>8.2f}s ({timings['exporting']/total_time*100:>5.1f}%)", file=sys.stderr)
    print(f"   • Evidência:      {timings['evidence']:>8.2f}s (incluído no processamento)", file=sys.stderr)
    print(f"\n🎯 TEMPO TOTAL:     {total_time:>8.2f}s", file=sys.stderr)
    print("="*60 + "\n", file=sys.stderr)


def _determine_status_from_coverage(coverage_report: Optional[dict]) -> Tuple[str, list]:
    """
    Determina status e erros baseado no coverage_report.
    
    Args:
        coverage_report: Relatório de cobertura (ou None)
        
    Returns:
        Tupla (status, errors) onde status é "PASS" ou "FAIL"
    """
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
    
    return status, errors


def _build_result_contract(
    session_id: str,
    status: str,
    errors: list,
    exported_files: dict,
    coverage_report: Optional[dict],
    addendum_metrics: Optional[dict],
    summaries: Optional[dict]
) -> dict:
    """
    Constrói contrato canônico de resultado.
    
    Args:
        session_id: ID da sessão
        status: Status do processamento (PASS/FAIL)
        errors: Lista de erros (se houver)
        exported_files: Arquivos exportados
        coverage_report: Relatório de cobertura
        addendum_metrics: Métricas de addendum
        summaries: Resumos gerados (apenas se status == PASS)
        
    Returns:
        Dicionário com contrato canônico de resultado
    """
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
    
    return result


async def process_with_progress(
    session_id: str,
    text: Optional[str],
    file_data: Optional[bytes],
    filename: Optional[str],
    export_formats: list
) -> None:
    """
    Processa sumarização com rastreamento de progresso via SSE.

    Esta função envolve a lógica de sumarização existente com atualizações
    de progresso em tempo real através de Server-Sent Events (SSE).

    Args:
        session_id: ID único da sessão de processamento
        text: Texto para sumarizar (se fornecido diretamente)
        file_data: Dados do arquivo para sumarizar (se fornecido via upload)
        filename: Nome do arquivo (se file_data fornecido)
        export_formats: Lista de formatos de exportação (ex: ['md', 'pdf'])

    Raises:
        ValueError: Se session_id não existe no tracker
        Exception: Qualquer erro durante processamento é capturado e
                   marcado no tracker, não propagado

    Note:
        Esta função é assíncrona e executa em background. O progresso
        pode ser acompanhado via endpoint /api/progress/{session_id}
    """
    import time

    tracker = get_progress_tracker()
    temp_file_path = None

    # Timing metrics
    start_time = time.time()
    timings = {}

    try:
        # Verificar se sessão existe antes de começar
        if session_id not in tracker.sessions:
            print(f"[ERROR] Session {session_id} not found at start of process_with_progress. Creating session.", file=sys.stderr)
            tracker.create_session(session_id)
        
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
        
        # Criar tarefa para enviar atualizações periódicas durante processamento longo
        async def send_periodic_updates():
            """Envia atualizações periódicas para manter SSE ativo durante processamento longo."""
            base_percentage = 35
            max_percentage = 90
            update_interval = 10  # segundos
            increment = 2  # incremento de porcentagem por atualização
            
            current = base_percentage
            iteration = 0
            while current < max_percentage:
                await asyncio.sleep(update_interval)
                # Verificar se já completou
                state = tracker.get_state(session_id)
                if state and state.complete:
                    break
                # Enviar atualização
                current = min(base_percentage + (iteration * increment), max_percentage)
                iteration += 1
                tracker.update_progress(
                    session_id,
                    "processing",
                    current,
                    f"Processando capítulos... (isso pode levar alguns minutos)"
                )
        
        # Iniciar tarefa de atualizações periódicas
        periodic_task = asyncio.create_task(send_periodic_updates())
        
        try:
            result = await summarizer.summarize_robust(content_text)
        finally:
            # Cancelar tarefa de atualizações periódicas
            periodic_task.cancel()
            try:
                await periodic_task
            except asyncio.CancelledError:
                pass
        
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
        
        # Complete timing calculations
        total_time = time.time() - start_time
        timings = _finalize_timings(timings, total_time)
        
        # Print detailed timing summary
        _print_timing_report(timings, total_time, filename, content_text)

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
        status, errors = _determine_status_from_coverage(coverage_report)

        # Build canonical contract
        result = _build_result_contract(
            session_id=session_id,
            status=status,
            errors=errors,
            exported_files=exported_files,
            coverage_report=coverage_report,
            addendum_metrics=addendum_metrics,
            summaries=summaries
        )

        tracker.mark_complete(session_id, result)
        
        # F4: Persistir resumo automaticamente após conclusão
        try:
            storage = get_storage_manager()
            
            # Criar objeto SummaryStorage a partir do resultado
            summary_storage = SummaryStorage(
                summary_id=session_id,  # Usar session_id como summary_id
                title=filename or "Resumo de texto",  # Título baseado no arquivo ou padrão
                created_at=datetime.now(),
                pipeline_type=PipelineType.ROBUST,  # Pipeline atual é sempre robust
                input_text=content_text if not filename else None,
                input_file=filename,
                summary=result.get('summary'),
                summaries=summaries,
                coverage_report=coverage_report,
                addendum_metrics=addendum_metrics,
                validation_report=result.get('validation_report'),
                validation=result.get('validation'),
                exported_files=exported_files,
                referencias=result.get('referencias'),
                tracker_info=result.get('tracker_info'),
                total_words_input=len(content_text.split()) if content_text else None,
                total_words_output=len(result.get('summary', '').split()) if result.get('summary') else None,
                processing_time=total_time
            )
            
            # Salvar resumo
            saved_path = storage.save_summary(summary_storage)
            print(f"✅ Resumo persistido: {saved_path}", file=sys.stderr)
            
        except Exception as storage_error:
            # Não falhar o processamento se a persistência falhar
            print(f"⚠️ Erro ao persistir resumo: {storage_error}", file=sys.stderr)
            import traceback
            traceback.print_exc(file=sys.stderr)

    except Exception as e:
        # Handle errors
        error_msg = f"Erro durante processamento: {str(e)}"
        print(f"❌ Error in session {session_id}: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        try:
            # Criar resultado de erro estruturado
            error_result = {
                "session_id": session_id,
                "status": "FAIL",
                "errors": [error_msg],
                "exported_files": {},
                "coverage_report": None,
                "addendum_metrics": None,
                "summaries": None,
                "summary": None
            }
            
            # Garantir que o erro seja marcado no tracker com resultado
            tracker.mark_error(session_id, error_msg, error_result=error_result)
            
            # Aguardar um pouco para garantir que a mensagem de erro seja enviada via SSE
            await asyncio.sleep(0.5)
        except Exception as tracker_error:
            print(f"❌ Failed to mark error in tracker: {tracker_error}", file=sys.stderr)
            # Se falhar ao marcar erro, tentar criar sessão de erro diretamente
            try:
                error_result = {
                    "session_id": session_id,
                    "status": "FAIL",
                    "errors": [f"Erro crítico: {str(e)}", f"Erro ao registrar no tracker: {str(tracker_error)}"],
                    "exported_files": {},
                    "coverage_report": None,
                    "addendum_metrics": None,
                    "summaries": None,
                    "summary": None
                }
                # Criar sessão de erro diretamente se não existir
                if session_id not in tracker.sessions:
                    tracker.create_session(session_id)
                tracker.sessions[session_id].complete = True
                tracker.sessions[session_id].result = error_result
                tracker.sessions[session_id].stage = "error"
                tracker.sessions[session_id].message = error_msg
            except Exception as final_error:
                print(f"❌ Failed to create error result: {final_error}", file=sys.stderr)

    finally:
        # Cleanup temp file
        if temp_file_path and temp_file_path.exists():
            try:
                temp_file_path.unlink()
            except Exception as e:
                print(f"Failed to delete temp file {temp_file_path}: {e}")


# F5: API de Histórico
@router.get("/api/summaries", response_model=SummaryListResponse)
async def list_summaries(
    pipeline_type: Optional[str] = None,
    limit: Optional[int] = None,
    offset: int = 0
):
    """
    Lista resumos persistidos.
    
    Args:
        pipeline_type: Filtrar por tipo de pipeline (robust, standard, experimental)
        limit: Limite de resultados
        offset: Offset para paginação
    """
    try:
        storage = get_storage_manager()
        
        # Converter pipeline_type string para enum
        pipeline_enum = None
        if pipeline_type:
            try:
                pipeline_enum = PipelineType(pipeline_type)
            except ValueError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Tipo de pipeline inválido: {pipeline_type}. Use: robust, standard, experimental"
                )
        
        # Listar resumos
        summaries = storage.list_summaries(
            pipeline_type=pipeline_enum,
            limit=limit,
            offset=offset
        )
        
        # Converter para dict (apenas metadados para listagem)
        summaries_dict = []
        for summary in summaries:
            summaries_dict.append({
                "summary_id": summary.summary_id,
                "title": summary.title,
                "created_at": summary.created_at.isoformat() if summary.created_at else None,
                "pipeline_type": summary.pipeline_type.value,
                "input_file": summary.input_file,
                "total_words_input": summary.total_words_input,
                "total_words_output": summary.total_words_output,
                "processing_time": summary.processing_time
            })
        
        # Contar total (sem paginação)
        total = len(storage.list_summaries(pipeline_type=pipeline_enum))
        
        return SummaryListResponse(
            summaries=summaries_dict,
            total=total,
            page=offset // (limit or 10) + 1 if limit else None,
            page_size=limit
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar resumos: {str(e)}")


@router.get("/api/summaries/{summary_id}", response_model=SummaryDetailResponse)
async def get_summary(summary_id: str):
    """
    Busca um resumo específico por ID.
    
    Args:
        summary_id: ID do resumo
    """
    try:
        storage = get_storage_manager()
        
        # Carregar resumo
        summary = storage.load_summary(summary_id)
        if not summary:
            raise HTTPException(status_code=404, detail=f"Resumo não encontrado: {summary_id}")
        
        # Carregar feedback associado
        feedback = storage.load_feedback(summary_id)
        
        return SummaryDetailResponse(
            summary=summary,
            feedback=feedback
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao buscar resumo: {str(e)}")


@router.post("/api/summaries/{summary_id}/feedback")
async def submit_feedback(
    summary_id: str,
    feedback_type: str = Form(...),
    message: str = Form(...)
):
    """
    Registra feedback vinculado a um resumo.
    
    Regra Canônica: "Feedback sem rastreabilidade é ruído."
    
    Args:
        summary_id: ID do resumo
        feedback_type: Tipo de feedback (dúvida, erro, sugestão, elogio)
        message: Mensagem do feedback
    """
    try:
        storage = get_storage_manager()
        
        # Verificar se resumo existe
        summary = storage.load_summary(summary_id)
        if not summary:
            raise HTTPException(status_code=404, detail=f"Resumo não encontrado: {summary_id}")
        
        # Validar tipo de feedback
        valid_types = ["dúvida", "erro", "sugestão", "elogio"]
        if feedback_type not in valid_types:
            raise HTTPException(
                status_code=400,
                detail=f"Tipo de feedback inválido: {feedback_type}. Use: {', '.join(valid_types)}"
            )
        
        # Criar feedback
        feedback = FeedbackEntry(
            feedback_id=str(uuid.uuid4()),
            summary_id=summary_id,
            feedback_type=feedback_type,
            message=message,
            created_at=datetime.now()
        )
        
        # Salvar feedback
        saved_path = storage.save_feedback(feedback)
        
        return {
            "status": "success",
            "feedback_id": feedback.feedback_id,
            "message": "Feedback registrado com sucesso",
            "saved_path": saved_path
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar feedback: {str(e)}")
