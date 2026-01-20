"""
Testes de integração para API de histórico de resumos.

Gate Z10: TDD-first e Clean Code enforced.
Gate Z11: END-USER SMOKE / FRONTEND.
"""
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
from uuid import uuid4

import sys
from pathlib import Path
# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from fastapi.testclient import TestClient
from src.api.app import app
from src.storage.summary_storage import SummaryStorageManager
from src.schemas.summary_storage import SummaryStorage, FeedbackEntry, PipelineType


@pytest.fixture
def temp_storage_dir():
    """Cria diretório temporário para testes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_storage_manager(temp_storage_dir, monkeypatch):
    """Mock do storage manager para usar diretório temporário."""
    manager = SummaryStorageManager(storage_dir=temp_storage_dir)
    
    # Mock da função global
    def get_mock_manager():
        return manager
    
    monkeypatch.setattr("src.api.routes.get_storage_manager", get_mock_manager)
    return manager


@pytest.fixture
def client():
    """Cria cliente de teste FastAPI."""
    return TestClient(app)


@pytest.fixture
def sample_summary(mock_storage_manager):
    """Cria e salva resumo de exemplo."""
    summary = SummaryStorage(
        summary_id=str(uuid4()),
        title="Resumo de Teste API",
        created_at=datetime.now(),
        pipeline_type=PipelineType.ROBUST,
        input_text="Texto de entrada",
        summary="Resumo completo",
        total_words_input=100,
        total_words_output=50,
        processing_time=1.5
    )
    mock_storage_manager.save_summary(summary)
    return summary


class TestAPISummaries:
    """Testes para endpoint GET /api/summaries."""
    
    def test_list_summaries_returns_empty_list_when_none(self, client, mock_storage_manager):
        """Testa que listar resumos retorna lista vazia quando não há resumos."""
        response = client.get("/api/summaries")
        
        assert response.status_code == 200
        data = response.json()
        assert data["summaries"] == []
        assert data["total"] == 0
    
    def test_list_summaries_returns_saved_summaries(self, client, sample_summary):
        """Testa que listar resumos retorna resumos salvos."""
        response = client.get("/api/summaries")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["summaries"]) == 1
        assert data["total"] == 1
        assert data["summaries"][0]["summary_id"] == sample_summary.summary_id
        assert data["summaries"][0]["title"] == sample_summary.title
    
    def test_list_summaries_filters_by_pipeline_type(self, client, mock_storage_manager):
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
        
        mock_storage_manager.save_summary(robust)
        mock_storage_manager.save_summary(standard)
        
        # Filtrar apenas robust
        response = client.get("/api/summaries?pipeline_type=robust")
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["summaries"]) == 1
        assert data["summaries"][0]["pipeline_type"] == "robust"
    
    def test_list_summaries_rejects_invalid_pipeline_type(self, client):
        """Testa que listar resumos rejeita tipo de pipeline inválido."""
        response = client.get("/api/summaries?pipeline_type=invalid")
        
        assert response.status_code == 400
        assert "inválido" in response.json()["detail"].lower()


class TestAPIGetSummary:
    """Testes para endpoint GET /api/summaries/{summary_id}."""
    
    def test_get_summary_returns_summary_details(self, client, sample_summary):
        """Testa que buscar resumo retorna detalhes completos."""
        response = client.get(f"/api/summaries/{sample_summary.summary_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["summary"]["summary_id"] == sample_summary.summary_id
        assert data["summary"]["title"] == sample_summary.title
        assert "feedback" in data
    
    def test_get_summary_returns_404_if_not_found(self, client):
        """Testa que buscar resumo inexistente retorna 404."""
        response = client.get("/api/summaries/nonexistent-id")
        
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()


class TestAPIFeedback:
    """Testes para endpoint POST /api/summaries/{summary_id}/feedback."""
    
    def test_submit_feedback_creates_feedback(self, client, sample_summary, mock_storage_manager):
        """Testa que submeter feedback cria registro."""
        response = client.post(
            f"/api/summaries/{sample_summary.summary_id}/feedback",
            data={
                "feedback_type": "sugestão",
                "message": "Feedback de teste"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "feedback_id" in data
        
        # Verificar que feedback foi salvo
        feedbacks = mock_storage_manager.load_feedback(sample_summary.summary_id)
        assert len(feedbacks) == 1
        assert feedbacks[0].message == "Feedback de teste"
    
    def test_submit_feedback_rejects_invalid_type(self, client, sample_summary):
        """Testa que submeter feedback rejeita tipo inválido."""
        response = client.post(
            f"/api/summaries/{sample_summary.summary_id}/feedback",
            data={
                "feedback_type": "tipo_invalido",
                "message": "Mensagem"
            }
        )
        
        assert response.status_code == 400
        assert "inválido" in response.json()["detail"].lower()
    
    def test_submit_feedback_returns_404_if_summary_not_found(self, client):
        """Testa que submeter feedback retorna 404 se resumo não existe."""
        response = client.post(
            "/api/summaries/nonexistent-id/feedback",
            data={
                "feedback_type": "sugestão",
                "message": "Mensagem"
            }
        )
        
        assert response.status_code == 404
        assert "não encontrado" in response.json()["detail"].lower()
