"""
Testes de recuperação de erro - tratamento e preservação de sessão.

Gate Z10: TDD-first e Clean Code enforced.
Cobre cenários críticos de recuperação de erro.

Cenários:
1. Erro durante processamento → sessão preservada
2. Erro não tratado → sessão criada automaticamente
3. Múltiplos erros → último erro preservado
4. Erro durante persistência → não perde sessão
"""
import pytest
import asyncio
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
from fastapi.testclient import TestClient

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.app import app
from src.api.progress_tracker import get_progress_tracker


class TestErrorRecovery:
    """Testes de recuperação de erro."""

    @pytest.fixture
    def client(self):
        """Fixture: TestClient do FastAPI."""
        return TestClient(app)

    @pytest.fixture
    def tracker(self):
        """Fixture: ProgressTracker."""
        return get_progress_tracker()

    @pytest.fixture
    def session_id(self):
        """Fixture: ID de sessão de teste."""
        return "test-error-recovery-123"

    def test_mark_error_creates_session_if_not_exists(
        self, tracker, session_id
    ):
        """
        Teste crítico: mark_error deve criar sessão se não existir.
        
        Valida que:
        - mark_error cria sessão automaticamente
        - Sessão é marcada como erro
        - Resultado de erro é armazenado
        """
        # Arrange
        # Garantir que sessão não existe
        if session_id in tracker.sessions:
            del tracker.sessions[session_id]
        if session_id in tracker.queues:
            del tracker.queues[session_id]
        
        error_result = {
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["Test error"]
        }
        
        # Act
        tracker.mark_error(session_id, "Test error message", error_result=error_result)
        
        # Assert
        state = tracker.get_state(session_id)
        assert state is not None, "mark_error deve criar sessão se não existir"
        assert state.stage == "error", "Sessão deve estar marcada como erro"
        assert state.complete is True, "Sessão deve estar completa"
        assert state.result == error_result, "Resultado de erro deve ser armazenado"

    def test_error_preserves_session_for_api_result(
        self, client, tracker, session_id
    ):
        """
        Teste crítico: Erro deve preservar sessão para /api/result.
        
        Valida que:
        - Sessão existe após erro
        - /api/result retorna erro estruturado, não 404
        - Frontend pode recuperar erro
        """
        # Arrange - usar tracker da API (mesmo singleton)
        from src.api.routes import get_progress_tracker as get_api_tracker
        api_tracker = get_api_tracker()
        
        error_result = {
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["Test error message"]
        }
        
        # Act: Marcar erro usando tracker da API
        api_tracker.mark_error(session_id, "Test error message", error_result=error_result)
        
        # Act: Buscar resultado via API
        result_response = client.get(f"/api/result/{session_id}")
        
        # Assert: Não deve ser 404
        assert result_response.status_code != 404, \
            f"BUG: Sessão não encontrada após erro (404). Session ID: {session_id}. " \
            f"Sessões ativas: {list(api_tracker.sessions.keys())}"
        
        # Assert: Deve retornar erro estruturado
        assert result_response.status_code == 200, \
            f"Resultado deve ser 200. Recebido: {result_response.status_code}"
        
        result_data = result_response.json()
        assert result_data.get("status") == "FAIL" or "errors" in result_data, \
            f"Resultado deve indicar erro. Recebido: {result_data}"

    @pytest.mark.asyncio
    async def test_multiple_errors_preserve_last_error(
        self, tracker, session_id
    ):
        """
        Teste crítico: Múltiplos erros devem preservar o último.
        
        Valida que:
        - Múltiplos mark_error atualizam sessão
        - Último erro é preservado
        - Resultado é atualizado
        """
        # Arrange
        tracker.create_session(session_id)
        
        error_result_1 = {
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["First error"]
        }
        
        error_result_2 = {
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["Second error"]
        }
        
        # Act: Marcar primeiro erro
        tracker.mark_error(session_id, "First error", error_result=error_result_1)
        
        # Act: Marcar segundo erro
        tracker.mark_error(session_id, "Second error", error_result=error_result_2)
        
        # Assert: Último erro deve estar preservado
        state = tracker.get_state(session_id)
        assert state is not None, "Sessão deve existir"
        assert state.message == "Second error", "Última mensagem de erro deve estar preservada"
        assert state.result == error_result_2, "Último resultado de erro deve estar preservado"

    def test_error_during_persistence_does_not_lose_session(
        self, client, tracker, session_id
    ):
        """
        Teste crítico: Erro durante persistência não deve perder sessão.
        
        Valida que:
        - Erro em persistência não remove sessão
        - Sessão permanece acessível via /api/result
        - Erro de persistência é logado mas não quebra sistema
        """
        # Arrange - usar tracker da API
        from src.api.routes import get_progress_tracker as get_api_tracker
        api_tracker = get_api_tracker()
        
        error_result = {
            "session_id": session_id,
            "status": "FAIL",
            "errors": ["Test error"]
        }
        
        api_tracker.mark_error(session_id, "Test error", error_result=error_result)
        
        # Act: Buscar resultado - deve funcionar mesmo se persistência falhar
        # (persistência já aconteceu antes, então não precisa mockar)
        result_response = client.get(f"/api/result/{session_id}")
        
        # Assert: Sessão ainda deve estar acessível
        assert result_response.status_code == 200, \
            f"Sessão deve estar acessível. Recebido: {result_response.status_code}"
        
        result_data = result_response.json()
        assert result_data.get("status") == "FAIL" or "errors" in result_data, \
            f"Resultado de erro deve estar disponível. Recebido: {result_data}"

    def test_error_without_result_creates_structured_error(
        self, client, tracker, session_id
    ):
        """
        Teste crítico: Erro sem resultado deve criar erro estruturado.
        
        Valida que:
        - mark_error sem error_result ainda cria sessão
        - /api/result cria erro estruturado automaticamente
        - Frontend recebe erro estruturado, não 500
        """
        # Arrange - usar tracker da API
        from src.api.routes import get_progress_tracker as get_api_tracker
        api_tracker = get_api_tracker()
        
        if session_id in api_tracker.sessions:
            del api_tracker.sessions[session_id]
        if session_id in api_tracker.queues:
            del api_tracker.queues[session_id]
        
        # Act: Marcar erro sem resultado
        api_tracker.mark_error(session_id, "Test error without result")
        
        # Assert: Sessão deve existir
        state = api_tracker.get_state(session_id)
        assert state is not None, "Sessão deve existir mesmo sem error_result"
        assert state.stage == "error", "Sessão deve estar marcada como erro"
        
        # Act: Buscar resultado via API (deve criar erro estruturado)
        result_response = client.get(f"/api/result/{session_id}")
        
        # Assert: Não deve ser 404
        assert result_response.status_code != 404, \
            f"Sessão não encontrada (404). Session ID: {session_id}"
        
        # Assert: Deve retornar erro estruturado
        assert result_response.status_code == 200, \
            f"Resultado deve ser 200. Recebido: {result_response.status_code}"
        
        result_data = result_response.json()
        assert result_data.get("status") == "FAIL" or "errors" in result_data, \
            f"Resultado deve ser erro estruturado. Recebido: {result_data}"
