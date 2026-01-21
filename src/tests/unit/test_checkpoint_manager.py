"""
Testes unitários para CheckpointManager.

Gate Z10: TDD-first - Testes escritos ANTES da implementação.
Regra Canônica: "Teste primeiro, código depois. Sem exceção."

RED: Testes falham porque código não existe ou está incompleto
GREEN: Implementação mínima para passar
REFACTOR: Melhorar código mantendo testes passando
"""
import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.storage.checkpoint_manager import CheckpointManager, CheckpointData


@pytest.fixture
def temp_checkpoints_dir():
    """Cria diretório temporário para testes de checkpoints."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def checkpoint_manager(temp_checkpoints_dir):
    """Cria instância do CheckpointManager com diretório temporário."""
    return CheckpointManager(checkpoints_dir=temp_checkpoints_dir)


@pytest.fixture
def sample_chapter_summary():
    """Cria ChapterSummary de exemplo conforme F1."""
    return {
        'numero': '1',
        'titulo': 'Capítulo 1',
        'palavras': 5000,
        'palavras_resumo': 400,
        'paginas': [1, 2, 3],
        'resumo': 'Resumo completo do capítulo 1 com 300-500 palavras.',
        'pontos_chave': ['Ponto 1', 'Ponto 2', 'Ponto 3'],
        'citacoes': ['Citação 1', 'Citação 2'],
        'exemplos': ['Exemplo 1', 'Exemplo 2']
    }


@pytest.fixture
def sample_coverage_report():
    """Cria CoverageReport parcial de exemplo conforme F1."""
    return {
        'chapter_number': '1',
        'chapter_title': 'Capítulo 1',
        'total_chunks': 10,
        'processed_chunks': 10,
        'chunk_coverage_percentage': 100.0,
        'recall_set': {
            'critical_items': [],
            'supporting_items': []
        },
        'audit_result': {
            'passed': True,
            'regeneration_count': 0,
            'addendum_count': 0,
            'missing_markers': [],
            'invalid_chunks': []
        }
    }


@pytest.fixture
def sample_metadata():
    """Cria metadados de processamento de exemplo conforme F1."""
    return {
        'session_id': str(uuid4()),
        'timestamp_inicio': datetime.now().isoformat(),
        'timestamp_ultimo_checkpoint': datetime.now().isoformat(),
        'capitulos_processados': ['1'],
        'chunks_processados_por_capitulo': {'1': 10},
        'total_chunks_por_capitulo': {'1': 10}
    }


@pytest.fixture
def valid_checkpoint_data(sample_chapter_summary, sample_coverage_report, sample_metadata):
    """Cria dados de checkpoint válidos conforme F3."""
    return {
        'session_id': sample_metadata['session_id'],
        'chapter_number': '1',
        'chapter_summary': sample_chapter_summary,
        'coverage_report': sample_coverage_report,
        'metadata': sample_metadata
    }


class TestCheckpointManagerSave:
    """Testes para salvar checkpoints."""
    
    def test_save_checkpoint_creates_file(
        self,
        checkpoint_manager,
        valid_checkpoint_data
    ):
        """Testa que salvar checkpoint cria arquivo JSON."""
        # RED: Teste falha se método não existe
        # GREEN: Implementação mínima para passar
        saved_path = checkpoint_manager.save_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number'],
            chapter_summary=valid_checkpoint_data['chapter_summary'],
            coverage_report=valid_checkpoint_data['coverage_report'],
            metadata=valid_checkpoint_data['metadata']
        )
        
        # Verificar que arquivo foi criado
        assert Path(saved_path).exists()
        assert saved_path.endswith(f"{valid_checkpoint_data['session_id']}_checkpoint_1.json")
    
    def test_save_checkpoint_atomic_write(
        self,
        checkpoint_manager,
        valid_checkpoint_data
    ):
        """Testa que salvamento é atômico (arquivo temporário + renomeação)."""
        saved_path = checkpoint_manager.save_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number'],
            chapter_summary=valid_checkpoint_data['chapter_summary'],
            coverage_report=valid_checkpoint_data['coverage_report'],
            metadata=valid_checkpoint_data['metadata']
        )
        
        # Verificar que arquivo final existe
        assert Path(saved_path).exists()
        
        # Verificar que arquivo temporário não existe
        temp_path = Path(saved_path).with_suffix('.tmp')
        assert not temp_path.exists()
    
    def test_save_checkpoint_contains_all_components(
        self,
        checkpoint_manager,
        valid_checkpoint_data
    ):
        """Testa que checkpoint salvo contém todos os componentes (F3)."""
        saved_path = checkpoint_manager.save_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number'],
            chapter_summary=valid_checkpoint_data['chapter_summary'],
            coverage_report=valid_checkpoint_data['coverage_report'],
            metadata=valid_checkpoint_data['metadata']
        )
        
        # Carregar e verificar estrutura
        with open(saved_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verificar componentes obrigatórios conforme F3
        assert 'session_id' in data
        assert 'chapter_number' in data
        assert 'chapter_summary' in data
        assert 'coverage_report' in data
        assert 'metadata' in data
        assert 'timestamp_checkpoint' in data


class TestCheckpointManagerLoad:
    """Testes para carregar checkpoints."""
    
    def test_load_checkpoint_returns_data(
        self,
        checkpoint_manager,
        valid_checkpoint_data
    ):
        """Testa que carregar checkpoint retorna CheckpointData."""
        # Salvar checkpoint primeiro
        checkpoint_manager.save_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number'],
            chapter_summary=valid_checkpoint_data['chapter_summary'],
            coverage_report=valid_checkpoint_data['coverage_report'],
            metadata=valid_checkpoint_data['metadata']
        )
        
        # Carregar checkpoint
        loaded = checkpoint_manager.load_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number']
        )
        
        assert loaded is not None
        assert isinstance(loaded, CheckpointData)
        assert loaded.session_id == valid_checkpoint_data['session_id']
        assert loaded.chapter_number == valid_checkpoint_data['chapter_number']
    
    def test_load_checkpoint_returns_none_if_not_found(
        self,
        checkpoint_manager
    ):
        """Testa que carregar checkpoint inexistente retorna None."""
        loaded = checkpoint_manager.load_checkpoint(
            session_id='inexistente',
            chapter_number='1'
        )
        
        assert loaded is None


class TestCheckpointManagerValidation:
    """Testes para validação de checkpoints conforme F3."""
    
    def test_validate_checkpoint_valid_data(
        self,
        checkpoint_manager,
        valid_checkpoint_data
    ):
        """Testa que checkpoint válido passa validação."""
        # Salvar checkpoint válido
        checkpoint_manager.save_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number'],
            chapter_summary=valid_checkpoint_data['chapter_summary'],
            coverage_report=valid_checkpoint_data['coverage_report'],
            metadata=valid_checkpoint_data['metadata']
        )
        
        # Carregar e validar
        loaded = checkpoint_manager.load_checkpoint(
            session_id=valid_checkpoint_data['session_id'],
            chapter_number=valid_checkpoint_data['chapter_number']
        )
        
        assert loaded is not None
    
    def test_validate_checkpoint_invalid_missing_chapter_summary(
        self,
        checkpoint_manager,
        sample_coverage_report,
        sample_metadata
    ):
        """Testa que checkpoint sem chapter_summary é inválido."""
        # Criar checkpoint inválido (sem chapter_summary)
        invalid_data = {
            'session_id': sample_metadata['session_id'],
            'chapter_number': '1',
            'coverage_report': sample_coverage_report,
            'metadata': sample_metadata
        }
        
        # Tentar salvar (deve falhar ou ser rejeitado)
        # Por enquanto, testamos validação direta
        is_valid = checkpoint_manager._validate_checkpoint(invalid_data)
        assert not is_valid
    
    def test_validate_checkpoint_invalid_incomplete_chapter_summary(
        self,
        checkpoint_manager,
        sample_coverage_report,
        sample_metadata
    ):
        """Testa que checkpoint com chapter_summary incompleto é inválido."""
        # Criar chapter_summary incompleto (falta 'resumo')
        incomplete_summary = {
            'numero': '1',
            'titulo': 'Capítulo 1',
            # Falta 'resumo', 'pontos_chave', etc.
        }
        
        invalid_data = {
            'session_id': sample_metadata['session_id'],
            'chapter_number': '1',
            'chapter_summary': incomplete_summary,
            'coverage_report': sample_coverage_report,
            'metadata': sample_metadata
        }
        
        is_valid = checkpoint_manager._validate_checkpoint(invalid_data)
        assert not is_valid
    
    def test_validate_checkpoint_invalid_inconsistent_session_id(
        self,
        checkpoint_manager,
        valid_checkpoint_data
    ):
        """Testa que checkpoint com session_id inconsistente é inválido."""
        # Modificar session_id no metadata para ser diferente
        valid_checkpoint_data['metadata']['session_id'] = 'diferente'
        
        is_valid = checkpoint_manager._validate_checkpoint(valid_checkpoint_data)
        assert not is_valid
    
    def test_validate_checkpoint_invalid_chapter_not_in_processed(
        self,
        checkpoint_manager,
        sample_chapter_summary,
        sample_coverage_report,
        sample_metadata
    ):
        """Testa que checkpoint com chapter_number não em capitulos_processados é inválido."""
        # Modificar metadata para não incluir chapter_number
        sample_metadata['capitulos_processados'] = []  # Lista vazia
        
        invalid_data = {
            'session_id': sample_metadata['session_id'],
            'chapter_number': '1',
            'chapter_summary': sample_chapter_summary,
            'coverage_report': sample_coverage_report,
            'metadata': sample_metadata
        }
        
        is_valid = checkpoint_manager._validate_checkpoint(invalid_data)
        assert not is_valid


class TestCheckpointManagerFindLast:
    """Testes para encontrar último checkpoint válido."""
    
    def test_find_last_valid_checkpoint_returns_most_recent(
        self,
        checkpoint_manager,
        sample_chapter_summary,
        sample_coverage_report
    ):
        """Testa que encontra último checkpoint válido (mais recente)."""
        session_id = str(uuid4())
        
        # Criar metadados para capítulo 1
        metadata_1 = {
            'session_id': session_id,
            'timestamp_inicio': datetime.now().isoformat(),
            'capitulos_processados': ['1'],
            'chunks_processados_por_capitulo': {'1': 10},
            'total_chunks_por_capitulo': {'1': 10}
        }
        
        # Salvar checkpoint 1
        checkpoint_manager.save_checkpoint(
            session_id=session_id,
            chapter_number='1',
            chapter_summary=sample_chapter_summary,
            coverage_report=sample_coverage_report,
            metadata=metadata_1
        )
        
        # Criar metadados para capítulo 2
        metadata_2 = {
            'session_id': session_id,
            'timestamp_inicio': metadata_1['timestamp_inicio'],
            'capitulos_processados': ['1', '2'],
            'chunks_processados_por_capitulo': {'1': 10, '2': 10},
            'total_chunks_por_capitulo': {'1': 10, '2': 10}
        }
        
        # Salvar checkpoint 2 (mais recente)
        checkpoint_manager.save_checkpoint(
            session_id=session_id,
            chapter_number='2',
            chapter_summary={**sample_chapter_summary, 'numero': '2', 'titulo': 'Capítulo 2'},
            coverage_report={**sample_coverage_report, 'chapter_number': '2'},
            metadata=metadata_2
        )
        
        # Encontrar último checkpoint válido
        last = checkpoint_manager.find_last_valid_checkpoint(session_id)
        
        assert last is not None
        assert last.chapter_number == '2'  # Mais recente
    
    def test_find_last_valid_checkpoint_returns_none_if_none_exist(
        self,
        checkpoint_manager
    ):
        """Testa que retorna None se nenhum checkpoint existe."""
        last = checkpoint_manager.find_last_valid_checkpoint('inexistente')
        assert last is None
    
    def test_find_last_valid_checkpoint_skips_invalid(
        self,
        checkpoint_manager,
        sample_chapter_summary,
        sample_coverage_report
    ):
        """Testa que ignora checkpoints inválidos e retorna válido mais antigo."""
        session_id = str(uuid4())
        
        # Criar checkpoint válido (capítulo 1)
        metadata_1 = {
            'session_id': session_id,
            'timestamp_inicio': datetime.now().isoformat(),
            'capitulos_processados': ['1'],
            'chunks_processados_por_capitulo': {'1': 10},
            'total_chunks_por_capitulo': {'1': 10}
        }
        
        checkpoint_manager.save_checkpoint(
            session_id=session_id,
            chapter_number='1',
            chapter_summary=sample_chapter_summary,
            coverage_report=sample_coverage_report,
            metadata=metadata_1
        )
        
        # Criar checkpoint inválido manualmente (sem chapter_summary)
        invalid_path = Path(checkpoint_manager.checkpoints_dir) / f"{session_id}_checkpoint_2.json"
        invalid_data = {
            'session_id': session_id,
            'chapter_number': '2',
            'coverage_report': sample_coverage_report,
            'metadata': {**metadata_1, 'capitulos_processados': ['1', '2']}
        }
        with open(invalid_path, 'w', encoding='utf-8') as f:
            json.dump(invalid_data, f)
        
        # Encontrar último checkpoint válido (deve ignorar inválido)
        last = checkpoint_manager.find_last_valid_checkpoint(session_id)
        
        assert last is not None
        assert last.chapter_number == '1'  # Válido mais recente


class TestCheckpointManagerGetProcessed:
    """Testes para obter capítulos processados."""
    
    def test_get_processed_chapters_returns_list(
        self,
        checkpoint_manager,
        sample_chapter_summary,
        sample_coverage_report
    ):
        """Testa que retorna lista de capítulos processados."""
        session_id = str(uuid4())
        
        # Criar metadados com múltiplos capítulos
        metadata = {
            'session_id': session_id,
            'timestamp_inicio': datetime.now().isoformat(),
            'capitulos_processados': ['1', '2', '3'],
            'chunks_processados_por_capitulo': {'1': 10, '2': 10, '3': 10},
            'total_chunks_por_capitulo': {'1': 10, '2': 10, '3': 10}
        }
        
        # Salvar checkpoint
        checkpoint_manager.save_checkpoint(
            session_id=session_id,
            chapter_number='3',
            chapter_summary={**sample_chapter_summary, 'numero': '3'},
            coverage_report={**sample_coverage_report, 'chapter_number': '3'},
            metadata=metadata
        )
        
        # Obter capítulos processados
        processed = checkpoint_manager.get_processed_chapters(session_id)
        
        assert isinstance(processed, list)
        assert '1' in processed
        assert '2' in processed
        assert '3' in processed
    
    def test_get_processed_chapters_returns_empty_if_none(
        self,
        checkpoint_manager
    ):
        """Testa que retorna lista vazia se nenhum checkpoint existe."""
        processed = checkpoint_manager.get_processed_chapters('inexistente')
        assert processed == []
