"""
Gate Z9.0 - Testes de schema da API (campos opcionais).

Prova que SummarizeResponse aceita coverage_report e addendum_metrics
como opcionais sem quebrar compatibilidade.
"""

import pytest
from src.api.schemas import SummarizeResponse


class TestAPISchemaGateZ9:
    """Testes para validar campos opcionais no SummarizeResponse."""

    def test_response_without_coverage_report(self):
        """
        Teste 1: Resposta sem coverage_report deve ser válida (compatibilidade retroativa).
        
        Arrange: SummarizeResponse sem campos opcionais
        Act: Criar instância
        Assert: Campos opcionais são None
        """
        response = SummarizeResponse(
            session_id="test-123",
            status="PASS",
            summaries={"curto": "Resumo curto"}
        )
        assert response.coverage_report is None
        assert response.addendum_metrics is None
        assert response.session_id == "test-123"
        assert response.summaries == {"curto": "Resumo curto"}

    def test_response_with_coverage_report(self):
        """
        Teste 2: Resposta com coverage_report deve ser válida.
        
        Arrange: SummarizeResponse com coverage_report
        Act: Criar instância
        Assert: coverage_report é preservado
        """
        coverage_data = {
            "overall_coverage_percentage": 100.0,
            "passed": True,
            "chapters": []
        }
        response = SummarizeResponse(
            session_id="test-123",
            status="PASS",
            summaries={"curto": "Resumo curto"},
            coverage_report=coverage_data
        )
        assert response.coverage_report == coverage_data
        assert response.addendum_metrics is None

    def test_response_with_null_coverage_report(self):
        """
        Teste 3: Resposta com coverage_report=None deve ser válida.
        
        Arrange: SummarizeResponse com coverage_report explicitamente None
        Act: Criar instância
        Assert: coverage_report é None
        """
        response = SummarizeResponse(
            session_id="test-123",
            status="PASS",
            summaries={"curto": "Resumo curto"},
            coverage_report=None
        )
        assert response.coverage_report is None

    def test_response_with_addendum_metrics(self):
        """
        Teste 4: Resposta com addendum_metrics deve ser válida.
        
        Arrange: SummarizeResponse com addendum_metrics
        Act: Criar instância
        Assert: addendum_metrics é preservado
        """
        addendum_data = {
            "chapters_using_addendum": 2,
            "total_addendums_used": 2,
            "avg_addendums_per_chapter": 0.18
        }
        response = SummarizeResponse(
            session_id="test-123",
            status="PASS",
            summaries={"curto": "Resumo curto"},
            addendum_metrics=addendum_data
        )
        assert response.addendum_metrics == addendum_data
        assert response.coverage_report is None

    def test_response_with_both_optional_fields(self):
        """
        Teste 5: Resposta com ambos os campos opcionais deve ser válida.
        
        Arrange: SummarizeResponse com coverage_report e addendum_metrics
        Act: Criar instância
        Assert: Ambos os campos são preservados
        """
        coverage_data = {
            "overall_coverage_percentage": 100.0,
            "passed": True,
            "summary": {
                "chapters_using_addendum": 2,
                "total_addendums_used": 2
            }
        }
        addendum_data = {
            "chapters_using_addendum": 2,
            "total_addendums_used": 2,
            "avg_addendums_per_chapter": 0.18
        }
        response = SummarizeResponse(
            session_id="test-123",
            status="PASS",
            summaries={"curto": "Resumo curto"},
            coverage_report=coverage_data,
            addendum_metrics=addendum_data
        )
        assert response.coverage_report == coverage_data
        assert response.addendum_metrics == addendum_data

    def test_response_serialization_with_optional_fields(self):
        """
        Teste 6: Serialização JSON deve incluir campos opcionais quando presentes.
        
        Arrange: SummarizeResponse com campos opcionais
        Act: Serializar para dict
        Assert: Campos opcionais aparecem no dict
        """
        coverage_data = {"overall_coverage_percentage": 100.0}
        addendum_data = {"chapters_using_addendum": 2}
        
        response = SummarizeResponse(
            session_id="test-123",
            status="PASS",
            summaries={"curto": "Resumo curto"},
            coverage_report=coverage_data,
            addendum_metrics=addendum_data
        )
        
        # Serializar usando model_dump() (Pydantic v2) ou dict() (Pydantic v1)
        if hasattr(response, 'model_dump'):
            response_dict = response.model_dump()
        elif hasattr(response, 'dict'):
            response_dict = response.dict()
        else:
            # Fallback: converter manualmente
            response_dict = {
                "session_id": response.session_id,
                "summaries": response.summaries,
                "coverage_report": response.coverage_report,
                "addendum_metrics": response.addendum_metrics
            }
        
        assert "coverage_report" in response_dict
        assert "addendum_metrics" in response_dict
        assert response_dict["coverage_report"] == coverage_data
        assert response_dict["addendum_metrics"] == addendum_data
