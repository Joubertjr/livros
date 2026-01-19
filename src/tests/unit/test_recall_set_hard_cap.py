"""
Gate Z4 - Teste de hard cap 12 em Recall Set.

ENDFIRST: Recall Set deve ter no máximo 12 itens críticos, selecionados
de forma determinística (mesma entrada = mesma ordem).
"""

import pytest
from src.recall_set import generate_recall_set, CriticalityReason


class TestRecallSetHardCap:
    """Testes para hard cap de 12 itens críticos."""

    def test_hard_cap_12_critical_items(self):
        """
        Teste obrigatório: Gerar 20 críticos → retorna 12 sempre iguais na mesma ordem.
        
        Arrange: Extrações que geram 20 itens críticos
        Act: Gerar Recall Set 2 vezes
        Assert: Deve retornar exatamente 12 itens críticos, na mesma ordem
        """
        # Arrange - Criar extrações que gerem 20 itens críticos
        # Usar MULTI_CHUNK (≥2 chunks) para garantir criticidade
        chunk_extractions = []
        
        # Criar 20 conceitos únicos, cada um aparecendo em 2 chunks (MULTI_CHUNK)
        for i in range(20):
            concept = f"Conceito importante {i}"
            # Cada conceito aparece em 2 chunks diferentes
            chunk_extractions.append({
                'chunk_id': i * 2,
                'concepts': [concept],
                'ideas': [],
                'is_heading': False
            })
            chunk_extractions.append({
                'chunk_id': i * 2 + 1,
                'concepts': [concept],
                'ideas': [],
                'is_heading': False
            })
        
        chapter_number = "1"
        
        # Act - Gerar Recall Set 2 vezes
        recall_set_1 = generate_recall_set(chunk_extractions, chapter_number)
        recall_set_2 = generate_recall_set(chunk_extractions, chapter_number)
        
        # Assert
        assert len(recall_set_1.critical_items) == 12, \
            "Deve ter exatamente 12 itens críticos (hard cap)"
        assert len(recall_set_2.critical_items) == 12, \
            "Deve ter exatamente 12 itens críticos na segunda execução"
        
        # Verificar que ordem é a mesma (determinística)
        ids_1 = [item.item_id for item in recall_set_1.critical_items]
        ids_2 = [item.item_id for item in recall_set_2.critical_items]
        assert ids_1 == ids_2, \
            "Ordem deve ser determinística (mesma entrada = mesma ordem)"
        
        # Verificar que todos são críticos
        for item in recall_set_1.critical_items:
            assert item.criticality == "critical", "Todos devem ser críticos"
            assert item.criticality_reason == CriticalityReason.MULTI_CHUNK, \
                "Devem ser marcados como MULTI_CHUNK (aparecem em ≥2 chunks)"

    def test_less_than_12_critical_items(self):
        """
        Teste: Se tiver menos de 12 críticos, retorna todos.
        
        Arrange: Extrações que geram 5 itens críticos
        Act: Gerar Recall Set
        Assert: Deve retornar todos os 5 itens críticos
        """
        # Arrange
        chunk_extractions = []
        for i in range(5):
            concept = f"Conceito {i}"
            chunk_extractions.append({
                'chunk_id': i * 2,
                'concepts': [concept],
                'ideas': [],
                'is_heading': False
            })
            chunk_extractions.append({
                'chunk_id': i * 2 + 1,
                'concepts': [concept],
                'ideas': [],
                'is_heading': False
            })
        
        # Act
        recall_set = generate_recall_set(chunk_extractions, "1")
        
        # Assert
        assert len(recall_set.critical_items) == 5, \
            "Deve retornar todos os 5 itens críticos (< 12)"

    def test_hard_cap_priority_deterministic(self):
        """
        Teste: Hard cap prioriza por frequência e tipo de marcador.
        
        Arrange: Extrações com diferentes frequências e tipos
        Act: Gerar Recall Set
        Assert: Itens com maior frequência e prioridade de marcador vêm primeiro
        """
        # Arrange - Criar itens com diferentes frequências
        chunk_extractions = []
        
        # Item com frequência 5 (deve ser prioritário)
        for i in range(5):
            chunk_extractions.append({
                'chunk_id': i,
                'concepts': ['Conceito frequente'],
                'ideas': [],
                'is_heading': False
            })
        
        # Item com frequência 2 (menor prioridade)
        chunk_extractions.append({
            'chunk_id': 10,
            'concepts': ['Conceito raro'],
            'ideas': [],
            'is_heading': False
        })
        chunk_extractions.append({
            'chunk_id': 11,
            'concepts': ['Conceito raro'],
            'ideas': [],
            'is_heading': False
        })
        
        # Act
        recall_set = generate_recall_set(chunk_extractions, "1")
        
        # Assert - Se tivermos mais de 12, o mais frequente deve vir primeiro
        if len(recall_set.critical_items) >= 2:
            assert recall_set.critical_items[0].frequency >= recall_set.critical_items[1].frequency, \
                "Itens devem estar ordenados por frequência (maior primeiro)"
