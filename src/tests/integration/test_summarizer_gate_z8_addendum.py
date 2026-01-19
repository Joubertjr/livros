"""
Gate Z8.1 - Teste de Addendum Incremental

Valida que o sistema gera addendum para itens faltantes e fecha gap de cobertura.
"""

import pytest
import tempfile
from pathlib import Path
from unittest.mock import patch, AsyncMock, MagicMock
import sys

# Mock do módulo summarizer antes de importar
mock_summarizer_module = MagicMock()
mock_async_client = AsyncMock()
mock_summarizer_module.AsyncOpenAIClient = MagicMock(return_value=mock_async_client)
mock_summarizer_module.SummarySpecs = MagicMock()
mock_summarizer_module.SummarySpecs.BASE_SYSTEM_MESSAGE = "You are a helpful assistant."

sys.modules['summarizer'] = mock_summarizer_module

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from src.summarizer_robust import BookSummarizerRobust
from src.recall_set import RecallSet, RecallSetItem, CriticalityReason


class TestSummarizerGateZ8Addendum:
    """Testes para addendum incremental (Estratégia A)."""

    @pytest.fixture
    def temp_evidencias_dir(self):
        """Fixture: Diretório temporário para evidências."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_text(self):
        """Fixture: Texto de exemplo com capítulo."""
        return """# Capítulo 1: Introduction

Este é o primeiro capítulo do livro. A dopamina é um neurotransmissor importante que regula o prazer e a motivação.
O sistema de recompensa do cérebro depende da dopamina para funcionar corretamente.
""" + ("Texto adicional. " * 100)

    @pytest.fixture
    def recall_set_with_3_items(self):
        """Fixture: Recall Set com 3 itens críticos."""
        # Usar generate_item_id para gerar item_ids determinísticos
        from src.recall_set import generate_item_id
        
        item1_id = generate_item_id('A dopamina é importante', '1')
        item2_id = generate_item_id('O sistema de recompensa depende da dopamina', '1')
        item3_id = generate_item_id('O cérebro funciona com neurotransmissores', '1')
        
        return RecallSet(
            chapter_number="1",
            critical_items=[
                RecallSetItem(
                    item_id=item1_id,
                    content='A dopamina é importante',
                    criticality='critical',
                    criticality_reason=CriticalityReason.MULTI_CHUNK,
                    source_chunks=[0, 1],
                    frequency=2
                ),
                RecallSetItem(
                    item_id=item2_id,
                    content='O sistema de recompensa depende da dopamina',
                    criticality='critical',
                    criticality_reason=CriticalityReason.MULTI_CHUNK,
                    source_chunks=[1, 2],
                    frequency=2
                ),
                RecallSetItem(
                    item_id=item3_id,
                    content='O cérebro funciona com neurotransmissores',
                    criticality='critical',
                    criticality_reason=CriticalityReason.MULTI_CHUNK,
                    source_chunks=[0, 2],
                    frequency=2
                )
            ],
            supporting_items=[]
        )

    @pytest.mark.asyncio
    async def test_addendum_closes_coverage_gap(self, temp_evidencias_dir, sample_text, recall_set_with_3_items):
        """
        Teste: Resumo deliberadamente faltando 2 itens → addendum deve fechar gap.
        
        Arrange: Mock que retorna resumo sem 2 marcadores
        Act: Pipeline deve gerar addendum
        Assert: Auditor deve passar após addendum
        """
        # Arrange
        # Usar os item_ids do recall_set_with_3_items
        item1_id = recall_set_with_3_items.critical_items[0].item_id
        item2_id = recall_set_with_3_items.critical_items[1].item_id
        item3_id = recall_set_with_3_items.critical_items[2].item_id
        
        item1_hash = item1_id.split(':')[-1]
        item2_hash = item2_id.split(':')[-1]
        item3_hash = item3_id.split(':')[-1]
        
        # Mock resumo que só tem 1 dos 3 marcadores (faltam 2)
        mock_summary_missing_2 = f"""RESUMO:
A dopamina é um neurotransmissor importante que regula o prazer. [[RS:cap1:{item1_hash}|chunks:0,1]]

Este capítulo discute a importância da dopamina no cérebro."""

        # Mock addendum que adiciona os 2 faltantes
        mock_addendum = f"""- O sistema de recompensa depende da dopamina para funcionar. [[RS:cap1:{item2_hash}|chunks:1,2]]
- O cérebro funciona com neurotransmissores essenciais. [[RS:cap1:{item3_hash}|chunks:0,2]]"""

        # Mock extraction
        mock_extraction = '{"concepts": ["dopamina"], "ideas": ["A dopamina é importante"], "examples": []}'

        # Função side_effect para mock_complete
        call_count = [0]
        def complete_side_effect(*args, **kwargs):
            call_count[0] += 1
            prompt = kwargs.get('user_message', '') or (args[0] if args else '')
            p = (prompt or "").lower()
            
            # Extração
            if "extraction" in p or "json" in p or "concepts" in p:
                return mock_extraction
            
            # Addendum (chamada após resumo falhar) - detectar por "bullets" ou "exatamente"
            if "bullets" in p or "exatamente" in p or ("gere" in p and "bullets" in p):
                return mock_addendum
            
            # Resumo (todas as outras chamadas de resumo)
            return mock_summary_missing_2

        # Mock generate_recall_set para retornar recall_set conhecido
        # IMPORTANTE: Patch na origem (src.recall_set.generate_recall_set)
        # E também no módulo summarizer_robust que usa getattr
        import src.recall_set
        import src.summarizer_robust
        
        # Patch em ambos os lugares para garantir interceptação
        with patch('src.recall_set.generate_recall_set', return_value=recall_set_with_3_items), \
             patch.object(src.summarizer_robust, '_generate_recall_set', return_value=recall_set_with_3_items):
            from src.summarizer_robust import BookSummarizerRobust
            summarizer = BookSummarizerRobust(evidencias_dir=str(temp_evidencias_dir))
            
            with patch.object(summarizer.chapter_summarizer.client, 'complete', side_effect=complete_side_effect) as mock_complete:
                # Act
                result = await summarizer.summarize_robust(sample_text)
                
                # Assert - Pipeline executou
                assert result is not None
                
                # Assert - Mock foi chamado (resumo + addendum)
                assert mock_complete.called, "Mock de complete deveria ter sido chamado"
                # Deve ter chamado: extrações + resumo + addendum
                assert mock_complete.call_count >= 3, f"Esperado pelo menos 3 chamadas (extrações + resumo + addendum), recebido: {mock_complete.call_count}"
                
                # Assert - Evidências geradas
                coverage_report_path = temp_evidencias_dir / "coverage_report.json"
                assert coverage_report_path.exists(), "coverage_report.json deve ser gerado"
                
                # Assert - Coverage report tem coverage 100%
                import json
                with open(coverage_report_path, 'r') as f:
                    report_data = json.load(f)
                
                assert report_data['overall_coverage_percentage'] == 100.0, \
                    f"Coverage deve ser 100%, encontrado: {report_data['overall_coverage_percentage']}"
                assert report_data['passed'] is True, "Quality Gate deve ter passado"
                
                # Assert - Nenhum missing_critical_item_ids
                chapters = report_data.get('chapters', [])
                for ch in chapters:
                    missing = ch.get('recall_set', {}).get('missing_critical_item_ids', [])
                    assert len(missing) == 0, f"Capítulo {ch.get('chapter_number')} não deve ter missing_critical_item_ids, encontrado: {missing}"
