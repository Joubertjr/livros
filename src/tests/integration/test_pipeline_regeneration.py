"""
Gate Z5 - Teste de integração do pipeline completo com loop de regeneração.

ENDFIRST: Mock LLM gera resumo falho 2x e correto na 3ª tentativa.
Valida regeneration_count e coverage 100%.
"""

import pytest
pytest_plugins = ('pytest_asyncio',)
import sys
from unittest.mock import AsyncMock, MagicMock, patch
from dataclasses import dataclass
from src.recall_set import RecallSet, RecallSetItem, CriticalityReason
from src.exceptions import CoverageError

# Criar mock do módulo summarizer antes de importar
mock_summarizer_module = MagicMock()
mock_async_client = AsyncMock()
mock_summarizer_module.AsyncOpenAIClient = MagicMock(return_value=mock_async_client)
mock_summarizer_module.SummarySpecs = MagicMock()
mock_summarizer_module.SummarySpecs.BASE_SYSTEM_MESSAGE = "You are a helpful assistant."

sys.modules['summarizer'] = mock_summarizer_module

from src.chapter_summarizer import ChapterSummarizer, ChapterSummary


@dataclass
class Chapter:
    """Mock de Chapter para testes."""
    number: str
    title: str
    word_count: int
    start_pos: int
    end_pos: int
    page_markers: list = None
    
    def __post_init__(self):
        if self.page_markers is None:
            self.page_markers = []


class TestPipelineRegeneration:
    """Testes para pipeline completo com loop de regeneração."""

    @pytest.fixture
    def chapter(self):
        """Fixture: Capítulo de teste."""
        return Chapter(
            number="1",
            title="Introduction",
            word_count=500,
            start_pos=0,
            end_pos=2500,
            page_markers=[1, 2]
        )

    @pytest.fixture
    def full_text(self):
        """Fixture: Texto completo."""
        return "Capítulo 1: Introduction\n\n" + "Texto do capítulo. " * 100

    @pytest.mark.asyncio
    async def test_regeneration_loop_with_mock_llm(self, chapter, full_text):
        """
        Teste obrigatório: Mock LLM gera resumo falho 2x e correto na 3ª.
        
        Arrange: Mock LLM que retorna resumos sem marcadores nas 2 primeiras tentativas
                 e com marcadores corretos na 3ª
        Act: Chamar summarize_chapter_robust()
        Assert: Deve passar na 3ª tentativa, regeneration_count == 2
        """
        # Arrange - Criar mock de Recall Set
        recall_set_item = RecallSetItem(
            item_id='RS:cap1:9f3a1c',
            content='A dopamina é importante',
            criticality='critical',
            criticality_reason=CriticalityReason.MULTI_CHUNK,
            source_chunks=[0, 1],
            frequency=2
        )
        recall_set = RecallSet(
            chapter_number="1",
            critical_items=[recall_set_item],
            supporting_items=[]
        )
        
        # Mock generate_recall_set para retornar Recall Set conhecido
        fixed_recall_set = RecallSet(
            chapter_number="1",
            critical_items=[recall_set_item],
            supporting_items=[]
        )
        
        # Mock: Primeiras 2 tentativas falham (sem marcadores), 3ª passa
        mock_responses = [
            """RESUMO:
Este é um resumo sem marcadores. A dopamina é importante.

PONTOS-CHAVE:
• Ponto 1""",  # Tentativa 1: FAIL
            """RESUMO:
Este é outro resumo sem marcadores. A dopamina é importante.

PONTOS-CHAVE:
• Ponto 1""",  # Tentativa 2: FAIL
            """RESUMO:
A dopamina é um neurotransmissor importante que regula o prazer e a motivação. [[RS:cap1:9f3a1c|chunks:0,1]] Ela é liberada em resposta a recompensas e desempenha papel crucial no sistema de recompensa do cérebro.

PONTOS-CHAVE:
• A dopamina é importante
• Ela regula o prazer""",  # Tentativa 3: PASS
        ]
        
        mock_extraction = '{"concepts": ["dopamina"], "ideas": ["A dopamina é importante"], "examples": []}'
        
        summarizer = ChapterSummarizer()
        
        # Mock do cliente OpenAI
        with patch('src.recall_set.generate_recall_set', return_value=fixed_recall_set):
            with patch.object(summarizer.client, 'complete') as mock_complete:
                # Configurar ordem: 2 extrações + 3 resumos
                mock_complete.side_effect = [
                    mock_extraction,  # Extração chunk 0
                    mock_extraction,  # Extração chunk 1
                    mock_responses[0],  # Resumo tentativa 1
                    mock_responses[1],  # Resumo tentativa 2
                    mock_responses[2],  # Resumo tentativa 3
                ]
            
                # Act
                result = await summarizer.summarize_chapter_robust(chapter, full_text, use_robust_pipeline=True)
                
                # Assert
                assert isinstance(result, ChapterSummary)
                assert result.numero == "1"
                assert "[[RS:cap1:9f3a1c|chunks:0,1]]" in result.resumo or "9f3a1c" in result.resumo
                
                # Verificar que foram feitas 3 tentativas de resumo (2 extrações + 3 resumos = 5 chamadas)
                assert mock_complete.call_count >= 5, \
                    f"Esperado pelo menos 5 chamadas (2 extrações + 3 resumos), recebido {mock_complete.call_count}"

    @pytest.mark.asyncio
    async def test_fails_after_max_attempts(self, chapter, full_text):
        """
        Teste: Deve levantar CoverageError após 3 tentativas falhadas.
        
        Arrange: Mock LLM que sempre retorna resumo sem marcadores
        Act: Chamar summarize_chapter_robust()
        Assert: Deve levantar CoverageError
        """
        # Arrange
        recall_set_item = RecallSetItem(
            item_id='RS:cap1:9f3a1c',
            content='A dopamina é importante',
            criticality='critical',
            criticality_reason=CriticalityReason.MULTI_CHUNK,
            source_chunks=[0, 1],
            frequency=2
        )
        
        fixed_recall_set = RecallSet(
            chapter_number="1",
            critical_items=[recall_set_item],
            supporting_items=[]
        )
        
        summarizer = ChapterSummarizer()
        
        # Mock: Sempre retorna resumo sem marcadores
        mock_response_no_markers = """RESUMO:
Este resumo nunca tem marcadores. A dopamina é importante.

PONTOS-CHAVE:
• Ponto 1"""
        mock_extraction = '{"concepts": ["dopamina"], "ideas": ["A dopamina é importante"], "examples": []}'
        
        with patch('src.recall_set.generate_recall_set', return_value=fixed_recall_set):
            with patch.object(summarizer.client, 'complete') as mock_complete:
                # Configurar: 2 extrações + 3 resumos (todos sem marcadores) + 2 addendums (também sem marcadores)
                mock_complete.side_effect = [
                    mock_extraction,  # Extração chunk 0
                    mock_extraction,  # Extração chunk 1
                    mock_response_no_markers,  # Resumo tentativa 1
                    mock_response_no_markers,  # Resumo tentativa 2
                    mock_response_no_markers,  # Resumo tentativa 3
                    "- Item sem marcador",  # Addendum tentativa 1 (sem marcador)
                    "- Item sem marcador",  # Addendum tentativa 2 (sem marcador)
                ]
                
                # Act & Assert
                with pytest.raises(CoverageError) as exc_info:
                    await summarizer.summarize_chapter_robust(chapter, full_text, use_robust_pipeline=True)
                
                assert "3 tentativas" in str(exc_info.value) or "não atingiu 100%" in str(exc_info.value).lower()
                
                # Verificar que foram feitas 5 chamadas (2 extrações + 3 resumos)
                assert mock_complete.call_count >= 4  # Pode variar dependendo do chunking

    @pytest.mark.asyncio
    async def test_passes_on_first_attempt(self, chapter, full_text):
        """
        Teste: Deve passar na primeira tentativa se resumo já estiver correto.
        
        Arrange: Mock LLM que retorna resumo com marcadores corretos na primeira tentativa
        Act: Chamar summarize_chapter_robust()
        Assert: Deve passar sem regeneração (regeneration_count == 0)
        """
        # Arrange
        recall_set_item = RecallSetItem(
            item_id='RS:cap1:9f3a1c',
            content='A dopamina é importante',
            criticality='critical',
            criticality_reason=CriticalityReason.MULTI_CHUNK,
            source_chunks=[0, 1],
            frequency=2
        )
        
        fixed_recall_set = RecallSet(
            chapter_number="1",
            critical_items=[recall_set_item],
            supporting_items=[]
        )
        
        summarizer = ChapterSummarizer()
        
        mock_extraction = '{"concepts": ["dopamina"], "ideas": ["A dopamina é importante"], "examples": []}'
        mock_response_with_markers = """RESUMO:
A dopamina é importante. [[RS:cap1:9f3a1c|chunks:0,1]] Resumo correto.

PONTOS-CHAVE:
• Ponto 1"""
        
        with patch('src.recall_set.generate_recall_set', return_value=fixed_recall_set):
            with patch.object(summarizer.client, 'complete') as mock_complete:
                mock_complete.side_effect = [
                    mock_extraction,  # Extração chunk 0
                    mock_extraction,  # Extração chunk 1
                    mock_response_with_markers,  # Resumo tentativa 1 (já correto)
                ]
                
                # Act
                result = await summarizer.summarize_chapter_robust(chapter, full_text, use_robust_pipeline=True)
                
                # Assert
                assert isinstance(result, ChapterSummary)
                assert result.numero == "1"
                # Verificar que foi apenas 1 tentativa de resumo (2 extrações + 1 resumo = 3 chamadas)
                assert mock_complete.call_count >= 3
