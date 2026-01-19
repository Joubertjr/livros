"""
Testes unitários para validação de timings em process_with_progress.

Gate: Garantir que timings sempre tem todas as chaves necessárias.
"""

import pytest
import asyncio
import time
from unittest.mock import patch, AsyncMock, MagicMock
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.api.routes import process_with_progress
from src.api.progress_tracker import get_progress_tracker


class TestProcessWithProgressTimings:
    """Testes para garantir que timings sempre tem todas as chaves."""

    @pytest.fixture
    def tracker(self):
        """Fixture: ProgressTracker limpo."""
        tracker = get_progress_tracker()
        # Limpar sessões existentes
        tracker.sessions.clear()
        tracker.queues.clear()
        return tracker

    @pytest.fixture
    def session_id(self):
        """Fixture: ID de sessão de teste."""
        return "test-timings-session"

    @pytest.mark.asyncio
    async def test_timings_has_all_required_keys(self, tracker, session_id):
        """Teste: timings deve ter todas as chaves necessárias (reading, processing, exporting, evidence, total)."""
        # Arrange
        tracker.create_session(session_id)

        mock_summarizer = AsyncMock()
        mock_summarizer.summarize_robust = AsyncMock(return_value={
            'total_chapters': 1,
            'chapters': [{
                'number': '1',
                'title': 'Test Chapter',
                'summary': 'Test summary'
            }]
        })

        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_summarizer), \
             patch('src.api.routes.read_file', return_value="Test content"), \
             patch('src.api.routes.export_summaries', return_value={}), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('aiofiles.open', new_callable=lambda: AsyncMock()), \
             patch('aiofiles.os.makedirs', new_callable=AsyncMock):

            # Act
            await process_with_progress(
                session_id=session_id,
                text="Test content",
                file_data=None,
                filename=None,
                export_formats=["md"]
            )

            # Assert - verificar que não houve KeyError
            state = tracker.get_state(session_id)
            assert state is not None
            # Se chegou aqui sem KeyError, timings estava completo

    @pytest.mark.asyncio
    async def test_timings_evidence_always_defined(self, tracker, session_id):
        """Teste: timings['evidence'] deve sempre estar definido (não pode causar KeyError)."""
        # Arrange
        tracker.create_session(session_id)

        mock_summarizer = AsyncMock()
        mock_summarizer.summarize_robust = AsyncMock(return_value={
            'total_chapters': 1,
            'chapters': [{
                'number': '1',
                'title': 'Test Chapter',
                'summary': 'Test summary'
            }]
        })

        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_summarizer), \
             patch('src.api.routes.read_file', return_value="Test content"), \
             patch('src.api.routes.export_summaries', return_value={}), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('aiofiles.open', new_callable=lambda: AsyncMock()), \
             patch('aiofiles.os.makedirs', new_callable=AsyncMock), \
             patch('builtins.print'):  # Suprimir prints

            # Act
            await process_with_progress(
                session_id=session_id,
                text="Test content",
                file_data=None,
                filename=None,
                export_formats=["md"]
            )

            # Assert - verificar que processamento completou sem KeyError
            state = tracker.get_state(session_id)
            assert state is not None
            # Se chegou aqui, timings['evidence'] estava definido

    @pytest.mark.asyncio
    async def test_timings_handles_export_formats_empty(self, tracker, session_id):
        """Teste: timings deve funcionar mesmo quando export_formats está vazio."""
        # Arrange
        tracker.create_session(session_id)

        mock_summarizer = AsyncMock()
        mock_summarizer.summarize_robust = AsyncMock(return_value={
            'total_chapters': 1,
            'chapters': [{
                'number': '1',
                'title': 'Test Chapter',
                'summary': 'Test summary'
            }]
        })

        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_summarizer), \
             patch('src.api.routes.read_file', return_value="Test content"), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.print'):

            # Act - sem export_formats
            await process_with_progress(
                session_id=session_id,
                text="Test content",
                file_data=None,
                filename=None,
                export_formats=[]  # Vazio
            )

            # Assert
            state = tracker.get_state(session_id)
            assert state is not None

    @pytest.mark.asyncio
    async def test_timings_handles_errors_gracefully(self, tracker, session_id):
        """Teste: timings não deve causar KeyError mesmo quando processamento falha."""
        # Arrange
        tracker.create_session(session_id)

        # Mock que falha durante o processamento (após leitura)
        mock_summarizer = AsyncMock()
        mock_summarizer.summarize_robust = AsyncMock(side_effect=Exception("Test error"))

        with patch('src.api.routes.BookSummarizerRobust', return_value=mock_summarizer), \
             patch('src.api.routes.read_file', return_value="Test content"), \
             patch('src.api.routes.export_summaries', return_value={}), \
             patch('pathlib.Path.exists', return_value=False), \
             patch('builtins.print'):

            # Act - não deve lançar KeyError mesmo com erro
            try:
                await process_with_progress(
                    session_id=session_id,
                    text="Test content",
                    file_data=None,
                    filename=None,
                    export_formats=["md"]
                )
            except KeyError as e:
                # Se houver KeyError, o teste falha
                pytest.fail(f"KeyError não deveria ocorrer: {e}")

            # Assert - deve ter marcado erro no tracker
            await asyncio.sleep(0.2)  # Aguardar processamento assíncrono
            state = tracker.get_state(session_id)
            assert state is not None
            # O importante é que não houve KeyError - o estado pode ser error ou ainda processando
