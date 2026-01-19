"""
Gate Z3 - Testes de imutabilidade e determinismo de item_id.

ENDFIRST: IDs devem ser determinísticos - mesma entrada = mesmo id.
"""

import pytest
from src.recall_set import generate_item_id, normalize_content


class TestItemIdImmutability:
    """Testes para garantir imutabilidade e determinismo de item_id."""

    def test_same_content_same_id(self):
        """
        Teste 1: Mesmo conteúdo normalizado → mesmo item_id.
        
        Arrange: Mesmo texto e mesmo capítulo
        Act: Gerar item_id 2 vezes
        Assert: Deve retornar mesmo item_id
        """
        # Arrange
        content = "A dopamina é um neurotransmissor importante"
        chapter_number = "1"
        
        # Act
        id1 = generate_item_id(content, chapter_number)
        id2 = generate_item_id(content, chapter_number)
        
        # Assert
        assert id1 == id2, "Mesma entrada deve gerar mesmo item_id (determinístico)"
        assert id1.startswith("RS:cap1:"), "item_id deve seguir formato correto"

    def test_different_content_different_id(self):
        """
        Teste 2: Texto diferente → item_id diferente.
        
        Arrange: Textos diferentes
        Act: Gerar item_id para cada um
        Assert: Deve retornar item_ids diferentes
        """
        # Arrange
        content1 = "A dopamina é um neurotransmissor"
        content2 = "A serotonina é um neurotransmissor"
        chapter_number = "1"
        
        # Act
        id1 = generate_item_id(content1, chapter_number)
        id2 = generate_item_id(content2, chapter_number)
        
        # Assert
        assert id1 != id2, "Conteúdos diferentes devem gerar item_ids diferentes"
        # Pequena mudança (1 caractere) deve mudar o hash
        content3 = "A dopamina é um neurotransmissorr"  # +1 caractere
        id3 = generate_item_id(content3, chapter_number)
        assert id1 != id3, "Mudança mínima deve gerar item_id diferente"

    def test_normalization_removes_punctuation(self):
        """
        Teste 3: Normalização remove pontuação.
        
        Arrange: Textos com pontuação diferente mas mesmo conteúdo
        Act: Gerar item_id para cada um
        Assert: Deve retornar mesmo item_id após normalização
        """
        # Arrange
        content1 = "Hello, world!"
        content2 = "Hello world"
        chapter_number = "1"
        
        # Act
        id1 = generate_item_id(content1, chapter_number)
        id2 = generate_item_id(content2, chapter_number)
        
        # Assert
        assert id1 == id2, "Pontuação deve ser removida na normalização"
        # Verificar normalização diretamente
        norm1 = normalize_content(content1)
        norm2 = normalize_content(content2)
        assert norm1 == norm2, "Normalização deve remover pontuação"

    def test_normalization_removes_redundant_spaces(self):
        """
        Teste 4: Normalização remove espaços redundantes.
        
        Arrange: Textos com espaços diferentes mas mesmo conteúdo
        Act: Gerar item_id para cada um
        Assert: Deve retornar mesmo item_id após normalização
        """
        # Arrange
        content1 = "Hello    world"
        content2 = "Hello world"
        chapter_number = "1"
        
        # Act
        id1 = generate_item_id(content1, chapter_number)
        id2 = generate_item_id(content2, chapter_number)
        
        # Assert
        assert id1 == id2, "Espaços redundantes devem ser removidos na normalização"
        # Verificar normalização diretamente
        norm1 = normalize_content(content1)
        norm2 = normalize_content(content2)
        assert norm1 == norm2, "Normalização deve remover espaços redundantes"

    def test_normalization_lowercase(self):
        """
        Teste 5: Normalização converte para minúsculas.
        
        Arrange: Textos com maiúsculas/minúsculas diferentes
        Act: Gerar item_id para cada um
        Assert: Deve retornar mesmo item_id após normalização
        """
        # Arrange
        content1 = "HELLO WORLD"
        content2 = "hello world"
        content3 = "Hello World"
        chapter_number = "1"
        
        # Act
        id1 = generate_item_id(content1, chapter_number)
        id2 = generate_item_id(content2, chapter_number)
        id3 = generate_item_id(content3, chapter_number)
        
        # Assert
        assert id1 == id2 == id3, "Maiúsculas/minúsculas devem ser normalizadas"

    def test_normalization_removes_accents(self):
        """
        Teste 6: Normalização remove acentos (opcional mas recomendado).
        
        Arrange: Textos com e sem acentos
        Act: Gerar item_id para cada um
        Assert: Deve retornar mesmo item_id após normalização
        """
        # Arrange
        content1 = "café"
        content2 = "cafe"
        chapter_number = "1"
        
        # Act
        id1 = generate_item_id(content1, chapter_number)
        id2 = generate_item_id(content2, chapter_number)
        
        # Assert
        assert id1 == id2, "Acentos devem ser removidos na normalização"

    def test_different_chapters_different_id(self):
        """
        Teste 7: Capítulos diferentes → item_ids diferentes (mesmo conteúdo).
        
        Arrange: Mesmo conteúdo mas capítulos diferentes
        Act: Gerar item_id para cada um
        Assert: Deve retornar item_ids diferentes (capítulo no id)
        """
        # Arrange
        content = "A dopamina é importante"
        
        # Act
        id1 = generate_item_id(content, "1")
        id2 = generate_item_id(content, "2")
        
        # Assert
        assert id1 != id2, "Capítulos diferentes devem gerar item_ids diferentes"
        assert id1.startswith("RS:cap1:"), "item_id deve incluir número do capítulo"
        assert id2.startswith("RS:cap2:"), "item_id deve incluir número do capítulo"

    def test_item_id_format(self):
        """
        Teste 8: item_id deve seguir formato correto.
        
        Arrange: Conteúdo qualquer
        Act: Gerar item_id
        Assert: Deve seguir formato "RS:cap{num}:{hash_6_chars}"
        """
        # Arrange
        content = "Teste de formato"
        chapter_number = "5"
        
        # Act
        item_id = generate_item_id(content, chapter_number)
        
        # Assert
        assert item_id.startswith("RS:cap5:"), "Deve começar com RS:cap{num}:"
        parts = item_id.split(":")
        assert len(parts) == 3, "Deve ter 3 partes separadas por :"
        assert parts[0] == "RS", "Primeira parte deve ser RS"
        assert parts[1] == f"cap{chapter_number}", "Segunda parte deve ser cap{num}"
        assert len(parts[2]) == 6, "Hash deve ter 6 caracteres hexadecimais"
        # Verificar que hash é hexadecimal
        assert all(c in '0123456789abcdef' for c in parts[2]), "Hash deve ser hexadecimal"
