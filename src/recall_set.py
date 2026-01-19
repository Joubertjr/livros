"""
Gate Z3/Z4 - Geração de item_id imutável e Recall Set com Hard Cap.

Gate Z3: item_id imutável (determinístico)
Gate Z4: Geração de Recall Set com enum CriticalityReason e hard cap de 12 itens críticos.
"""

import hashlib
import re
import unicodedata
from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


def normalize_content(content: str) -> str:
    """
    Normaliza conteúdo para garantir determinismo na geração de item_id.
    
    Processo de normalização:
    1. Remover pontuação
    2. Remover espaços redundantes
    3. Converter para minúsculas
    4. Remover acentos (opcional, mas recomendado)
    
    Args:
        content: Conteúdo a normalizar
        
    Returns:
        Conteúdo normalizado
    """
    if not content:
        return ""
    
    # Converter para minúsculas
    normalized = content.lower()
    
    # Remover acentos usando NFKD (decomposição) + remover diacríticos
    normalized = unicodedata.normalize('NFKD', normalized)
    normalized = ''.join(c for c in normalized if not unicodedata.combining(c))
    
    # Remover pontuação (manter apenas letras, números e espaços)
    normalized = re.sub(r'[^\w\s]', '', normalized)
    
    # Remover espaços redundantes
    normalized = re.sub(r'\s+', ' ', normalized)
    normalized = normalized.strip()
    
    return normalized


def generate_item_id(content: str, chapter_number: str) -> str:
    """
    Gera item_id imutável usando hash SHA256 do conteúdo normalizado.
    
    Processo:
    1. Normalizar conteúdo
    2. Gerar hash SHA256
    3. Pegar primeiros 6 caracteres hexadecimais
    4. Retornar: f"RS:cap{chapter_number}:{hash_short}"
    
    Args:
        content: Conteúdo do item (será normalizado)
        chapter_number: Número do capítulo
        
    Returns:
        item_id no formato: "RS:cap1:9f3a1c"
        
    Exemplo:
        >>> generate_item_id("A dopamina é importante", "1")
        'RS:cap1:9f3a1c'
        
        >>> generate_item_id("A dopamina é importante", "1")  # Mesma entrada
        'RS:cap1:9f3a1c'  # Mesmo resultado (determinístico)
    """
    # Normalizar conteúdo
    normalized = normalize_content(content)
    
    # Gerar hash SHA256
    hash_obj = hashlib.sha256(normalized.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()
    
    # Pegar primeiros 6 caracteres
    hash_short = hash_hex[:6]
    
    # Retornar item_id formatado
    return f"RS:cap{chapter_number}:{hash_short}"


class CriticalityReason(Enum):
    """Razão da criticidade de um item no Recall Set."""
    MULTI_CHUNK = "MULTI_CHUNK"                    # Aparece em ≥2 chunks
    STRUCTURAL_POSITION = "STRUCTURAL_POSITION"    # Em heading/título
    DEFINITION_MARKER = "DEFINITION_MARKER"       # Palavras-chave: "definição", "significa", "é"
    LAW_MARKER = "LAW_MARKER"                     # Palavras-chave: "lei", "regra", "princípio"


@dataclass
class RecallSetItem:
    """Item do Recall Set."""
    item_id: str
    content: str
    criticality: str  # "critical" ou "supporting"
    criticality_reason: Optional[CriticalityReason]
    source_chunks: List[int]  # chunk_ids onde aparece
    frequency: int  # Quantas vezes aparece


@dataclass
class RecallSet:
    """Recall Set de um capítulo."""
    chapter_number: str
    critical_items: List[RecallSetItem]  # Máximo 12
    supporting_items: List[RecallSetItem]  # Sem limite


# Palavras-chave para detecção de criticidade
DEFINITION_KEYWORDS = ['definição', 'define', 'significa', 'é', 'são', 'representa', 'caracteriza']
LAW_KEYWORDS = ['lei', 'regra', 'princípio', 'norma', 'mandamento', 'preceito']


def _determine_criticality(
    item_content: str,
    chunk_count: int,
    is_structural: bool
) -> Tuple[str, Optional[CriticalityReason]]:
    """
    Determina criticidade de um item usando regras mecânicas.
    
    Regras:
    1. MULTI_CHUNK: Aparece em ≥2 chunks diferentes
    2. STRUCTURAL_POSITION: Aparece em heading/título de chunk
    3. DEFINITION_MARKER: Contém palavras-chave de definição
    4. LAW_MARKER: Contém palavras-chave de lei/regra
    
    Args:
        item_content: Conteúdo do item
        chunk_count: Número de chunks onde aparece
        is_structural: Se aparece em posição estrutural (heading/título)
        
    Returns:
        Tupla (criticality, reason) onde:
        - criticality: "critical" ou "supporting"
        - reason: CriticalityReason ou None
    """
    content_lower = item_content.lower()
    
    # Prioridade 1: DEFINITION_MARKER
    if any(keyword in content_lower for keyword in DEFINITION_KEYWORDS):
        return ("critical", CriticalityReason.DEFINITION_MARKER)
    
    # Prioridade 2: LAW_MARKER
    if any(keyword in content_lower for keyword in LAW_KEYWORDS):
        return ("critical", CriticalityReason.LAW_MARKER)
    
    # Prioridade 3: MULTI_CHUNK
    if chunk_count >= 2:
        return ("critical", CriticalityReason.MULTI_CHUNK)
    
    # Prioridade 4: STRUCTURAL_POSITION
    if is_structural:
        return ("critical", CriticalityReason.STRUCTURAL_POSITION)
    
    # Se nenhum critério, é supporting
    return ("supporting", None)


def _sort_items_for_hard_cap(items: List[RecallSetItem]) -> List[RecallSetItem]:
    """
    Ordena itens críticos para aplicar hard cap 12 de forma determinística.
    
    Ordem de desempate:
    1. Frequência (maior primeiro)
    2. Tipo de marcador (DEFINITION > LAW > MULTI_CHUNK > STRUCTURAL)
    3. Número de chunks (maior primeiro)
    4. Posição do item_id (lexicográfico, para determinismo)
    
    Args:
        items: Lista de itens críticos a ordenar
        
    Returns:
        Lista ordenada (determinística)
    """
    def sort_key(item: RecallSetItem) -> tuple:
        # Prioridade do tipo de marcador
        reason_priority = {
            CriticalityReason.DEFINITION_MARKER: 0,
            CriticalityReason.LAW_MARKER: 1,
            CriticalityReason.MULTI_CHUNK: 2,
            CriticalityReason.STRUCTURAL_POSITION: 3,
            None: 4
        }
        reason_prio = reason_priority.get(item.criticality_reason, 4)
        
        # Retornar tupla para ordenação
        # Negativo na frequência para ordem decrescente (maior primeiro)
        return (
            -item.frequency,  # Maior frequência primeiro
            reason_prio,      # Menor número = maior prioridade
            -len(item.source_chunks),  # Mais chunks primeiro
            item.item_id      # Lexicográfico para determinismo
        )
    
    return sorted(items, key=sort_key)


def generate_recall_set(
    chunk_extractions: List[Dict],
    chapter_number: str,
    hard_cap_critical: int = 12
) -> RecallSet:
    """
    Gera Recall Set a partir de extrações de chunks.
    
    Gate Z4: Aplica hard cap de 12 itens críticos com desempate determinístico.
    
    Args:
        chunk_extractions: Lista de dicionários com extrações por chunk:
            [
                {
                    'chunk_id': 1,
                    'concepts': ['conceito1', 'conceito2'],
                    'ideas': ['ideia1'],
                    'is_heading': False
                },
                ...
            ]
        chapter_number: Número do capítulo
        hard_cap_critical: Limite máximo de itens críticos (padrão: 12)
        
    Returns:
        RecallSet com critical_items (≤12) e supporting_items
    """
    # Agregar itens de todos os chunks
    items_dict: Dict[str, Dict] = {}
    
    for extraction in chunk_extractions:
        chunk_id = extraction.get('chunk_id', 0)
        is_heading = extraction.get('is_heading', False)
        
        # Processar conceitos
        concepts = extraction.get('concepts', [])
        for concept in concepts:
            normalized = normalize_content(concept)
            item_id = generate_item_id(concept, chapter_number)
            
            if item_id not in items_dict:
                items_dict[item_id] = {
                    'content': concept,
                    'item_id': item_id,
                    'source_chunks': [],
                    'frequency': 0,
                    'is_structural': False
                }
            
            items_dict[item_id]['source_chunks'].append(chunk_id)
            items_dict[item_id]['frequency'] += 1
            if is_heading:
                items_dict[item_id]['is_structural'] = True
        
        # Processar ideias
        ideas = extraction.get('ideas', [])
        for idea in ideas:
            normalized = normalize_content(idea)
            item_id = generate_item_id(idea, chapter_number)
            
            if item_id not in items_dict:
                items_dict[item_id] = {
                    'content': idea,
                    'item_id': item_id,
                    'source_chunks': [],
                    'frequency': 0,
                    'is_structural': False
                }
            
            items_dict[item_id]['source_chunks'].append(chunk_id)
            items_dict[item_id]['frequency'] += 1
            if is_heading:
                items_dict[item_id]['is_structural'] = True
    
    # Remover duplicatas de source_chunks
    for item_data in items_dict.values():
        item_data['source_chunks'] = sorted(list(set(item_data['source_chunks'])))
    
    # Determinar criticidade de cada item
    critical_items: List[RecallSetItem] = []
    supporting_items: List[RecallSetItem] = []
    
    for item_data in items_dict.values():
        criticality, reason = _determine_criticality(
            item_data['content'],
            len(item_data['source_chunks']),
            item_data['is_structural']
        )
        
        item = RecallSetItem(
            item_id=item_data['item_id'],
            content=item_data['content'],
            criticality=criticality,
            criticality_reason=reason,
            source_chunks=item_data['source_chunks'],
            frequency=item_data['frequency']
        )
        
        if criticality == "critical":
            critical_items.append(item)
        else:
            supporting_items.append(item)
    
    # Aplicar hard cap 12 em critical_items
    if len(critical_items) > hard_cap_critical:
        # Ordenar de forma determinística
        critical_items = _sort_items_for_hard_cap(critical_items)
        # Manter apenas os primeiros 12
        critical_items = critical_items[:hard_cap_critical]
    
    return RecallSet(
        chapter_number=chapter_number,
        critical_items=critical_items,
        supporting_items=supporting_items
    )

