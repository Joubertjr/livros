"""
Gate Z2 - Auditoria Determinística Anti-Fraude (Sem LLM).

Implementa validação puramente determinística de marcadores no resumo,
usando regex e validações estruturais sem depender de LLM.
"""

import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

# Regex padrão para marcadores no resumo
# Captura também chunks vazios (para detectar anti-fraude)
MARKER_PATTERN = r'\[\[RS:cap(\d+):([a-f0-9]{6})\|(chunks|src):([^\]]*)\]\]'


@dataclass
class AuditResult:
    """Resultado da auditoria determinística."""
    passed: bool
    missing_markers: List[str]  # item_ids sem marcador
    invalid_chunks: List[str]    # marcadores com chunks inválidos (formato: "item_id:chunk1,chunk2")
    invented_markers: List[str]  # marcadores com item_id inexistente
    errors: List[str]            # Mensagens de erro detalhadas

    def __post_init__(self):
        """Garantir que passed é False se houver erros."""
        if self.missing_markers or self.invalid_chunks or self.invented_markers or self.errors:
            self.passed = False


class RecallAuditor:
    """
    Auditor determinístico para validar marcadores no resumo.
    
    Gate Z2: Validação anti-fraude usando apenas regex e validações estruturais.
    Não depende de LLM.
    """
    
    def __init__(self, marker_pattern: str = MARKER_PATTERN):
        """
        Inicializa o auditor.
        
        Args:
            marker_pattern: Padrão regex para encontrar marcadores no resumo
        """
        self.marker_pattern = marker_pattern
        self.compiled_pattern = re.compile(marker_pattern)
    
    def audit_summary(
        self,
        summary_text: str,
        recall_set: Dict,
        chapter_number: str
    ) -> AuditResult:
        """
        Audita um resumo contra um Recall Set.
        
        Validações determinísticas:
        1. Marcador encontrado: Regex encontra todos os marcadores no resumo
        2. item_id existe: Cada item_id do marcador existe em recall_set['critical_items']
        3. Mínimo 1 chunk: Cada marcador tem pelo menos 1 chunk referenciado
        4. Chunks válidos: Chunks no marcador pertencem a source_chunks do item no Recall Set
        
        Args:
            summary_text: Texto do resumo a auditar
            recall_set: Dicionário com estrutura do Recall Set:
                {
                    'critical_items': [
                        {
                            'item_id': 'RS:cap1:9f3a1c',
                            'source_chunks': [2, 4]
                        },
                        ...
                    ]
                }
            chapter_number: Número do capítulo (para validação)
            
        Returns:
            AuditResult com resultado da auditoria
        """
        missing_markers: List[str] = []
        invalid_chunks: List[str] = []
        invented_markers: List[str] = []
        errors: List[str] = []
        
        # Extrair critical_items do recall_set
        critical_items = recall_set.get('critical_items', [])
        if not critical_items:
            errors.append("Recall Set não contém critical_items")
            return AuditResult(
                passed=False,
                missing_markers=[],
                invalid_chunks=[],
                invented_markers=[],
                errors=errors
            )
        
        # Criar dicionário de item_id -> item para lookup rápido
        items_by_id: Dict[str, Dict] = {}
        for item in critical_items:
            item_id = item.get('item_id')
            if item_id:
                items_by_id[item_id] = item
        
        # Encontrar todos os marcadores no resumo
        markers_found = self.compiled_pattern.findall(summary_text)
        
        # Criar conjunto de item_ids encontrados nos marcadores
        found_item_ids: set = set()
        
        # Validar cada marcador encontrado
        for match in markers_found:
            if len(match) != 4:
                errors.append(f"Marcador inválido encontrado: {match}")
                continue
                
            cap_num_str, item_hash, ref_type, chunks_str = match
            item_id = f"RS:cap{cap_num_str}:{item_hash}"
            
            # Validar número do capítulo
            if cap_num_str != chapter_number:
                errors.append(f"Marcador {item_id} aponta para capítulo {cap_num_str}, esperado {chapter_number}")
            
            # Verificar se item_id existe no Recall Set
            if item_id not in items_by_id:
                invented_markers.append(item_id)
                errors.append(f"Marcador inventado: {item_id} não existe no Recall Set")
                continue
            
            found_item_ids.add(item_id)
            item = items_by_id[item_id]
            source_chunks = item.get('source_chunks', [])
            
            # Validar chunks no marcador
            if not chunks_str or not chunks_str.strip():
                invalid_chunks.append(f"{item_id}:")
                errors.append(f"Marcador {item_id} sem chunks (anti-fraude)")
                continue
            
            # Parsear chunks do marcador
            try:
                chunks = [int(c.strip()) for c in chunks_str.split(',') if c.strip().isdigit()]
            except (ValueError, AttributeError):
                chunks = []
            
            # Validar que tem pelo menos 1 chunk
            if len(chunks) == 0:
                invalid_chunks.append(f"{item_id}:")
                errors.append(f"Marcador {item_id} não tem chunks válidos (anti-fraude)")
                continue
            
            # Validar que chunks estão em source_chunks
            invalid_chunk_list = [c for c in chunks if c not in source_chunks]
            if invalid_chunk_list:
                invalid_chunks.append(f"{item_id}:{','.join(map(str, invalid_chunk_list))}")
                errors.append(
                    f"Marcador {item_id} aponta para chunks {invalid_chunk_list} "
                    f"que não estão em source_chunks {source_chunks}"
                )
        
        # Verificar se todos os critical_items têm marcador
        for item in critical_items:
            item_id = item.get('item_id')
            if item_id and item_id not in found_item_ids:
                missing_markers.append(item_id)
                errors.append(f"Item crítico {item_id} não tem marcador no resumo")
        
        # Criar resultado
        result = AuditResult(
            passed=len(missing_markers) == 0 and len(invalid_chunks) == 0 and len(invented_markers) == 0 and len(errors) == 0,
            missing_markers=missing_markers,
            invalid_chunks=invalid_chunks,
            invented_markers=invented_markers,
            errors=errors
        )
        
        logger.debug(f"Auditoria concluída: passed={result.passed}, "
                    f"missing={len(missing_markers)}, invalid={len(invalid_chunks)}, "
                    f"invented={len(invented_markers)}")
        
        return result
