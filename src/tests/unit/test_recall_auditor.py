"""
Gate Z2 - Testes unitários para RecallAuditor.

ENDFIRST: Auditoria determinística anti-fraude usando apenas regex e validações.
"""

import pytest
from src.recall_auditor import RecallAuditor, AuditResult


class TestRecallAuditor:
    """Testes para auditoria determinística de marcadores."""

    def setup_method(self):
        """Setup antes de cada teste."""
        self.auditor = RecallAuditor()

    def test_fails_when_marker_missing(self):
        """
        Teste 1: Deve falhar quando marcador está faltando.
        
        Arrange: Resumo sem marcador para item crítico
        Act: Auditar resumo
        Assert: Deve retornar passed=False com missing_markers preenchido
        """
        # Arrange
        summary_text = "Este resumo não tem marcadores. A dopamina é importante."
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is False
        assert len(result.missing_markers) > 0
        assert 'RS:cap1:9f3a1c' in result.missing_markers
        assert len(result.errors) > 0

    def test_fails_when_chunks_empty(self):
        """
        Teste 2: Deve falhar quando marcador tem chunks vazios.
        
        Arrange: Marcador com chunks: vazio ou sem chunks válidos
        Act: Auditar resumo
        Assert: Deve retornar passed=False com invalid_chunks preenchido
        """
        # Arrange - Marcador sem chunks
        summary_text = "A dopamina é importante. [[RS:cap1:9f3a1c|chunks:]]"
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is False
        assert len(result.invalid_chunks) > 0
        assert any('RS:cap1:9f3a1c' in invalid for invalid in result.invalid_chunks)
        assert len(result.errors) > 0

    def test_fails_when_chunk_inexistent(self):
        """
        Teste 3: Deve falhar quando marcador aponta para chunk inexistente.
        
        Arrange: Marcador com chunk que não está em source_chunks
        Act: Auditar resumo
        Assert: Deve retornar passed=False com invalid_chunks preenchido
        """
        # Arrange - Marcador com chunk 99 que não está em source_chunks [2, 4]
        summary_text = "A dopamina é importante. [[RS:cap1:9f3a1c|chunks:99]]"
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is False
        assert len(result.invalid_chunks) > 0
        assert any('RS:cap1:9f3a1c' in invalid and '99' in invalid for invalid in result.invalid_chunks)
        assert len(result.errors) > 0

    def test_passes_when_marker_valid(self):
        """
        Teste 4: Deve passar quando marcador é válido.
        
        Arrange: Marcador válido com chunks corretos
        Act: Auditar resumo
        Assert: Deve retornar passed=True
        """
        # Arrange
        summary_text = "A dopamina é importante. [[RS:cap1:9f3a1c|chunks:2,4]]"
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is True
        assert len(result.missing_markers) == 0
        assert len(result.invalid_chunks) == 0
        assert len(result.invented_markers) == 0
        assert len(result.errors) == 0

    def test_fails_when_invented_item_id(self):
        """
        Teste 5: Deve falhar quando marcador tem item_id inventado.
        
        Arrange: Marcador com item_id que não existe no Recall Set
        Act: Auditar resumo
        Assert: Deve retornar passed=False com invented_markers preenchido
        """
        # Arrange - Marcador com item_id que não existe
        summary_text = "A dopamina é importante. [[RS:cap1:abcdef|chunks:2,4]]"
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is False
        assert len(result.invented_markers) > 0
        assert 'RS:cap1:abcdef' in result.invented_markers
        assert len(result.errors) > 0

    def test_passes_with_multiple_markers(self):
        """
        Teste 6: Deve passar com múltiplos marcadores válidos.
        
        Arrange: Resumo com múltiplos marcadores válidos
        Act: Auditar resumo
        Assert: Deve retornar passed=True
        """
        # Arrange
        summary_text = (
            "A dopamina é um neurotransmissor. [[RS:cap1:9f3a1c|chunks:2,4]] "
            "Ela causa prazer. [[RS:cap1:a2b3c4|chunks:1,3,5]]"
        )
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                },
                {
                    'item_id': 'RS:cap1:a2b3c4',
                    'source_chunks': [1, 3, 5]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is True
        assert len(result.missing_markers) == 0
        assert len(result.invalid_chunks) == 0

    def test_fails_with_partial_chunks_invalid(self):
        """
        Teste 7: Deve falhar quando alguns chunks são válidos mas outros não.
        
        Arrange: Marcador com chunks mistos (alguns válidos, outros não)
        Act: Auditar resumo
        Assert: Deve retornar passed=False
        """
        # Arrange - Marcador com chunk 2 válido e chunk 99 inválido
        summary_text = "A dopamina é importante. [[RS:cap1:9f3a1c|chunks:2,99]]"
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        assert result.passed is False
        assert len(result.invalid_chunks) > 0
        assert any('99' in invalid for invalid in result.invalid_chunks)

    def test_fails_when_wrong_chapter_number(self):
        """
        Teste 8: Deve falhar quando marcador aponta para capítulo errado.
        
        Arrange: Marcador com número de capítulo diferente do esperado
        Act: Auditar resumo
        Assert: Deve retornar passed=False com erro
        """
        # Arrange - Marcador diz capítulo 2 mas esperamos capítulo 1
        summary_text = "A dopamina é importante. [[RS:cap2:9f3a1c|chunks:2,4]]"
        recall_set = {
            'critical_items': [
                {
                    'item_id': 'RS:cap1:9f3a1c',
                    'source_chunks': [2, 4]
                }
            ]
        }
        
        # Act
        result = self.auditor.audit_summary(summary_text, recall_set, "1")
        
        # Assert
        # Deve falhar porque item_id não vai ser encontrado (cap2 vs cap1)
        # ou porque número do capítulo está errado
        assert result.passed is False
        assert len(result.errors) > 0
