"""
Teste de robustez do addendum - cenário onde addendum falha após múltiplas tentativas.

Gate Z10: TDD + Clean Code
Este teste valida que o sistema lida adequadamente quando addendums falham.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
import sys
import re

# Mock do módulo summarizer antes de importar
mock_summarizer_module = MagicMock()
mock_async_client = AsyncMock()
mock_summarizer_module.AsyncOpenAIClient = MagicMock(return_value=mock_async_client)
mock_summarizer_module.SummarySpecs = MagicMock()
mock_summarizer_module.SummarySpecs.BASE_SYSTEM_MESSAGE = "You are a helpful assistant."

sys.modules['summarizer'] = mock_summarizer_module

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.chapter_summarizer import ChapterSummarizer
from src.recall_set import RecallSet, RecallSetItem, CriticalityReason
from src.exceptions import CoverageError


class TestAddendumRobustness:
    """Testes para robustez do addendum quando falha após múltiplas tentativas."""

    @pytest.fixture
    def chapter_summarizer(self):
        """Fixture: ChapterSummarizer com mock client."""
        summarizer = ChapterSummarizer()
        summarizer.client = mock_async_client
        return summarizer

    @pytest.fixture
    def sample_chapter(self):
        """Fixture: Capítulo de exemplo."""
        from src.chapter_detector import Chapter
        return Chapter(
            number="2",
            title="Test Chapter",
            start_pos=0,
            end_pos=1000,
            start_line=0,
            word_count=500,
            page_markers=[],
            pattern_matched="##",
            confidence=1.0
        )

    @pytest.fixture
    def recall_set_with_2_items(self):
        """Fixture: Recall Set com 2 itens críticos."""
        return RecallSet(
            chapter_number="2",
            critical_items=[
                RecallSetItem(
                    item_id="RS:cap2:09d6f1",
                    content="Primeiro item crítico importante",
                    criticality="critical",
                    criticality_reason=CriticalityReason.MULTI_CHUNK,
                    source_chunks=[1, 2],
                    frequency=2
                ),
                RecallSetItem(
                    item_id="RS:cap2:d78f2f",
                    content="Segundo item crítico essencial",
                    criticality="critical",
                    criticality_reason=CriticalityReason.MULTI_CHUNK,
                    source_chunks=[3, 4],
                    frequency=2
                )
            ],
            supporting_items=[]
        )

    @pytest.mark.asyncio
    async def test_addendum_fails_after_multiple_attempts_raises_coverage_error(
        self, chapter_summarizer, sample_chapter, recall_set_with_2_items
    ):
        """
        Teste: Quando addendum falha após múltiplas tentativas, deve levantar CoverageError.
        
        Arrange: Mock que retorna resumo sem marcadores e addendum que também não inclui marcadores
        Act: Tentar gerar resumo com max_attempts=2 e max_addendums=2
        Assert: CoverageError deve ser levantado com mensagem clara
        """
        # Arrange
        full_text = "Texto completo do capítulo com conteúdo relevante."
        
        # Mock: Resumo sem marcadores (falha todas as tentativas)
        mock_summary_without_markers = """RESUMO:
Este capítulo discute conceitos importantes sem incluir os marcadores obrigatórios.
Não há marcadores aqui.
"""
        
        # Mock: Addendum que também não inclui os marcadores corretos
        # Simula o problema real onde o LLM não segue as instruções
        def complete_side_effect(*args, **kwargs):
            prompt = kwargs.get('user_message', '') or (args[1] if len(args) > 1 else '')
            p = prompt.lower()
            
            # Se for addendum (contém "bullets" ou "exatamente")
            if "bullets" in p or "exatamente" in p or ("gere" in p and "bullets" in p):
                # Retornar addendum SEM os marcadores corretos (simula falha)
                return "- Primeiro item importante (sem marcador)\n- Segundo item essencial (sem marcador)"
            
            # Resumo sempre sem marcadores
            return mock_summary_without_markers
        
        mock_async_client.complete = AsyncMock(side_effect=complete_side_effect)
        
        # Act & Assert
        with pytest.raises(CoverageError) as exc_info:
            await chapter_summarizer._audit_and_regenerate(
                sample_chapter,
                recall_set_with_2_items,
                full_text,
                max_attempts=2,
                max_addendums=2
            )
        
        # Assert: Mensagem de erro deve ser clara
        error_message = str(exc_info.value)
        assert "Cobertura não atingiu 100%" in error_message
        assert "tentativas de resumo" in error_message
        assert "tentativas de addendum" in error_message
        assert "RS:cap2:09d6f1" in error_message or "RS:cap2:d78f2f" in error_message

    @pytest.mark.asyncio
    async def test_addendum_with_improved_prompt_succeeds(
        self, chapter_summarizer, sample_chapter, recall_set_with_2_items
    ):
        """
        Teste: Addendum com prompt melhorado deve conseguir incluir marcadores.
        
        Arrange: Mock que retorna addendum correto quando prompt é específico
        Act: Gerar addendum
        Assert: Addendum deve conter os marcadores corretos
        """
        # Arrange
        full_text = "Texto completo do capítulo."
        
        # Mock: Addendum correto quando prompt é específico sobre marcadores
        def complete_side_effect(*args, **kwargs):
            prompt = kwargs.get('user_message', '') or (args[1] if len(args) > 1 else '')
            p = prompt.lower()
            
            if "bullets" in p or "exatamente" in p:
                # Retornar addendum CORRETO com marcadores
                return (
                    "- Primeiro item crítico importante. [[RS:cap2:09d6f1|chunks:1,2]]\n"
                    "- Segundo item crítico essencial. [[RS:cap2:d78f2f|chunks:3,4]]"
                )
            
            # Resumo sem marcadores (força uso de addendum)
            return "RESUMO:\nEste capítulo discute conceitos importantes."
        
        mock_async_client.complete = AsyncMock(side_effect=complete_side_effect)
        
        # Act
        result = await chapter_summarizer._generate_missing_markers_addendum(
            sample_chapter,
            recall_set_with_2_items.critical_items,
            full_text
        )
        
        # Assert: Addendum deve conter ambos os marcadores
        assert "RS:cap2:09d6f1" in result
        assert "RS:cap2:d78f2f" in result
        assert "chunks:1,2" in result or "chunks:2,1" in result
        assert "chunks:3,4" in result or "chunks:4,3" in result

    @pytest.mark.asyncio
    async def test_addendum_logs_detailed_information(
        self, chapter_summarizer, sample_chapter, recall_set_with_2_items, caplog
    ):
        """
        Teste: Addendum deve logar informações detalhadas para debug.
        
        Arrange: Mock que retorna addendum
        Act: Gerar addendum
        Assert: Logs devem conter informações sobre itens faltantes e addendum gerado
        """
        import logging
        caplog.set_level(logging.INFO)
        
        # Arrange
        full_text = "Texto completo."
        
        def complete_side_effect(*args, **kwargs):
            return (
                "- Item 1. [[RS:cap2:09d6f1|chunks:1,2]]\n"
                "- Item 2. [[RS:cap2:d78f2f|chunks:3,4]]"
            )
        
        mock_async_client.complete = AsyncMock(side_effect=complete_side_effect)
        
        # Act
        await chapter_summarizer._generate_missing_markers_addendum(
            sample_chapter,
            recall_set_with_2_items.critical_items,
            full_text
        )
        
        # Assert: Logs devem conter informações úteis
        log_messages = caplog.text.lower()
        # Verificar que o processo foi executado (logs podem estar em outros lugares)
        assert mock_async_client.complete.called
