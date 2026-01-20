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
        # Arrange
        tracker = get_progress_tracker()
        
        # Mock summarizer para lançar erro
        mock_summarizer.summarize_robust = AsyncMock(side_effect=Exception("Test error during processing"))
        
        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_summarizer), \
             patch('src.api.routes.get_evidencias_dir', return_value=temp_evidencias_dir):
            
            # Act 1: Iniciar processamento (vai falhar)
            files = {"file": ("test.pdf", sample_pdf_content, "application/pdf")}
            response = client.post("/api/process", files=files)
            
            # Assert 1: Processamento iniciado (status 200 ou 202)
            assert response.status_code in [200, 202], f"Expected 200/202, got {response.status_code}"
            
            # Obter session_id da resposta
            session_id = None
            if response.status_code == 200:
                data = response.json()
                session_id = data.get("session_id")
            else:
                # Se 202, session_id pode estar no header ou precisamos buscar de outra forma
                # Por ora, vamos assumir que está na resposta
                data = response.json() if response.content else {}
                session_id = data.get("session_id")
            
            # Se não temos session_id, tentar obter do tracker (última sessão criada)
            if not session_id:
                # Buscar última sessão criada
                sessions = list(tracker.sessions.keys())
                if sessions:
                    session_id = sessions[-1]
            
            assert session_id is not None, "Session ID deve estar disponível"
            
            # Act 2: Aguardar um pouco para erro ser processado
            await asyncio.sleep(1.0)
            
            # Act 3: Buscar resultado (deve retornar erro estruturado, não 404)
            result_response = client.get(f"/api/result/{session_id}")
            
            # Assert 2: Resultado não deve ser 404
            assert result_response.status_code != 404, \
                f"BUG DETECTADO: Sessão não encontrada após erro (404). Session ID: {session_id}"
            
            # Assert 3: Deve retornar erro estruturado
            if result_response.status_code == 200:
                result_data = result_response.json()
                assert result_data.get("status") == "FAIL" or "errors" in result_data, \
                    f"Resultado deve indicar erro. Recebido: {result_data}"
            
            # Assert 4: Sessão deve existir no tracker
            state = tracker.get_state(session_id)
            assert state is not None, "Sessão deve existir no tracker após erro"
            assert state.stage == "error" or state.complete is True, \
                f"Sessão deve estar marcada como erro ou completa. Estado: {state}"

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
        
        mock_summarizer.summarize_robust = long_processing
        
        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_summarizer), \
             patch('src.api.routes.get_evidencias_dir', return_value=temp_evidencias_dir):
            
            # Act 1: Iniciar processamento
            files = {"file": ("test.pdf", sample_pdf_content, "application/pdf")}
            response = client.post("/api/process", files=files)
            
            assert response.status_code in [200, 202]
            session_id = response.json().get("session_id") if response.content else None
            
            if not session_id:
                sessions = list(tracker.sessions.keys())
                if sessions:
                    session_id = sessions[-1]
            
            assert session_id is not None
            
            # Act 2: Simular SSE interrompido (não conectar SSE, apenas aguardar)
            # Em produção, SSE seria interrompido aqui
            await asyncio.sleep(1.0)  # Aguardar processamento
            
            # Act 3: Tentar buscar resultado (simula frontend após SSE falhar)
            result_response = client.get(f"/api/result/{session_id}")
            
            # Assert: Resultado deve estar disponível ou erro estruturado, não 404
            assert result_response.status_code != 404, \
                f"BUG DETECTADO: Sessão não encontrada após SSE interrompido (404). Session ID: {session_id}"
            
            # Se ainda processando, deve retornar 400 com mensagem informativa
            # Se completo, deve retornar 200 com resultado
            # Se erro, deve retornar 200 com erro estruturado
            assert result_response.status_code in [200, 400], \
                f"Resultado deve ser 200 (completo/erro) ou 400 (em processamento), não {result_response.status_code}"

    @pytest.mark.asyncio
    async def test_mark_error_creates_session_if_not_exists(
        self, client, temp_evidencias_dir, mock_summarizer
    ):
        """
        Teste crítico: mark_error deve criar sessão se não existir.
        
        Este teste valida a correção do bug:
        - Erro ocorre antes de sessão ser criada
        - mark_error deve criar sessão de erro
        - /api/result deve retornar erro estruturado, não 404
        """
        # Arrange
        tracker = get_progress_tracker()
        session_id = "test-error-session-123"
        
        # Act: Marcar erro em sessão que não existe
        tracker.mark_error(session_id, "Test error message", error_result={
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["Test error message"]
        })
        
        # Assert 1: Sessão deve existir
        state = tracker.get_state(session_id)
        assert state is not None, "mark_error deve criar sessão se não existir"
        assert state.stage == "error", "Sessão deve estar marcada como erro"
        assert state.complete is True, "Sessão deve estar completa"
        
        # Assert 2: /api/result deve retornar erro estruturado, não 404
        result_response = client.get(f"/api/result/{session_id}")
        assert result_response.status_code != 404, \
            f"BUG: Sessão criada por mark_error não encontrada (404). Session ID: {session_id}"
        
        if result_response.status_code == 200:
            result_data = result_response.json()
            assert result_data.get("status") == "FAIL" or "errors" in result_data, \
                "Resultado deve indicar erro estruturado"
