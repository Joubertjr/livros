#!/usr/bin/env python3
"""
CoverageSummarizer - Gerador de Evidências
INCR-6: Evidência automática
"""

import os
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional


class EvidenceGenerator:
    """Classe responsável por gerar evidências de execução do sistema."""
    
    def __init__(self, output_dir: str = "/app/EVIDENCIAS"):
        """
        Inicializa o gerador de evidências.
        
        Args:
            output_dir: Diretório onde salvar evidências
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def generate_evidence(self, summaries: Dict, original_text: str, 
                         input_source: str, execution_info: Optional[Dict] = None) -> str:
        """
        Gera evidência completa de uma execução.
        
        Args:
            summaries: Dicionário com resumos gerados
            original_text: Texto original processado
            input_source: Fonte da entrada (texto direto ou arquivo)
            execution_info: Informações adicionais de execução
        
        Returns:
            Caminho do arquivo de evidência gerado
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        evidence_file = self.output_dir / f"evidence_{timestamp}.json"
        
        # Preparar dados da evidência
        evidence_data = {
            "timestamp": datetime.now().isoformat(),
            "demanda": "DEMANDA-000",
            "sistema": "CoverageSummarizer",
            "input_source": input_source,
            "execution_info": execution_info or {},
            "text_info": {
                "total_characters": len(original_text),
                "total_words": len(original_text.split()),
                "preview": original_text[:500] + "..." if len(original_text) > 500 else original_text
            },
            "summaries": {
                "curto": {
                    "length": len(summaries.get("curto", "")),
                    "word_count": len(summaries.get("curto", "").split()),
                    "preview": summaries.get("curto", "")[:200] + "..." if len(summaries.get("curto", "")) > 200 else summaries.get("curto", "")
                },
                "medio": {
                    "length": len(summaries.get("medio", "")),
                    "word_count": len(summaries.get("medio", "").split()),
                    "preview": summaries.get("medio", "")[:200] + "..." if len(summaries.get("medio", "")) > 200 else summaries.get("medio", "")
                },
                "longo": {
                    "length": len(summaries.get("longo", "")),
                    "word_count": len(summaries.get("longo", "").split()),
                    "preview": summaries.get("longo", "")[:200] + "..." if len(summaries.get("longo", "")) > 200 else summaries.get("longo", "")
                },
                "bullets": {
                    "length": len(summaries.get("bullets", "")),
                    "bullet_count": summaries.get("bullets", "").count("-") + summaries.get("bullets", "").count("•"),
                    "preview": summaries.get("bullets", "")[:200] + "..." if len(summaries.get("bullets", "")) > 200 else summaries.get("bullets", "")
                }
            },
            "tracking_info": summaries.get("tracker_info", {}),
            "validation": {}
        }
        
        # Adicionar informações de validação
        if "validation" in summaries:
            validation_results = summaries["validation"]
            evidence_data["validation"] = {
                summary_type: {
                    "valid": is_valid,
                    "errors": errors
                }
                for summary_type, (is_valid, errors) in validation_results.items()
            }
        
        # Adicionar estatísticas de referências
        if "referencias" in summaries:
            evidence_data["references_info"] = {
                summary_type: {
                    "reference_count": len(refs)
                }
                for summary_type, refs in summaries["referencias"].items()
            }
        
        # Salvar evidência em JSON
        with open(evidence_file, 'w', encoding='utf-8') as f:
            json.dump(evidence_data, f, indent=2, ensure_ascii=False)
        
        # Gerar também relatório em texto
        text_report = self._generate_text_report(evidence_data)
        text_file = self.output_dir / f"evidence_{timestamp}.txt"
        with open(text_file, 'w', encoding='utf-8') as f:
            f.write(text_report)
        
        return str(evidence_file)
    
    def _generate_text_report(self, evidence_data: Dict) -> str:
        """
        Gera relatório de evidência em formato texto.
        
        Args:
            evidence_data: Dados da evidência
        
        Returns:
            Relatório formatado em texto
        """
        lines = []
        lines.append("=" * 70)
        lines.append("EVIDÊNCIA DE EXECUÇÃO - CoverageSummarizer")
        lines.append("=" * 70)
        lines.append("")
        
        lines.append(f"Data/Hora: {evidence_data['timestamp']}")
        lines.append(f"Demanda: {evidence_data['demanda']}")
        lines.append(f"Sistema: {evidence_data['sistema']}")
        lines.append(f"Fonte de entrada: {evidence_data['input_source']}")
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("INFORMAÇÕES DO TEXTO ORIGINAL")
        lines.append("-" * 70)
        text_info = evidence_data['text_info']
        lines.append(f"Total de caracteres: {text_info['total_characters']}")
        lines.append(f"Total de palavras: {text_info['total_words']}")
        lines.append("")
        lines.append("Preview do texto:")
        lines.append(text_info['preview'])
        lines.append("")
        
        lines.append("-" * 70)
        lines.append("RESUMOS GERADOS")
        lines.append("-" * 70)
        for summary_type, summary_data in evidence_data['summaries'].items():
            lines.append(f"\n{summary_type.upper()}:")
            if 'word_count' in summary_data:
                lines.append(f"  Palavras: {summary_data['word_count']}")
            if 'bullet_count' in summary_data:
                lines.append(f"  Bullets: {summary_data['bullet_count']}")
            lines.append(f"  Preview: {summary_data['preview']}")
        lines.append("")
        
        if 'tracking_info' in evidence_data and evidence_data['tracking_info']:
            lines.append("-" * 70)
            lines.append("INFORMAÇÕES DE RASTREABILIDADE")
            lines.append("-" * 70)
            tracking = evidence_data['tracking_info']
            lines.append(f"Total de palavras: {tracking.get('total_palavras', 'N/A')}")
            lines.append(f"Total de segmentos: {tracking.get('total_segmentos', 'N/A')}")
            lines.append("")
        
        if 'validation' in evidence_data and evidence_data['validation']:
            lines.append("-" * 70)
            lines.append("QUALITY GATE - RESULTADOS")
            lines.append("-" * 70)
            for summary_type, validation_data in evidence_data['validation'].items():
                status = "✅ APROVADO" if validation_data['valid'] else "❌ REPROVADO"
                lines.append(f"{summary_type.upper()}: {status}")
                if validation_data['errors']:
                    for error in validation_data['errors']:
                        lines.append(f"  • {error}")
            lines.append("")
        
        if 'references_info' in evidence_data:
            lines.append("-" * 70)
            lines.append("REFERÊNCIAS")
            lines.append("-" * 70)
            for summary_type, ref_info in evidence_data['references_info'].items():
                lines.append(f"{summary_type.upper()}: {ref_info['reference_count']} referências")
            lines.append("")
        
        lines.append("=" * 70)
        lines.append(f"Evidência gerada em {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
        lines.append("=" * 70)
        
        return "\n".join(lines)
    
    def generate_summary_report(self) -> str:
        """
        Gera relatório resumido de todas as evidências.
        
        Returns:
            Caminho do arquivo de relatório
        """
        evidence_files = sorted(self.output_dir.glob("evidence_*.json"))
        
        if not evidence_files:
            return None
        
        summary_data = {
            "total_evidences": len(evidence_files),
            "generated_at": datetime.now().isoformat(),
            "evidences": []
        }
        
        for evidence_file in evidence_files:
            try:
                with open(evidence_file, 'r', encoding='utf-8') as f:
                    evidence = json.load(f)
                    summary_data["evidences"].append({
                        "timestamp": evidence.get("timestamp"),
                        "input_source": evidence.get("input_source"),
                        "text_words": evidence.get("text_info", {}).get("total_words", 0),
                        "validation_status": {
                            k: v.get("valid", False)
                            for k, v in evidence.get("validation", {}).items()
                        }
                    })
            except Exception as e:
                print(f"Erro ao processar {evidence_file}: {e}", file=os.sys.stderr)
        
        summary_file = self.output_dir / "evidence_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2, ensure_ascii=False)
        
        return str(summary_file)
