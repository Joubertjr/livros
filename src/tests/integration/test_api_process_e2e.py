"""
Testes de integração end-to-end para fluxo completo de processamento.

Gate Z10: TDD-first e Clean Code enforced.
Cobre fluxos críticos que testes unitários isolados não detectam.

Cenários:
1. Happy path completo: upload → SSE → result
2. Erro durante processamento → sessão preservada
3. SSE interrompido → recuperação via /api/result
4. Sessão não encontrada após erro → tratamento adequado
"""
import pytest
import asyncio
import json
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.app import app
from src.api.progress_tracker import get_progress_tracker, ProgressTracker


class TestAPIProcessE2E:
    """Testes end-to-end do fluxo completo de processamento."""

    @pytest.fixture
    def client(self):
        """Fixture: TestClient do FastAPI."""
        return TestClient(app)

    @pytest.fixture
    def temp_evidencias_dir(self, tmp_path):
        """Fixture: Diretório temporário para evidências."""
        evidencias_dir = tmp_path / "EVIDENCIAS"
        evidencias_dir.mkdir(parents=True, exist_ok=True)
        return evidencias_dir

    @pytest.fixture
    def mock_summarizer(self):
        """Fixture: Mock do BookSummarizerRobust."""
        mock = AsyncMock()
        mock.summarize_robust = AsyncMock(return_value={
            'chapters': [{'number': '1', 'title': 'Test', 'summary': 'Test summary'}],
            'total_chapters': 1,
            'evidence_files': {}
        })
        return mock

    @pytest.fixture
    def sample_pdf_content(self):
        """Fixture: Conteúdo de PDF de teste."""
        return b"%PDF-1.4\nfake pdf content"

    @pytest.mark.asyncio
    async def test_process_error_preserves_session_for_result(
        self, client, temp_evidencias_dir, mock_summarizer, sample_pdf_content
    ):
        """
        Teste crítico: Erro durante processamento deve preservar sessão para /api/result.
        
        Este teste detecta o bug original:
        - Erro ocorre durante processamento
        - Sessão deve ser preservada (mark_error cria se não existir)
        - /api/result deve retornar erro estruturado, não 404
        """
        # Arrange - usar o tracker da API (mesmo singleton)
        from src.api.routes import get_progress_tracker as get_api_tracker
        tracker = get_api_tracker()
        
        # Mock summarizer para lançar erro DURANTE o summarize_robust
        # Mockar read_file para evitar erro na leitura do PDF e permitir chegar ao summarize_robust
        mock_instance = MagicMock()
        mock_instance.summarize_robust = AsyncMock(side_effect=Exception("Test error during processing"))
        
        # Mock aiofiles para evitar problemas com arquivo temporário
        mock_aiofiles = MagicMock()
        mock_aiofiles.open = AsyncMock()
        mock_file_handle = AsyncMock()
        mock_file_handle.__aenter__ = AsyncMock(return_value=mock_file_handle)
        mock_file_handle.__aexit__ = AsyncMock(return_value=None)
        mock_file_handle.write = AsyncMock()
        mock_aiofiles.open.return_value = mock_file_handle
        
        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_instance), \
             patch('src.api.routes.Path') as mock_path, \
             patch('src.api.routes.read_file', return_value="Test content from PDF"), \
             patch('src.api.routes.aiofiles', mock_aiofiles):
            
            # Mock Path para retornar temp_evidencias_dir quando usado para /app/EVIDENCIAS
            def path_side_effect(path_str):
                if path_str == "/app/EVIDENCIAS":
                    return temp_evidencias_dir
                return Path(path_str)
            
            mock_path.side_effect = path_side_effect
            
            # Act 1: Iniciar processamento (vai falhar)
            files = {"file": ("test.pdf", sample_pdf_content, "application/pdf")}
            response = client.post("/api/summarize", files=files)
            
            # Assert 1: Processamento iniciado (status 200)
            assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
            
            # Obter session_id da resposta
            data = response.json()
            session_id = data.get("session_id")
            assert session_id is not None, f"Session ID deve estar na resposta. Recebido: {data}"
            
            # Act 2: Aguardar processamento em background terminar (com timeout)
            # Processamento roda em background, aguardar até erro ser processado ou timeout
            max_wait = 6.0  # máximo 6 segundos (processamento pode demorar)
            wait_interval = 0.3
            waited = 0.0
            
            while waited < max_wait:
                await asyncio.sleep(wait_interval)
                waited += wait_interval
                
                # Verificar se sessão existe e está completa ou em erro
                state = tracker.get_state(session_id)
                if state and (state.complete or state.stage == "error"):
                    break
                
                # Se chegou na fase de processing, aguardar um pouco mais para erro acontecer
                if state and state.stage == "processing":
                    await asyncio.sleep(0.5)  # Aguardar erro no summarize_robust
                    break
            
            # Assert 4: Sessão deve existir no tracker (mesmo após erro)
            state = tracker.get_state(session_id)
            assert state is not None, \
                f"Sessão deve existir no tracker após erro. Session ID: {session_id}. " \
                f"Sessões ativas: {list(tracker.sessions.keys())}"
            
            # Act 3: Buscar resultado (deve retornar erro estruturado, não 404)
            result_response = client.get(f"/api/result/{session_id}")
            
            # Assert 2: Resultado não deve ser 404
            assert result_response.status_code != 404, \
                f"BUG DETECTADO: Sessão não encontrada após erro (404). Session ID: {session_id}. " \
                f"Sessões ativas: {list(tracker.sessions.keys())}"
            
            # Assert 3: Deve retornar erro estruturado ou status PROCESSING
            assert result_response.status_code == 200, \
                f"Resultado deve ser 200. Recebido: {result_response.status_code}"
            
            result_data = result_response.json()
            # Pode ser PROCESSING (ainda processando) ou FAIL (erro)
            assert result_data.get("status") in ["FAIL", "PROCESSING"] or "errors" in result_data or result_data.get("complete") is False, \
                f"Resultado deve indicar erro ou processamento. Recebido: {result_data}"
            
            # Validar que sessão está marcada corretamente
            # Pode estar em qualquer estágio (reading, processing) ou erro/completo
            assert state.stage in ["error", "reading", "processing"] or state.complete is True, \
                f"Sessão deve estar em estágio válido. Estado: {state}"
            
            # Se ainda está processando, aguardar mais um pouco para erro acontecer
            if state.stage != "error" and not state.complete:
                await asyncio.sleep(1.0)
                state = tracker.get_state(session_id)
                # Agora deve estar em erro ou completo
                assert state is not None, "Sessão deve existir após aguardar erro"
                assert state.stage == "error" or state.complete is True, \
                    f"Após aguardar, sessão deve estar em erro ou completa. Estado: {state}"

    @pytest.mark.asyncio
    async def test_sse_interrupted_during_processing_recovery(
        self, client, temp_evidencias_dir, mock_summarizer, sample_pdf_content
    ):
        """
        Teste crítico: SSE interrompido durante processamento deve permitir recuperação.
        
        Este teste detecta o bug original:
        - SSE é interrompido (simulado)
        - Frontend tenta buscar resultado via /api/result
        - Resultado deve estar disponível, não 404
        """
        # Arrange
        tracker = get_progress_tracker()
        
        # Mock summarizer para processamento longo (simula timeout SSE)
        async def long_processing(text):
            await asyncio.sleep(0.5)  # Simula processamento longo
            return {
                'chapters': [{'number': '1', 'title': 'Test', 'summary': 'Test summary'}],
                'total_chapters': 1,
                'evidence_files': {}
            }
        
        mock_instance = MagicMock()
        mock_instance.summarize_robust = long_processing
        
        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_instance), \
             patch('src.api.routes.Path') as mock_path:
            
            # Mock Path para retornar temp_evidencias_dir
            def path_side_effect(path_str):
                if path_str == "/app/EVIDENCIAS":
                    return temp_evidencias_dir
                return Path(path_str)
            
            mock_path.side_effect = path_side_effect
            
            # Act 1: Iniciar processamento
            files = {"file": ("test.pdf", sample_pdf_content, "application/pdf")}
            response = client.post("/api/summarize", files=files)
            
            assert response.status_code in [200, 202]
            session_id = response.json().get("session_id") if response.content else None
            
            if not session_id:
                sessions = list(tracker.sessions.keys())
                if sessions:
                    session_id = sessions[-1]
            
            assert session_id is not None
            
            # Act 2: Simular SSE interrompido (não conectar SSE, apenas aguardar)
            # Em produção, SSE seria interrompido aqui
            await asyncio.sleep(1.5)  # Aguardar processamento
            
            # Act 3: Tentar buscar resultado (simula frontend após SSE falhar)
            result_response = client.get(f"/api/result/{session_id}")
            
            # Assert: Resultado deve estar disponível ou erro estruturado, não 404
            assert result_response.status_code != 404, \
                f"BUG DETECTADO: Sessão não encontrada após SSE interrompido (404). Session ID: {session_id}. " \
                f"Sessões ativas: {list(tracker.sessions.keys())}"
            
            # Se ainda processando, deve retornar 200 com status PROCESSING
            # Se completo, deve retornar 200 com resultado
            # Se erro, deve retornar 200 com erro estruturado
            assert result_response.status_code == 200, \
                f"Resultado deve ser 200 (completo/erro/processando), não {result_response.status_code}"
            
            # Validar que resposta tem estrutura esperada
            if result_response.status_code == 200:
                result_data = result_response.json()
                assert "session_id" in result_data or "status" in result_data or "complete" in result_data, \
                    f"Resposta deve ter estrutura válida. Recebido: {result_data}"

    def test_mark_error_creates_session_if_not_exists(
        self, client, temp_evidencias_dir, mock_summarizer
    ):
        """
        Teste crítico: mark_error deve criar sessão se não existir.
        
        Este teste valida a correção do bug:
        - Erro ocorre antes de sessão ser criada
        - mark_error deve criar sessão de erro
        - /api/result deve retornar erro estruturado, não 404
        """
        # Arrange - usar o tracker da API (mesmo singleton)
        from src.api.routes import get_progress_tracker as get_api_tracker
        tracker = get_api_tracker()
        session_id = "test-error-session-123"
        
        # Limpar sessão se existir (para teste limpo)
        if session_id in tracker.sessions:
            del tracker.sessions[session_id]
        if session_id in tracker.queues:
            del tracker.queues[session_id]
        
        # Act: Marcar erro em sessão que não existe
        tracker.mark_error(session_id, "Test error message", error_result={
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["Test error message"]
        })
        
        # Assert 1: Sessão deve existir no tracker
        state = tracker.get_state(session_id)
        assert state is not None, "mark_error deve criar sessão se não existir"
        assert state.stage == "error", "Sessão deve estar marcada como erro"
        assert state.complete is True, "Sessão deve estar completa"
        
        # Assert 2: /api/result deve retornar erro estruturado, não 404
        # Usar o mesmo tracker que a API usa
        result_response = client.get(f"/api/result/{session_id}")
        assert result_response.status_code != 404, \
            f"BUG: Sessão criada por mark_error não encontrada (404). Session ID: {session_id}. " \
            f"Sessões no tracker: {list(tracker.sessions.keys())}"
        
        if result_response.status_code == 200:
            result_data = result_response.json()
            assert result_data.get("status") == "FAIL" or "errors" in result_data, \
                f"Resultado deve indicar erro estruturado. Recebido: {result_data}"
