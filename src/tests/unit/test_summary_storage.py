"""
Testes unitários para módulo de persistência de resumos.

Gate Z10: TDD-first e Clean Code enforced.
"""
import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

import sys
from pathlib import Path
# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.storage.summary_storage import SummaryStorageManager
from src.schemas.summary_storage import SummaryStorage, FeedbackEntry, PipelineType


@pytest.fixture
def temp_storage_dir():
    """Cria diretório temporário para testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def storage_manager(temp_storage_dir):
    """Cria instância do gerenciador de persistência."""
    return SummaryStorageManager(storage_dir=temp_storage_dir)


@pytest.fixture
def sample_summary():
    """Cria resumo de exemplo para testes."""
    return SummaryStorage(
        summary_id=str(uuid4()),
        title="Resumo de Teste",
        created_at=datetime.now(),
        pipeline_type=PipelineType.ROBUST,
        input_text="Texto de entrada para teste",
        summary="Resumo completo de teste",
        total_words_input=100,
        total_words_output=50,
        processing_time=1.5
    )


class TestSummaryStorageManager:
    """Testes para SummaryStorageManager."""
    
    def test_save_summary_creates_file(self, storage_manager, sample_summary):
        """Testa que salvar resumo cria arquivo JSON."""
        saved_path = storage_manager.save_summary(sample_summary)
        
        assert Path(saved_path).exists()
        assert saved_path.endswith(f"{sample_summary.summary_id}.json")
    
    def test_save_summary_generates_id_if_missing(self, storage_manager):
        """Testa que ID é gerado automaticamente se não fornecido."""
        summary = SummaryStorage(
            summary_id="",  # ID vazio para forçar geração
            created_at=datetime.now(),
            pipeline_type=PipelineType.ROBUST,
            summary="Teste"
        )
        
        # summary_id vazio deve ser tratado como None
        original_id = summary.summary_id
        saved_path = storage_manager.save_summary(summary)
        
        # Verificar que ID foi gerado
        assert summary.summary_id != original_id
        assert summary.summary_id is not None
        assert len(summary.summary_id) > 0
        assert Path(saved_path).exists()
    
    def test_load_summary_returns_correct_data(self, storage_manager, sample_summary):
        """Testa que carregar resumo retorna dados corretos."""
        storage_manager.save_summary(sample_summary)
        
        loaded = storage_manager.load_summary(sample_summary.summary_id)
        
        assert loaded is not None
        assert loaded.summary_id == sample_summary.summary_id
        assert loaded.title == sample_summary.title
        assert loaded.pipeline_type == sample_summary.pipeline_type
        assert loaded.total_words_input == sample_summary.total_words_input
    
    def test_load_summary_returns_none_if_not_found(self, storage_manager):
        """Testa que carregar resumo inexistente retorna None."""
        loaded = storage_manager.load_summary("nonexistent-id")
        
        assert loaded is None
    
    def test_list_summaries_returns_all(self, storage_manager, sample_summary):
        """Testa que listar resumos retorna todos os salvos."""
        storage_manager.save_summary(sample_summary)
        
        # Criar segundo resumo
        summary2 = SummaryStorage(
            summary_id=str(uuid4()),
            created_at=datetime.now(),
            pipeline_type=PipelineType.ROBUST,
            summary="Segundo resumo"
        )
        storage_manager.save_summary(summary2)
        
        summaries = storage_manager.list_summaries()
        
        assert len(summaries) == 2
        summary_ids = [s.summary_id for s in summaries]
        assert sample_summary.summary_id in summary_ids
        assert summary2.summary_id in summary_ids
    
    def test_list_summaries_filters_by_pipeline_type(self, storage_manager):
        """Testa que listar resumos filtra por tipo de pipeline."""
        # Criar resumos com diferentes tipos
        robust = SummaryStorage(
            summary_id=str(uuid4()),
            created_at=datetime.now(),
            pipeline_type=PipelineType.ROBUST,
            summary="Robust"
        )
        standard = SummaryStorage(
            summary_id=str(uuid4()),
            created_at=datetime.now(),
            pipeline_type=PipelineType.STANDARD,
            summary="Standard"
        )
        
        storage_manager.save_summary(robust)
        storage_manager.save_summary(standard)
        
        # Filtrar apenas robust
        robust_only = storage_manager.list_summaries(pipeline_type=PipelineType.ROBUST)
        
        assert len(robust_only) == 1
        assert robust_only[0].pipeline_type == PipelineType.ROBUST
    
    def test_list_summaries_respects_limit(self, storage_manager):
        """Testa que listar resumos respeita limite."""
        # Criar 5 resumos
        for i in range(5):
            summary = SummaryStorage(
                summary_id=str(uuid4()),
                created_at=datetime.now(),
                pipeline_type=PipelineType.ROBUST,
                summary=f"Resumo {i}"
            )
            storage_manager.save_summary(summary)
        
        limited = storage_manager.list_summaries(limit=3)
        
        assert len(limited) == 3
    
    def test_list_summaries_respects_offset(self, storage_manager):
        """Testa que listar resumos respeita offset."""
        # Criar 5 resumos
        for i in range(5):
            summary = SummaryStorage(
                summary_id=str(uuid4()),
                created_at=datetime.now(),
                pipeline_type=PipelineType.ROBUST,
                summary=f"Resumo {i}"
            )
            storage_manager.save_summary(summary)
        
        all_summaries = storage_manager.list_summaries()
        offset_summaries = storage_manager.list_summaries(offset=2)
        
        assert len(offset_summaries) == len(all_summaries) - 2
        assert offset_summaries[0].summary_id != all_summaries[0].summary_id


class TestFeedbackStorage:
    """Testes para persistência de feedback."""
    
    def test_save_feedback_creates_file(self, storage_manager, sample_summary):
        """Testa que salvar feedback cria arquivo JSON."""
        storage_manager.save_summary(sample_summary)
        
        feedback = FeedbackEntry(
            feedback_id=str(uuid4()),
            summary_id=sample_summary.summary_id,
            feedback_type="sugestão",
            message="Feedback de teste",
            created_at=datetime.now()
        )
        
        saved_path = storage_manager.save_feedback(feedback)
        
        assert Path(saved_path).exists()
        assert saved_path.endswith(f"{feedback.feedback_id}.json")
    
    def test_load_feedback_returns_all_for_summary(self, storage_manager, sample_summary):
        """Testa que carregar feedback retorna todos de um resumo."""
        storage_manager.save_summary(sample_summary)
        
        # Criar múltiplos feedbacks
        feedback1 = FeedbackEntry(
            feedback_id=str(uuid4()),
            summary_id=sample_summary.summary_id,
            feedback_type="dúvida",
            message="Primeiro feedback",
            created_at=datetime.now()
        )
        feedback2 = FeedbackEntry(
            feedback_id=str(uuid4()),
            summary_id=sample_summary.summary_id,
            feedback_type="sugestão",
            message="Segundo feedback",
            created_at=datetime.now()
        )
        
        storage_manager.save_feedback(feedback1)
        storage_manager.save_feedback(feedback2)
        
        loaded = storage_manager.load_feedback(sample_summary.summary_id)
        
        assert len(loaded) == 2
        feedback_ids = [f.feedback_id for f in loaded]
        assert feedback1.feedback_id in feedback_ids
        assert feedback2.feedback_id in feedback_ids
    
    def test_load_feedback_returns_empty_if_none(self, storage_manager, sample_summary):
        """Testa que carregar feedback de resumo sem feedback retorna lista vazia."""
        storage_manager.save_summary(sample_summary)
        
        loaded = storage_manager.load_feedback(sample_summary.summary_id)
        
        assert loaded == []
    
    def test_load_feedback_returns_empty_for_nonexistent_summary(self, storage_manager):
        """Testa que carregar feedback de resumo inexistente retorna lista vazia."""
        loaded = storage_manager.load_feedback("nonexistent-id")
        
        assert loaded == []
