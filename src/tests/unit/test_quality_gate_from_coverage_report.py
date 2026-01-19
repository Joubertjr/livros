"""
Gate Z1 - Testes unitários para validate_from_coverage_report().

ENDFIRST: Quality Gate deve ler apenas o coverage_report.json (não recalcular).
"""

import pytest
import json
import os
import tempfile
from pathlib import Path
from src.quality_gate import QualityGate


class TestQualityGateFromCoverageReport:
    """Testes para validação via coverage_report.json (fonte única)."""

    def setup_method(self):
        """Setup antes de cada teste."""
        self.quality_gate = QualityGate()
        self.test_dir = Path(__file__).parent.parent.parent / "tests" / "fixtures"

    def test_fails_when_file_missing(self):
        """
        Teste 1: Deve falhar quando arquivo não existe.
        
        Arrange: Caminho para arquivo inexistente
        Act: Chamar validate_from_coverage_report()
        Assert: Deve retornar (False, ["coverage_report.json não encontrado"])
        """
        # Arrange
        non_existent_file = "/caminho/inexistente/coverage_report.json"
        
        # Act
        passed, errors = self.quality_gate.validate_from_coverage_report(non_existent_file)
        
        # Assert
        assert passed is False
        assert len(errors) > 0
        assert any("não encontrado" in error.lower() or "não existe" in error.lower() for error in errors)

    def test_fails_when_json_invalid(self):
        """
        Teste 2: Deve falhar quando JSON está malformado.
        
        Arrange: Arquivo com JSON inválido
        Act: Chamar validate_from_coverage_report()
        Assert: Deve retornar (False, ["JSON inválido"])
        """
        # Arrange
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ inválido json }")
            temp_path = f.name
        
        try:
            # Act
            passed, errors = self.quality_gate.validate_from_coverage_report(temp_path)
            
            # Assert
            assert passed is False
            assert len(errors) > 0
            assert any("json inválido" in error.lower() or "jsondecodeerror" in error.lower() for error in errors)
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_fails_when_coverage_99_percent(self):
        """
        Teste 3: Deve falhar quando overall_coverage_percentage == 99.0.
        
        Arrange: Fixture com 99% de cobertura
        Act: Chamar validate_from_coverage_report()
        Assert: Deve retornar (False, ["Cobertura insuficiente: 99.0%"])
        """
        # Arrange
        fixture_path = self.test_dir / "coverage_report_99.json"
        
        # Act
        passed, errors = self.quality_gate.validate_from_coverage_report(str(fixture_path))
        
        # Assert
        assert passed is False
        assert len(errors) > 0
        assert any("99" in error and ("cobertura" in error.lower() or "coverage" in error.lower()) for error in errors)

    def test_fails_when_passed_false(self):
        """
        Teste 3b: Deve falhar quando passed == false (mesmo com coverage 100%).
        
        Arrange: Report com passed: false (estrutura válida do schema)
        Act: Chamar validate_from_coverage_report()
        Assert: Deve retornar (False, [mensagem sobre passed: false])
        """
        # Arrange - Estrutura válida do schema mas com passed: false
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "version": "1.0",
                "generated_at": "2024-01-15T10:30:00Z",
                "overall_coverage_percentage": 100.0,
                "passed": False,
                "chapters": [
                    {
                        "chapter_number": "1",
                        "chapter_title": "Test",
                        "total_chunks": 1,
                        "processed_chunks": 1,
                        "chunk_coverage_percentage": 100.0,
                        "recall_set": {
                            "critical_items_total": 1,
                            "critical_items_covered": 1,
                            "supporting_items_total": 0,
                            "missing_critical_item_ids": []
                        },
                        "audit_result": {
                            "passed": False,
                            "regeneration_count": 0,
                            "missing_markers": [],
                            "invalid_chunks": []
                        }
                    }
                ],
                "summary": {
                    "total_chapters": 1,
                    "chapters_with_100_percent": 0,
                    "chapters_failed": 1
                }
            }, f)
            temp_path = f.name
        
        try:
            # Act
            passed, errors = self.quality_gate.validate_from_coverage_report(temp_path)
            
            # Assert
            assert passed is False
            assert len(errors) > 0
            assert any("passed" in error.lower() and "false" in error.lower() for error in errors)
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)

    def test_passes_when_coverage_100_percent(self):
        """
        Teste 4: Deve passar quando overall_coverage_percentage == 100.0 e passed == true.
        
        Arrange: Fixture com 100% de cobertura e passed: true
        Act: Chamar validate_from_coverage_report()
        Assert: Deve retornar (True, [])
        """
        # Arrange
        fixture_path = self.test_dir / "coverage_report_100.json"
        
        # Act
        passed, errors = self.quality_gate.validate_from_coverage_report(str(fixture_path))
        
        # Assert
        assert passed is True
        assert len(errors) == 0

    def test_fails_when_missing_fields(self):
        """
        Teste 5: Deve falhar quando campos obrigatórios estão faltando (validação do schema).
        
        Arrange: JSON sem campo 'overall_coverage_percentage'
        Act: Chamar validate_from_coverage_report()
        Assert: Deve retornar (False, [mensagens sobre campos faltantes do schema])
        """
        # Arrange - Sem overall_coverage_percentage (schema deve rejeitar)
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({
                "version": "1.0",
                "generated_at": "2024-01-15T10:30:00Z",
                "passed": True,
                "chapters": [],
                "summary": {
                    "total_chapters": 0,
                    "chapters_with_100_percent": 0,
                    "chapters_failed": 0
                }
            }, f)
            temp_path = f.name
        
        try:
            # Act
            passed, errors = self.quality_gate.validate_from_coverage_report(temp_path)
            
            # Assert
            assert passed is False
            assert len(errors) > 0
            # Schema deve detectar campo faltante
            assert any("overall_coverage_percentage" in error.lower() or "schema" in error.lower() or "faltando" in error.lower() for error in errors)
        finally:
            # Cleanup
            if os.path.exists(temp_path):
                os.unlink(temp_path)
