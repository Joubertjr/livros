"""
Testes unitários para persistência de resumos com estrutura de capítulos.

Gate Z10: TDD-first - Testes escritos ANTES da implementação.
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from uuid import uuid4

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.storage.summary_storage import SummaryStorageManager
from src.schemas.summary_storage import SummaryStorage, PipelineType


@pytest.fixture
def temp_storage_dir():
    """Cria diretório temporário para testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def storage_manager(temp_storage_dir):
    """Cria storage manager com diretório temporário."""
    return SummaryStorageManager(storage_dir=temp_storage_dir)


class TestSummaryStorageWithCapitulos:
    """Testes para persistência de resumos com estrutura de capítulos."""
    
    def test_save_summary_with_capitulos_structure(self, storage_manager):
        """
        Testa que salvar resumo com estrutura 'capitulos' funciona corretamente.
        
        RED: Teste falha se schema não aceita Dict genérico
        GREEN: Schema aceita Dict genérico
        """
        summaries = {
            'estrutura': 'capitulos',
            'resumo_executivo': {
                'medio': 'Resumo executivo de teste'
            },
            'capitulos': [
                {
                    'numero': '1',
                    'titulo': 'Capítulo 1',
                    'resumo': 'Resumo do capítulo 1',
                    'palavras': 100,
                    'palavras_resumo': 50,
                    'paginas': [1, 2, 3],
                    'pontos_chave': ['Ponto 1', 'Ponto 2'],
                    'citacoes': ['Citação 1'],
                    'exemplos': ['Exemplo 1']
                }
            ]
        }
        
        summary = SummaryStorage(
            summary_id=str(uuid4()),
            title="Resumo com Capítulos",
            created_at=datetime.now(),
            pipeline_type=PipelineType.ROBUST,
            summary="Resumo completo",
            summaries=summaries,
            total_words_input=100,
            total_words_output=50
        )
        
        # Deve salvar sem erro de validação
        saved_path = storage_manager.save_summary(summary)
        
        assert Path(saved_path).exists()
        
        # Deve carregar corretamente
        loaded = storage_manager.load_summary(summary.summary_id)
        
        assert loaded is not None
        assert loaded.summaries is not None
        assert loaded.summaries['estrutura'] == 'capitulos'
        assert len(loaded.summaries['capitulos']) == 1
        assert loaded.summaries['capitulos'][0]['numero'] == '1'
        assert loaded.summaries['capitulos'][0]['pontos_chave'] == ['Ponto 1', 'Ponto 2']
    
    def test_save_summary_with_empty_capitulos(self, storage_manager):
        """Testa que salvar resumo com capítulos vazios funciona."""
        summaries = {
            'estrutura': 'capitulos',
            'resumo_executivo': {
                'medio': 'Resumo executivo'
            },
            'capitulos': []
        }
        
        summary = SummaryStorage(
            summary_id=str(uuid4()),
            created_at=datetime.now(),
            pipeline_type=PipelineType.ROBUST,
            summaries=summaries
        )
        
        saved_path = storage_manager.save_summary(summary)
        assert Path(saved_path).exists()
        
        loaded = storage_manager.load_summary(summary.summary_id)
        assert loaded.summaries['capitulos'] == []
    
    def test_save_summary_with_multiple_capitulos(self, storage_manager):
        """Testa que salvar resumo com múltiplos capítulos funciona."""
        summaries = {
            'estrutura': 'capitulos',
            'resumo_executivo': {
                'medio': 'Resumo executivo'
            },
            'capitulos': [
                {
                    'numero': '1',
                    'titulo': 'Capítulo 1',
                    'resumo': 'Resumo 1',
                    'palavras': 100,
                    'palavras_resumo': 50,
                    'paginas': [1],
                    'pontos_chave': [],
                    'citacoes': [],
                    'exemplos': []
                },
                {
                    'numero': '2',
                    'titulo': 'Capítulo 2',
                    'resumo': 'Resumo 2',
                    'palavras': 200,
                    'palavras_resumo': 100,
                    'paginas': [2],
                    'pontos_chave': [],
                    'citacoes': [],
                    'exemplos': []
                }
            ]
        }
        
        summary = SummaryStorage(
            summary_id=str(uuid4()),
            created_at=datetime.now(),
            pipeline_type=PipelineType.ROBUST,
            summaries=summaries
        )
        
        saved_path = storage_manager.save_summary(summary)
        assert Path(saved_path).exists()
        
        loaded = storage_manager.load_summary(summary.summary_id)
        assert len(loaded.summaries['capitulos']) == 2
        assert loaded.summaries['capitulos'][0]['numero'] == '1'
        assert loaded.summaries['capitulos'][1]['numero'] == '2'
