"""
Gate Z6 - Evidence Generator Robusto.

Gera evidências canônicas e auditáveis:
- EVIDENCIAS/coverage_report.json (validado pelo schema)
- EVIDENCIAS/extractions_<timestamp>.json
- EVIDENCIAS/report.md
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
from src.schemas.coverage_report import CoverageReport, ChapterCoverageData, RecallSetData, AuditResultData, SummaryData


class EvidenceGeneratorRobust:
    """
    Gerador de evidências robusto para Gate Z6.
    
    Gera artefatos canônicos e auditáveis seguindo o schema rígido.
    """
    
    def __init__(self, output_dir: str = "EVIDENCIAS"):
        """
        Inicializa o gerador de evidências robusto.
        
        Args:
            output_dir: Diretório onde salvar evidências
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_robust_evidence(
        self,
        chapter_summaries: List[Dict],
        extractions: Dict,
        overall_passed: Optional[bool] = None
    ) -> Dict[str, str]:
        """
        Gera evidências robustas (Gate Z6).
        
        Args:
            chapter_summaries: Lista de dicionários com dados dos capítulos:
                {
                    'chapter_number': str,
                    'chapter_title': str,
                    'summary_text': str,
                    'recall_set': {
                        'critical_items': [...],
                        'supporting_items': [...]
                    },
                    'audit_result': {
                        'passed': bool,
                        'regeneration_count': int,
                        'missing_markers': List[str],
                        'invalid_chunks': List[str]
                    },
                    'total_chunks': int,
                    'processed_chunks': int
                }
            extractions: Dicionário com extrações por capítulo
            overall_passed: Se None, calcula automaticamente
            
        Returns:
            Dicionário com caminhos dos arquivos gerados:
            {
                'coverage_report': str,
                'extractions': str,
                'report_md': str
            }
        """
        # Gerar coverage_report.json
        coverage_report_path = self._generate_coverage_report(chapter_summaries, overall_passed)
        
        # Gerar extractions_<timestamp>.json
        extractions_path = self._generate_extractions(extractions)
        
        # Gerar report.md
        report_md_path = self._generate_report_md(chapter_summaries, coverage_report_path)
        
        return {
            'coverage_report': str(coverage_report_path),
            'extractions': str(extractions_path),
            'report_md': str(report_md_path)
        }
    
    def _generate_coverage_report(
        self,
        chapter_summaries: List[Dict],
        overall_passed: Optional[bool] = None
    ) -> Path:
        """
        Gera coverage_report.json seguindo o schema rígido.
        
        Args:
            chapter_summaries: Lista de dados dos capítulos
            overall_passed: Se None, calcula automaticamente
            
        Returns:
            Caminho do arquivo gerado
        """
        chapters_data = []
        total_critical_items = 0
        total_covered = 0
        chapters_with_100 = 0
        chapters_failed = 0
        
        for chapter_data in chapter_summaries:
            recall_set = chapter_data.get('recall_set', {})
            critical_items = recall_set.get('critical_items', [])
            audit_result = chapter_data.get('audit_result', {})
            
            # Calcular cobertura
            critical_items_total = len(critical_items)
            missing_item_ids = audit_result.get('missing_markers', [])
            critical_items_covered = critical_items_total - len(missing_item_ids)
            
            total_critical_items += critical_items_total
            total_covered += critical_items_covered
            
            # Calcular chunk coverage
            total_chunks = chapter_data.get('total_chunks', 0)
            processed_chunks = chapter_data.get('processed_chunks', 0)
            chunk_coverage = (processed_chunks / total_chunks * 100.0) if total_chunks > 0 else 0.0
            
            # Determinar se passou
            chapter_passed = audit_result.get('passed', False) and chunk_coverage == 100.0
            if chapter_passed:
                chapters_with_100 += 1
            else:
                chapters_failed += 1
            
            chapters_data.append(ChapterCoverageData(
                chapter_number=str(chapter_data.get('chapter_number', '')),
                chapter_title=str(chapter_data.get('chapter_title', '')),
                total_chunks=total_chunks,
                processed_chunks=processed_chunks,
                chunk_coverage_percentage=chunk_coverage,
                recall_set=RecallSetData(
                    critical_items_total=critical_items_total,
                    critical_items_covered=critical_items_covered,
                    supporting_items_total=len(recall_set.get('supporting_items', [])),
                    missing_critical_item_ids=missing_item_ids
                ),
                audit_result=AuditResultData(
                    passed=chapter_passed,
                    regeneration_count=audit_result.get('regeneration_count', 0),
                    addendum_count=audit_result.get('addendum_count', 0),  # NOVO: métrica de addendum
                    missing_markers=audit_result.get('missing_markers', []),
                    invalid_chunks=audit_result.get('invalid_chunks', [])
                )
            ))
        
        # Calcular overall coverage
        overall_coverage = (total_covered / total_critical_items * 100.0) if total_critical_items > 0 else 0.0
        
        # Determinar overall_passed
        if overall_passed is None:
            overall_passed = (
                overall_coverage == 100.0 and
                chapters_failed == 0 and
                all(ch.chunk_coverage_percentage == 100.0 for ch in chapters_data)
            )
        
        # Calcular métricas de addendum (observabilidade)
        chapters_using_addendum = sum(1 for ch in chapters_data if ch.audit_result.addendum_count > 0)
        total_addendums_used = sum(ch.audit_result.addendum_count for ch in chapters_data)
        avg_addendums = total_addendums_used / len(chapters_data) if chapters_data else 0.0
        
        # Criar CoverageReport
        report = CoverageReport(
            version="1.0",
            generated_at=datetime.now().isoformat(),
            overall_coverage_percentage=overall_coverage,
            passed=overall_passed,
            chapters=chapters_data,
            summary=SummaryData(
                total_chapters=len(chapter_summaries),
                chapters_with_100_percent=chapters_with_100,
                chapters_failed=chapters_failed,
                chapters_using_addendum=chapters_using_addendum,  # NOVO: métrica agregada
                total_addendums_used=total_addendums_used,  # NOVO: métrica agregada
                avg_addendums_per_chapter=avg_addendums  # NOVO: métrica agregada
            )
        )
        
        # Salvar JSON
        coverage_report_path = self.output_dir / "coverage_report.json"
        with open(coverage_report_path, 'w', encoding='utf-8') as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)
        
        return coverage_report_path
    
    def _generate_extractions(self, extractions: Dict) -> Path:
        """
        Gera extractions_<timestamp>.json.
        
        Args:
            extractions: Dicionário com extrações por capítulo
            
        Returns:
            Caminho do arquivo gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        extractions_path = self.output_dir / f"extractions_{timestamp}.json"
        
        with open(extractions_path, 'w', encoding='utf-8') as f:
            json.dump(extractions, f, indent=2, ensure_ascii=False)
        
        return extractions_path
    
    def _generate_report_md(
        self,
        chapter_summaries: List[Dict],
        coverage_report_path: Path
    ) -> Path:
        """
        Gera report.md com resumo das evidências.
        
        Args:
            chapter_summaries: Lista de dados dos capítulos
            coverage_report_path: Caminho do coverage_report.json
            
        Returns:
            Caminho do arquivo gerado
        """
        report_md_path = self.output_dir / "report.md"
        
        # Carregar coverage report para obter dados
        report = CoverageReport.from_json_file(str(coverage_report_path))
        
        lines = [
            "# Relatório de Cobertura - CoverageSummarizer",
            "",
            f"**Gerado em:** {report.generated_at}",
            f"**Versão:** {report.version}",
            "",
            "## Resumo Geral",
            "",
            f"- **Cobertura Total:** {report.overall_coverage_percentage:.1f}%",
            f"- **Status:** {'✅ PASSOU' if report.passed else '❌ FALHOU'}",
            f"- **Total de Capítulos:** {report.summary.total_chapters}",
            f"- **Capítulos com 100%:** {report.summary.chapters_with_100_percent}",
            f"- **Capítulos Falhados:** {report.summary.chapters_failed}",
            "",
            "## Detalhes por Capítulo",
            ""
        ]
        
        for chapter in report.chapters:
            lines.extend([
                f"### Capítulo {chapter.chapter_number}: {chapter.chapter_title}",
                "",
                f"- **Chunks:** {chapter.processed_chunks}/{chapter.total_chunks} ({chapter.chunk_coverage_percentage:.1f}%)",
                f"- **Itens Críticos:** {chapter.recall_set.critical_items_covered}/{chapter.recall_set.critical_items_total}",
                f"- **Status:** {'✅ PASSOU' if chapter.audit_result.passed else '❌ FALHOU'}",
                f"- **Regenerações:** {chapter.audit_result.regeneration_count}",
                ""
            ])
            
            if chapter.recall_set.missing_critical_item_ids:
                lines.append(f"- **Itens Faltantes:** {', '.join(chapter.recall_set.missing_critical_item_ids)}")
                lines.append("")
            
            if chapter.audit_result.missing_markers:
                lines.append(f"- **Marcadores Faltantes:** {', '.join(chapter.audit_result.missing_markers)}")
                lines.append("")
            
            if chapter.audit_result.invalid_chunks:
                lines.append(f"- **Chunks Inválidos:** {', '.join(chapter.audit_result.invalid_chunks)}")
                lines.append("")
        
        lines.append("---")
        lines.append("")
        lines.append(f"*Relatório gerado automaticamente pelo CoverageSummarizer*")
        
        with open(report_md_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
        
        return report_md_path
