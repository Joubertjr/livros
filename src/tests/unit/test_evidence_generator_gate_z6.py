"""
Gate Z6 - Evidence Generator (gera evidências + coverage_report.json).

ENDFIRST: Evidence Generator deve gerar:
- EVIDENCIAS/coverage_report.json (validado pelo schema)
- EVIDENCIAS/extractions_<timestamp>.json
- EVIDENCIAS/report.md

Regras:
- coverage_report.json tem estrutura válida (schema)
- Totalizadores batem: total_critical_items == total_covered
- overall_coverage_percentage == 100.0 quando PASS
"""

import pytest
import json
import tempfile
from pathlib import Path
from datetime import datetime
from src.evidence_generator_robust import EvidenceGeneratorRobust
from src.schemas.coverage_report import CoverageReport


class TestEvidenceGeneratorGateZ6:
    """Testes para Gate Z6: Evidence Generator."""

    @pytest.fixture
    def temp_evidencias_dir(self):
        """Fixture: Diretório temporário para evidências."""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    @pytest.fixture
    def sample_chapter_summaries(self):
        """Fixture: Resumos de capítulos de exemplo."""
        return [
            {
                'chapter_number': '1',
                'chapter_title': 'Introduction',
                'summary_text': 'Resumo do capítulo 1. [[RS:cap1:9f3a1c|chunks:0,1]]',
                'recall_set': {
                    'critical_items': [
                        {
                            'item_id': 'RS:cap1:9f3a1c',
                            'content': 'A dopamina é importante',
                            'source_chunks': [0, 1]
                        }
                    ]
                },
                'audit_result': {
                    'passed': True,
                    'regeneration_count': 0,
                    'missing_markers': [],
                    'invalid_chunks': []
                },
                'total_chunks': 5,
                'processed_chunks': 5
            }
        ]

    @pytest.fixture
    def sample_extractions(self):
        """Fixture: Extrações de exemplo."""
        return {
            'chapter_1': {
                'chunks': [
                    {
                        'chunk_id': 0,
                        'extraction': {
                            'concepts': ['dopamina'],
                            'ideas': ['A dopamina é importante'],
                            'examples': []
                        }
                    },
                    {
                        'chunk_id': 1,
                        'extraction': {
                            'concepts': ['dopamina'],
                            'ideas': ['A dopamina regula prazer'],
                            'examples': []
                        }
                    }
                ]
            }
        }

    def test_generates_coverage_report_json(self, temp_evidencias_dir, sample_chapter_summaries):
        """
        Teste 1: Deve gerar coverage_report.json com estrutura válida.
        
        Arrange: EvidenceGenerator com dados de capítulos
        Act: Chamar generate_robust_evidence()
        Assert: Arquivo coverage_report.json existe e passa no schema
        """
        # Arrange
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=sample_chapter_summaries,
            extractions={}
        )
        
        # Assert - Arquivo existe
        coverage_report_path = temp_evidencias_dir / "coverage_report.json"
        assert coverage_report_path.exists(), "coverage_report.json deve ser gerado"
        
        # Assert - Schema válido
        report = CoverageReport.from_json_file(str(coverage_report_path))
        assert report.version is not None
        assert report.overall_coverage_percentage is not None
        assert report.passed is not None
        assert len(report.chapters) == 1

    def test_coverage_report_has_required_fields(self, temp_evidencias_dir, sample_chapter_summaries):
        """
        Teste 2: coverage_report.json deve ter todos os campos obrigatórios.
        
        Arrange: EvidenceGenerator com dados completos
        Act: Gerar evidências
        Assert: Todos os campos obrigatórios estão presentes
        """
        # Arrange
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=sample_chapter_summaries,
            extractions={}
        )
        
        # Assert
        coverage_report_path = temp_evidencias_dir / "coverage_report.json"
        with open(coverage_report_path, 'r') as f:
            data = json.load(f)
        
        # Validar campos obrigatórios do nível raiz
        assert 'version' in data
        assert 'generated_at' in data
        assert 'overall_coverage_percentage' in data
        assert 'passed' in data
        assert 'chapters' in data
        assert 'summary' in data
        
        # Validar campos do chapter
        chapter = data['chapters'][0]
        assert 'chapter_number' in chapter
        assert 'chapter_title' in chapter
        assert 'total_chunks' in chapter
        assert 'processed_chunks' in chapter
        assert 'chunk_coverage_percentage' in chapter
        assert 'recall_set' in chapter
        assert 'audit_result' in chapter
        
        # Validar recall_set
        recall_set = chapter['recall_set']
        assert 'critical_items_total' in recall_set
        assert 'critical_items_covered' in recall_set
        assert 'supporting_items_total' in recall_set
        assert 'missing_critical_item_ids' in recall_set
        
        # Validar audit_result
        audit_result = chapter['audit_result']
        assert 'passed' in audit_result
        assert 'regeneration_count' in audit_result
        assert 'missing_markers' in audit_result
        assert 'invalid_chunks' in audit_result

    def test_generates_extractions_json(self, temp_evidencias_dir, sample_chapter_summaries, sample_extractions):
        """
        Teste 3: Deve gerar extractions_<timestamp>.json.
        
        Arrange: EvidenceGenerator com extrações
        Act: Gerar evidências
        Assert: Arquivo extractions_*.json existe
        """
        # Arrange
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=sample_chapter_summaries,
            extractions=sample_extractions
        )
        
        # Assert - Arquivo existe
        extraction_files = list(temp_evidencias_dir.glob("extractions_*.json"))
        assert len(extraction_files) > 0, "extractions_*.json deve ser gerado"
        
        # Assert - JSON válido
        with open(extraction_files[0], 'r') as f:
            data = json.load(f)
        assert isinstance(data, dict)

    def test_generates_report_md(self, temp_evidencias_dir, sample_chapter_summaries):
        """
        Teste 4: Deve gerar report.md.
        
        Arrange: EvidenceGenerator com dados
        Act: Gerar evidências
        Assert: Arquivo report.md existe
        """
        # Arrange
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=sample_chapter_summaries,
            extractions={}
        )
        
        # Assert
        report_md_path = temp_evidencias_dir / "report.md"
        assert report_md_path.exists(), "report.md deve ser gerado"
        
        # Assert - Conteúdo não vazio
        content = report_md_path.read_text(encoding='utf-8')
        assert len(content) > 0, "report.md não deve estar vazio"

    def test_totalizadores_batem(self, temp_evidencias_dir, sample_chapter_summaries):
        """
        Teste 5: Totalizadores devem bater (total_critical_items == total_covered).
        
        Arrange: EvidenceGenerator com dados onde todos os itens críticos estão cobertos
        Act: Gerar evidências
        Assert: total_critical_items == critical_items_covered
        """
        # Arrange
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=sample_chapter_summaries,
            extractions={}
        )
        
        # Assert
        coverage_report_path = temp_evidencias_dir / "coverage_report.json"
        report = CoverageReport.from_json_file(str(coverage_report_path))
        
        for chapter in report.chapters:
            assert chapter.recall_set.critical_items_total == chapter.recall_set.critical_items_covered, \
                f"Chapter {chapter.chapter_number}: total ({chapter.recall_set.critical_items_total}) != covered ({chapter.recall_set.critical_items_covered})"

    def test_overall_coverage_100_when_pass(self, temp_evidencias_dir, sample_chapter_summaries):
        """
        Teste 6: overall_coverage_percentage == 100.0 quando passed == true.
        
        Arrange: EvidenceGenerator com dados onde todos passam
        Act: Gerar evidências
        Assert: overall_coverage_percentage == 100.0 e passed == true
        """
        # Arrange
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=sample_chapter_summaries,
            extractions={}
        )
        
        # Assert
        coverage_report_path = temp_evidencias_dir / "coverage_report.json"
        report = CoverageReport.from_json_file(str(coverage_report_path))
        
        if report.passed:
            assert report.overall_coverage_percentage == 100.0, \
                f"Quando passed=True, overall_coverage deve ser 100.0, encontrado: {report.overall_coverage_percentage}"

    def test_fails_when_missing_critical_item(self, temp_evidencias_dir):
        """
        Teste 7: Deve falhar se faltar 1 item crítico (missing_critical_item_ids não vazio).
        
        Arrange: Chapter summary com item crítico faltando
        Act: Gerar evidências
        Assert: missing_critical_item_ids não está vazio e passed == false
        """
        # Arrange - Chapter com item crítico faltando
        chapter_summaries = [
            {
                'chapter_number': '1',
                'chapter_title': 'Introduction',
                'summary_text': 'Resumo sem marcadores.',
                'recall_set': {
                    'critical_items': [
                        {
                            'item_id': 'RS:cap1:9f3a1c',
                            'content': 'A dopamina é importante',
                            'source_chunks': [0, 1]
                        }
                    ]
                },
                'audit_result': {
                    'passed': False,
                    'regeneration_count': 3,
                    'missing_markers': ['RS:cap1:9f3a1c'],
                    'invalid_chunks': []
                },
                'total_chunks': 5,
                'processed_chunks': 5
            }
        ]
        
        generator = EvidenceGeneratorRobust(output_dir=str(temp_evidencias_dir))
        
        # Act
        generator.generate_robust_evidence(
            chapter_summaries=chapter_summaries,
            extractions={}
        )
        
        # Assert
        coverage_report_path = temp_evidencias_dir / "coverage_report.json"
        report = CoverageReport.from_json_file(str(coverage_report_path))
        
        chapter = report.chapters[0]
        assert len(chapter.recall_set.missing_critical_item_ids) > 0, \
            "missing_critical_item_ids deve conter item faltante"
        assert chapter.audit_result.passed is False, \
            "audit_result.passed deve ser False quando há item faltante"
        assert report.passed is False, \
            "overall passed deve ser False quando há item faltante"
