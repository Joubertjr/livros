"""
Gate Z5.2 - Schema rígido para coverage_report.json.

Congela o contrato do coverage_report para evitar mudanças não controladas.
Validação determinística sem depender de bibliotecas externas.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
import json


@dataclass
class RecallSetData:
    """Dados do Recall Set no coverage report."""
    critical_items_total: int
    critical_items_covered: int
    supporting_items_total: int
    missing_critical_item_ids: List[str] = field(default_factory=list)


@dataclass
class AuditResultData:
    """Dados do resultado da auditoria no coverage report."""
    passed: bool
    regeneration_count: int
    addendum_count: int = 0  # Número de addendums usados (Estratégia A)
    missing_markers: List[str] = field(default_factory=list)
    invalid_chunks: List[str] = field(default_factory=list)


@dataclass
class ChapterCoverageData:
    """Dados de cobertura de um capítulo."""
    chapter_number: str
    chapter_title: str
    total_chunks: int
    processed_chunks: int
    chunk_coverage_percentage: float
    recall_set: RecallSetData
    audit_result: AuditResultData


@dataclass
class SummaryData:
    """Dados de resumo geral."""
    total_chapters: int
    chapters_with_100_percent: int
    chapters_failed: int
    # Métricas de addendum (observabilidade)
    chapters_using_addendum: int = 0
    total_addendums_used: int = 0
    avg_addendums_per_chapter: float = 0.0


@dataclass
class CoverageReport:
    """
    Schema rígido para coverage_report.json.
    
    Gate Z5.2: Este schema congela o contrato e valida todos os campos obrigatórios.
    """
    version: str
    generated_at: str
    overall_coverage_percentage: float
    passed: bool
    chapters: List[ChapterCoverageData]
    summary: SummaryData
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'CoverageReport':
        """
        Cria CoverageReport a partir de dicionário, validando estrutura.
        
        Args:
            data: Dicionário com dados do coverage report
            
        Returns:
            CoverageReport validado
            
        Raises:
            ValueError: Se estrutura estiver inválida ou campos obrigatórios faltarem
        """
        # Validar campos obrigatórios do nível raiz
        required_root_fields = ['version', 'generated_at', 'overall_coverage_percentage', 'passed', 'chapters', 'summary']
        for field_name in required_root_fields:
            if field_name not in data:
                raise ValueError(f"Campo obrigatório faltando: '{field_name}'")
        
        # Validar tipos do nível raiz
        if not isinstance(data['version'], str):
            raise ValueError(f"Campo 'version' deve ser string, encontrado: {type(data['version'])}")
        if not isinstance(data['generated_at'], str):
            raise ValueError(f"Campo 'generated_at' deve ser string, encontrado: {type(data['generated_at'])}")
        if not isinstance(data['overall_coverage_percentage'], (int, float)):
            raise ValueError(f"Campo 'overall_coverage_percentage' deve ser número, encontrado: {type(data['overall_coverage_percentage'])}")
        if not isinstance(data['passed'], bool):
            raise ValueError(f"Campo 'passed' deve ser boolean, encontrado: {type(data['passed'])}")
        if not isinstance(data['chapters'], list):
            raise ValueError(f"Campo 'chapters' deve ser lista, encontrado: {type(data['chapters'])}")
        if not isinstance(data['summary'], dict):
            raise ValueError(f"Campo 'summary' deve ser objeto, encontrado: {type(data['summary'])}")
        
        # Validar e criar chapters
        chapters = []
        for i, chapter_data in enumerate(data['chapters']):
            if not isinstance(chapter_data, dict):
                raise ValueError(f"Chapter {i} deve ser objeto, encontrado: {type(chapter_data)}")
            
            # Validar campos obrigatórios do chapter
            required_chapter_fields = ['chapter_number', 'chapter_title', 'total_chunks', 
                                      'processed_chunks', 'chunk_coverage_percentage', 
                                      'recall_set', 'audit_result']
            for field_name in required_chapter_fields:
                if field_name not in chapter_data:
                    raise ValueError(f"Chapter {i}: campo obrigatório faltando: '{field_name}'")
            
            # Validar recall_set
            recall_set_data = chapter_data['recall_set']
            if not isinstance(recall_set_data, dict):
                raise ValueError(f"Chapter {i}: 'recall_set' deve ser objeto")
            required_recall_fields = ['critical_items_total', 'critical_items_covered', 
                                     'supporting_items_total', 'missing_critical_item_ids']
            for field_name in required_recall_fields:
                if field_name not in recall_set_data:
                    raise ValueError(f"Chapter {i}.recall_set: campo obrigatório faltando: '{field_name}'")
            
            recall_set = RecallSetData(
                critical_items_total=recall_set_data['critical_items_total'],
                critical_items_covered=recall_set_data['critical_items_covered'],
                supporting_items_total=recall_set_data['supporting_items_total'],
                missing_critical_item_ids=recall_set_data.get('missing_critical_item_ids', [])
            )
            
            # Validar audit_result
            audit_data = chapter_data['audit_result']
            if not isinstance(audit_data, dict):
                raise ValueError(f"Chapter {i}: 'audit_result' deve ser objeto")
            required_audit_fields = ['passed', 'regeneration_count', 'missing_markers', 'invalid_chunks']
            for field_name in required_audit_fields:
                if field_name not in audit_data:
                    raise ValueError(f"Chapter {i}.audit_result: campo obrigatório faltando: '{field_name}'")
            
            audit_result = AuditResultData(
                passed=audit_data['passed'],
                regeneration_count=audit_data['regeneration_count'],
                addendum_count=audit_data.get('addendum_count', 0),  # Default 0 para compatibilidade
                missing_markers=audit_data.get('missing_markers', []),
                invalid_chunks=audit_data.get('invalid_chunks', [])
            )
            
            chapters.append(ChapterCoverageData(
                chapter_number=str(chapter_data['chapter_number']),
                chapter_title=str(chapter_data['chapter_title']),
                total_chunks=int(chapter_data['total_chunks']),
                processed_chunks=int(chapter_data['processed_chunks']),
                chunk_coverage_percentage=float(chapter_data['chunk_coverage_percentage']),
                recall_set=recall_set,
                audit_result=audit_result
            ))
        
        # Validar summary
        summary_data = data['summary']
        required_summary_fields = ['total_chapters', 'chapters_with_100_percent', 'chapters_failed']
        for field_name in required_summary_fields:
            if field_name not in summary_data:
                raise ValueError(f"summary: campo obrigatório faltando: '{field_name}'")
        
        summary = SummaryData(
            total_chapters=int(summary_data['total_chapters']),
            chapters_with_100_percent=int(summary_data['chapters_with_100_percent']),
            chapters_failed=int(summary_data['chapters_failed'])
        )
        
        return cls(
            version=data['version'],
            generated_at=data['generated_at'],
            overall_coverage_percentage=float(data['overall_coverage_percentage']),
            passed=bool(data['passed']),
            chapters=chapters,
            summary=summary
        )
    
    @classmethod
    def from_json_file(cls, file_path: str) -> 'CoverageReport':
        """
        Carrega e valida coverage_report.json de arquivo.
        
        Args:
            file_path: Caminho para o arquivo JSON
            
        Returns:
            CoverageReport validado
            
        Raises:
            FileNotFoundError: Se arquivo não existe
            json.JSONDecodeError: Se JSON está malformado
            ValueError: Se estrutura estiver inválida
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def to_dict(self) -> Dict:
        """Converte CoverageReport para dicionário."""
        return {
            'version': self.version,
            'generated_at': self.generated_at,
            'overall_coverage_percentage': self.overall_coverage_percentage,
            'passed': self.passed,
            'chapters': [
                {
                    'chapter_number': ch.chapter_number,
                    'chapter_title': ch.chapter_title,
                    'total_chunks': ch.total_chunks,
                    'processed_chunks': ch.processed_chunks,
                    'chunk_coverage_percentage': ch.chunk_coverage_percentage,
                    'recall_set': {
                        'critical_items_total': ch.recall_set.critical_items_total,
                        'critical_items_covered': ch.recall_set.critical_items_covered,
                        'supporting_items_total': ch.recall_set.supporting_items_total,
                        'missing_critical_item_ids': ch.recall_set.missing_critical_item_ids
                    },
                    'audit_result': {
                        'passed': ch.audit_result.passed,
                        'regeneration_count': ch.audit_result.regeneration_count,
                        'addendum_count': ch.audit_result.addendum_count,
                        'missing_markers': ch.audit_result.missing_markers,
                        'invalid_chunks': ch.audit_result.invalid_chunks
                    }
                }
                for ch in self.chapters
            ],
            'summary': {
                'total_chapters': self.summary.total_chapters,
                'chapters_with_100_percent': self.summary.chapters_with_100_percent,
                'chapters_failed': self.summary.chapters_failed,
                'chapters_using_addendum': self.summary.chapters_using_addendum,
                'total_addendums_used': self.summary.total_addendums_used,
                'avg_addendums_per_chapter': self.summary.avg_addendums_per_chapter
            }
        }
