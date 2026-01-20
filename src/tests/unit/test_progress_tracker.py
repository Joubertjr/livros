"""
Testes unitários para ProgressTracker (SSE, timings, tratamento de erros).

Gate: Validação de robustez do sistema de progresso.
"""

import pytest
import asyncio
import json
from datetime import datetime
from unittest.mock import patch, AsyncMock

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.progress_tracker import ProgressTracker, ProgressState, get_progress_tracker


class TestProgressTracker:
    """Testes para ProgressTracker."""

    @pytest.fixture
    def tracker(self):
        """Fixture: ProgressTracker limpo."""
        return ProgressTracker(ttl_hours=1)

    @pytest.fixture
    def session_id(self):
        """Fixture: ID de sessão de teste."""
        return "test-session-123"

    def test_create_session(self, tracker, session_id):
        """Teste: Criar sessão deve inicializar estado correto."""
        # Arrange & Act
        tracker.create_session(session_id)

        # Assert
        assert session_id in tracker.sessions
        state = tracker.sessions[session_id]
        assert state.session_id == session_id
        assert state.stage == "initializing"
        assert state.percentage == 0
        assert state.complete is False
        assert session_id in tracker.queues

    def test_update_progress(self, tracker, session_id):
        """Teste: Atualizar progresso deve atualizar estado e enfileirar."""
        # Arrange
        tracker.create_session(session_id)

        # Act
        tracker.update_progress(session_id, "processing", 50, "Processando...")

        # Assert
        state = tracker.sessions[session_id]
        assert state.stage == "processing"
        assert state.percentage == 50
        assert state.message == "Processando..."
        assert not tracker.queues[session_id].empty()

    def test_update_progress_clamps_percentage(self, tracker, session_id):
        """Teste: Porcentagem deve ser limitada entre 0-100."""
        # Arrange
        tracker.create_session(session_id)

        # Act
        tracker.update_progress(session_id, "processing", 150, "Over 100")
        assert tracker.sessions[session_id].percentage == 100

        tracker.update_progress(session_id, "processing", -10, "Negative")
        assert tracker.sessions[session_id].percentage == 0

    def test_mark_complete(self, tracker, session_id):
        """Teste: Marcar como completo deve atualizar estado e enviar mensagem final."""
        # Arrange
        tracker.create_session(session_id)
        result = {"status": "PASS", "summaries": {}}

        # Act
        tracker.mark_complete(session_id, result)

        # Assert
        state = tracker.sessions[session_id]
        assert state.complete is True
        assert state.result == result
        assert not tracker.queues[session_id].empty()

    def test_mark_error(self, tracker, session_id):
        """Teste: Marcar erro deve atualizar estado corretamente."""
        # Arrange
        tracker.create_session(session_id)
        error_msg = "Erro de processamento"

        # Act
        tracker.mark_error(session_id, error_msg)

        # Assert
        state = tracker.sessions[session_id]
        assert state.complete is True
        assert state.stage == "error"
        assert state.message == error_msg

    def test_get_state(self, tracker, session_id):
        """Teste: get_state deve retornar estado correto."""
        # Arrange
        tracker.create_session(session_id)
        tracker.update_progress(session_id, "processing", 75, "75% completo")

        # Act
        state = tracker.get_state(session_id)

        # Assert
        assert state is not None
        assert state.percentage == 75
        assert state.stage == "processing"

    def test_get_state_nonexistent(self, tracker):
        """Teste: get_state deve retornar None para sessão inexistente."""
        # Act
        state = tracker.get_state("nonexistent-session")

        # Assert
        assert state is None

    @pytest.mark.asyncio
    async def test_stream_progress_sends_initial_state(self, tracker, session_id):
        """Teste: stream_progress deve enviar estado inicial."""
        # Arrange
        tracker.create_session(session_id)
        tracker.update_progress(session_id, "reading", 10, "Lendo arquivo...")

        # Act
        events = []
        async for event in tracker.stream_progress(session_id):
            events.append(event)
            if len(events) >= 2:  # Estado inicial + primeira atualização
                break

        # Assert
        assert len(events) >= 1
        assert events[0].startswith("data: ")
        data = json.loads(events[0].replace("data: ", "").strip())
        assert data["session_id"] == session_id
        assert data["stage"] == "reading"
        assert data["percentage"] == 10

    @pytest.mark.asyncio
    async def test_stream_progress_sends_updates(self, tracker, session_id):
        """Teste: stream_progress deve enviar atualizações em tempo real."""
        # Arrange
        tracker.create_session(session_id)

        # Act - iniciar stream em background
        events = []
        async def collect_events():
            async for event in tracker.stream_progress(session_id):
                events.append(event)
                if len(events) >= 3:  # Estado inicial + 2 updates
                    break

        # Enviar atualizações enquanto stream está rodando
        task = asyncio.create_task(collect_events())
        await asyncio.sleep(0.1)  # Dar tempo para stream iniciar

        tracker.update_progress(session_id, "processing", 25, "Processando...")
        await asyncio.sleep(0.1)

        tracker.update_progress(session_id, "processing", 50, "50% completo")
        await asyncio.sleep(0.1)

        # Cancelar task após coletar eventos
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        # Assert
        assert len(events) >= 2

    @pytest.mark.asyncio
    async def test_stream_progress_sends_keepalive_on_timeout(self, tracker, session_id):
        """Teste: stream_progress deve enviar keepalive em timeout."""
        # Arrange
        tracker.create_session(session_id)

        # Act - coletar eventos com timeout
        events = []
        async for event in tracker.stream_progress(session_id):
            events.append(event)
            if len(events) >= 2:  # Estado inicial + keepalive
                break

        # Assert - deve ter keepalive após timeout
        keepalives = [e for e in events if e.startswith(": keepalive")]
        assert len(keepalives) > 0

    @pytest.mark.asyncio
    async def test_stream_progress_completes_on_mark_complete(self, tracker, session_id):
        """Teste: stream_progress deve terminar quando marcado como completo."""
        # Arrange
        tracker.create_session(session_id)

        # Act
        events = []
        async def collect_events():
            async for event in tracker.stream_progress(session_id):
                events.append(event)
                data_str = event.replace("data: ", "").strip()
                if data_str and not data_str.startswith(":"):
                    try:
                        data = json.loads(data_str)
                        if data.get("complete"):
                            break
                    except:
                        pass

        task = asyncio.create_task(collect_events())
        await asyncio.sleep(0.1)

        tracker.mark_complete(session_id, {"status": "PASS"})
        await asyncio.sleep(0.2)

        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass

        # Assert
        complete_events = [
            e for e in events
            if e.startswith("data: ") and "complete" in e
        ]
        assert len(complete_events) > 0

    @pytest.mark.asyncio
    async def test_stream_progress_handles_nonexistent_session(self, tracker):
        """Teste: stream_progress deve retornar erro para sessão inexistente."""
        # Act
        events = []
        async for event in tracker.stream_progress("nonexistent"):
            events.append(event)
            break  # Apenas primeiro evento

        # Assert
        assert len(events) == 1
        data = json.loads(events[0].replace("data: ", "").strip())
        assert "error" in data

    def test_cleanup_old_sessions(self, tracker):
        """Teste: cleanup_old_sessions deve remover sessões antigas."""
        # Arrange
        tracker.create_session("old-session")
        tracker.create_session("new-session")

        # Simular sessão antiga
        old_state = tracker.sessions["old-session"]
        old_state.updated_at = datetime(2020, 1, 1)

        # Act
        removed = tracker.cleanup_old_sessions()

        # Assert
        assert removed >= 1
        assert "old-session" not in tracker.sessions
        assert "new-session" in tracker.sessions

    def test_get_progress_tracker_singleton(self):
        """Teste: get_progress_tracker deve retornar instância singleton."""
        # Act
        tracker1 = get_progress_tracker()
        tracker2 = get_progress_tracker()

        # Assert
        assert tracker1 is tracker2


class TestProgressTrackerErrorHandling:
    """Testes de tratamento de erros do ProgressTracker."""

    @pytest.fixture
    def tracker(self):
        """Fixture: ProgressTracker limpo."""
        return ProgressTracker()

    def test_update_progress_raises_on_nonexistent_session(self, tracker):
        """Teste: update_progress deve lançar exceção para sessão inexistente."""
        # Act & Assert
        with pytest.raises(ValueError, match="Session.*not found"):
            tracker.update_progress("nonexistent", "stage", 50, "Message")

    def test_mark_complete_raises_on_nonexistent_session(self, tracker):
        """Teste: mark_complete deve lançar exceção para sessão inexistente."""
        # Act & Assert
        with pytest.raises(ValueError, match="Session.*not found"):
            tracker.mark_complete("nonexistent", {})

    def test_mark_error_creates_session_if_not_exists(self, tracker):
        """Teste: mark_error deve criar sessão de erro se não existir."""
        # Arrange
        nonexistent_id = "nonexistent-session"
        error_message = "Error message"

        # Act
        tracker.mark_error(nonexistent_id, error_message)

        # Assert
        assert nonexistent_id in tracker.sessions
        state = tracker.sessions[nonexistent_id]
        assert state.stage == "error"
        assert state.message == error_message
        assert state.complete is True
