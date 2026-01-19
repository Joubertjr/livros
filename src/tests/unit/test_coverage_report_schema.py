"""
Gate Z5.2 - Testes de validação do schema do coverage_report.

ENDFIRST: Schema deve ser rígido e validar todos os campos obrigatórios.
"""

import pytest
import json
import tempfile
from pathlib import Path
from src.schemas.coverage_report import CoverageReport, RecallSetData, AuditResultData, ChapterCoverageData, SummaryData


class TestCoverageReportSchema:
    """Testes para validação rígida do schema do coverage_report."""

    @pytest.fixture
    def valid_report_dict(self):
        """Fixture: Dicionário válido de coverage report."""
        return {
            "version": "1.0",
            "generated_at": "2024-01-15T10:30:00Z",
            "overall_coverage_percentage": 100.0,
            "passed": True,
            "chapters": [
                {
                    "chapter_number": "1",
                    "chapter_title": "Introduction",
                    "total_chunks": 5,
                    "processed_chunks": 5,
                    "chunk_coverage_percentage": 100.0,
                    "recall_set": {
                        "critical_items_total": 8,
                        "critical_items_covered": 8,
                        "supporting_items_total": 15,
                        "missing_critical_item_ids": []
                    },
                    "audit_result": {
                        "passed": True,
                        "regeneration_count": 0,
                        "missing_markers": [],
                        "invalid_chunks": []
                    }
                }
            ],
            "summary": {
                "total_chapters": 1,
                "chapters_with_100_percent": 1,
                "chapters_failed": 0
            }
        }

    def test_fails_when_missing_required_field(self, valid_report_dict):
        """
        Teste 1: Deve falhar quando campo obrigatório está faltando.
        
        Arrange: Dicionário sem campo 'overall_coverage_percentage'
        Act: Tentar criar CoverageReport
        Assert: Deve levantar ValueError
        """
        # Arrange
        invalid_data = valid_report_dict.copy()
        del invalid_data['overall_coverage_percentage']
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CoverageReport.from_dict(invalid_data)
        
        assert "overall_coverage_percentage" in str(exc_info.value).lower() or "faltando" in str(exc_info.value).lower()

    def test_fails_when_wrong_type(self, valid_report_dict):
        """
        Teste 2: Deve falhar quando tipo está errado.
        
        Arrange: Dicionário com 'overall_coverage_percentage' como string
        Act: Tentar criar CoverageReport
        Assert: Deve levantar ValueError
        """
        # Arrange
        invalid_data = valid_report_dict.copy()
        invalid_data['overall_coverage_percentage'] = "100.0"  # String ao invés de número
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CoverageReport.from_dict(invalid_data)
        
        assert "overall_coverage_percentage" in str(exc_info.value).lower() and "número" in str(exc_info.value).lower()

    def test_fails_when_missing_chunks_validated(self, valid_report_dict):
        """
        Teste 3: Deve falhar quando falta campo em recall_set.
        
        Arrange: Dicionário sem 'missing_critical_item_ids' em recall_set
        Act: Tentar criar CoverageReport
        Assert: Deve levantar ValueError
        """
        # Arrange
        invalid_data = valid_report_dict.copy()
        del invalid_data['chapters'][0]['recall_set']['missing_critical_item_ids']
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CoverageReport.from_dict(invalid_data)
        
        assert "missing_critical_item_ids" in str(exc_info.value).lower() or "recall_set" in str(exc_info.value).lower()

    def test_fails_when_overall_coverage_not_100(self, valid_report_dict):
        """
        Teste 4: Deve falhar quando overall_coverage_percentage != 100.0 (no Quality Gate).
        
        Nota: Este teste valida que o Quality Gate deve rejeitar se != 100.0
        O schema em si aceita qualquer número, mas o Quality Gate valida == 100.0
        """
        # Arrange
        invalid_data = valid_report_dict.copy()
        invalid_data['overall_coverage_percentage'] = 99.0
        invalid_data['passed'] = False
        
        # Act - Schema aceita (validação de estrutura)
        report = CoverageReport.from_dict(invalid_data)
        
        # Assert - Mas Quality Gate deve rejeitar
        assert report.overall_coverage_percentage == 99.0
        assert report.passed is False
        # Quality Gate (testado em test_quality_gate_from_coverage_report.py) deve falhar

    def test_passes_with_valid_structure(self, valid_report_dict):
        """
        Teste 5: Deve passar quando estrutura está válida.
        
        Arrange: Dicionário válido
        Act: Criar CoverageReport
        Assert: Deve criar sem erros
        """
        # Act
        report = CoverageReport.from_dict(valid_report_dict)
        
        # Assert
        assert report.version == "1.0"
        assert report.overall_coverage_percentage == 100.0
        assert report.passed is True
        assert len(report.chapters) == 1
        assert report.chapters[0].chapter_number == "1"
        assert report.chapters[0].recall_set.critical_items_total == 8
        assert report.chapters[0].audit_result.passed is True

    def test_from_json_file_valid(self, valid_report_dict):
        """
        Teste 6: Deve carregar de arquivo JSON válido.
        
        Arrange: Arquivo JSON válido
        Act: Carregar com from_json_file()
        Assert: Deve criar CoverageReport sem erros
        """
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_report_dict, f)
            temp_path = f.name
        
        try:
            # Act
            report = CoverageReport.from_json_file(temp_path)
            
            # Assert
            assert report.version == "1.0"
            assert report.overall_coverage_percentage == 100.0
        finally:
            Path(temp_path).unlink()

    def test_from_json_file_invalid_json(self):
        """
        Teste 7: Deve falhar quando JSON está malformado.
        
        Arrange: Arquivo com JSON inválido
        Act: Tentar carregar
        Assert: Deve levantar json.JSONDecodeError
        """
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ inválido json }")
            temp_path = f.name
        
        try:
            # Act & Assert
            with pytest.raises(json.JSONDecodeError):
                CoverageReport.from_json_file(temp_path)
        finally:
            Path(temp_path).unlink()

    def test_to_dict_roundtrip(self, valid_report_dict):
        """
        Teste 8: to_dict() deve manter estrutura válida.
        
        Arrange: CoverageReport válido
        Act: Converter para dict e validar novamente
        Assert: Deve criar CoverageReport válido novamente
        """
        # Arrange
        report1 = CoverageReport.from_dict(valid_report_dict)
        
        # Act
        dict_data = report1.to_dict()
        report2 = CoverageReport.from_dict(dict_data)
        
        # Assert
        assert report2.version == report1.version
        assert report2.overall_coverage_percentage == report1.overall_coverage_percentage
        assert len(report2.chapters) == len(report1.chapters)

    def test_fails_when_missing_audit_result_field(self, valid_report_dict):
        """
        Teste 9: Deve falhar quando falta campo em audit_result.
        
        Arrange: Dicionário sem 'invalid_chunks' em audit_result
        Act: Tentar criar CoverageReport
        Assert: Deve levantar ValueError
        """
        # Arrange
        invalid_data = valid_report_dict.copy()
        del invalid_data['chapters'][0]['audit_result']['invalid_chunks']
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CoverageReport.from_dict(invalid_data)
        
        assert "invalid_chunks" in str(exc_info.value).lower() or "audit_result" in str(exc_info.value).lower()

    def test_fails_when_chapter_missing_field(self, valid_report_dict):
        """
        Teste 10: Deve falhar quando chapter está faltando campo obrigatório.
        
        Arrange: Dicionário sem 'total_chunks' em chapter
        Act: Tentar criar CoverageReport
        Assert: Deve levantar ValueError
        """
        # Arrange
        invalid_data = valid_report_dict.copy()
        del invalid_data['chapters'][0]['total_chunks']
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            CoverageReport.from_dict(invalid_data)
        
        assert "total_chunks" in str(exc_info.value).lower() or "chapter" in str(exc_info.value).lower()
