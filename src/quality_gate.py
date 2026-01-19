#!/usr/bin/env python3
"""
CoverageSummarizer - Módulo de Quality Gate
INCR-4: Validação automática de qualidade dos resumos
"""

from typing import Dict, List, Tuple, Optional
import re
import json
import os
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


class QualityGate:
    """Classe responsável por validar a qualidade dos resumos gerados."""
    
    def __init__(self):
        """Inicializa o Quality Gate com critérios de validação."""
        self.max_retries = 3
        self.min_word_count = {
            "curto": 50,      # Mínimo 50 palavras para resumo curto
            "medio": 150,     # Mínimo 150 palavras para resumo médio
            "longo": 300,     # Mínimo 300 palavras para resumo longo
            "bullets": 5       # Mínimo 5 bullets
        }
        self.max_word_count = {
            "curto": 150,     # Máximo 150 palavras para resumo curto
            "medio": 400,     # Máximo 400 palavras para resumo médio
            "longo": 600,     # Máximo 600 palavras para resumo longo
            "bullets": 20     # Máximo 20 bullets
        }
    
    def count_words(self, text: str) -> int:
        """Conta o número de palavras em um texto."""
        return len(text.split())
    
    def count_bullets(self, text: str) -> int:
        """Conta o número de bullet points em um texto."""
        # Buscar por padrões comuns de bullets
        patterns = [
            r'^[-•*]\s+',      # - ou • ou * no início da linha
            r'^\d+\.\s+',      # Números seguidos de ponto
            r'^[a-z]\)\s+',    # Letras minúsculas seguidas de )
        ]
        lines = text.split('\n')
        bullet_count = 0
        for line in lines:
            line = line.strip()
            if any(re.match(pattern, line) for pattern in patterns):
                bullet_count += 1
        return bullet_count
    
    def validate_length(self, summary: str, summary_type: str) -> Tuple[bool, Optional[str]]:
        """
        Valida o comprimento do resumo.
        
        Args:
            summary: Texto do resumo
            summary_type: Tipo do resumo (curto, medio, longo, bullets)
        
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if summary_type == "bullets":
            count = self.count_bullets(summary)
            min_count = self.min_word_count["bullets"]
            max_count = self.max_word_count["bullets"]
            
            if count < min_count:
                return False, f"Resumo tem apenas {count} bullets, mínimo esperado: {min_count}"
            if count > max_count:
                return False, f"Resumo tem {count} bullets, máximo esperado: {max_count}"
            return True, None
        else:
            word_count = self.count_words(summary)
            min_words = self.min_word_count.get(summary_type, 0)
            max_words = self.max_word_count.get(summary_type, float('inf'))
            
            if word_count < min_words:
                return False, f"Resumo tem apenas {word_count} palavras, mínimo esperado: {min_words}"
            if word_count > max_words:
                return False, f"Resumo tem {word_count} palavras, máximo esperado: {max_words}"
            return True, None
    
    def validate_content_quality(self, summary: str, original_text: str) -> Tuple[bool, Optional[str]]:
        """
        Valida a qualidade do conteúdo do resumo.
        
        Args:
            summary: Texto do resumo
            original_text: Texto original
        
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        # Verificar se o resumo não está vazio
        if not summary or len(summary.strip()) < 50:
            return False, "Resumo muito curto ou vazio"
        
        # Verificar se o resumo não é apenas repetição de uma frase
        sentences = re.split(r'[.!?]+', summary)
        unique_sentences = set(s.strip().lower() for s in sentences if len(s.strip()) > 20)
        if len(unique_sentences) < 2:
            return False, "Resumo parece ser repetitivo ou muito simples"
        
        # Verificar se há palavras-chave do texto original no resumo
        # (validação básica de relevância)
        original_words = set(word.lower() for word in original_text.split() if len(word) > 4)
        summary_words = set(word.lower() for word in summary.split() if len(word) > 4)
        common_words = original_words.intersection(summary_words)
        
        if len(common_words) < 3:
            return False, "Resumo não parece estar relacionado ao texto original (poucas palavras em comum)"
        
        return True, None
    
    def validate_structure(self, summary: str, summary_type: str) -> Tuple[bool, Optional[str]]:
        """
        Valida a estrutura do resumo.
        
        Args:
            summary: Texto do resumo
            summary_type: Tipo do resumo
        
        Returns:
            Tupla (é_válido, mensagem_erro)
        """
        if summary_type == "bullets":
            # Verificar se há pelo menos alguns bullets
            if self.count_bullets(summary) == 0:
                return False, "Resumo de bullets não contém bullets formatados"
        
        # Verificar se há pelo menos algumas sentenças completas
        sentences = re.split(r'[.!?]+', summary)
        complete_sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
        
        if len(complete_sentences) < 2:
            return False, "Resumo não contém sentenças completas suficientes"
        
        return True, None
    
    def validate_summary(self, summary: str, summary_type: str, original_text: str) -> Tuple[bool, List[str]]:
        """
        Valida um resumo completo usando todos os critérios.
        
        Args:
            summary: Texto do resumo
            summary_type: Tipo do resumo (curto, medio, longo, bullets)
            original_text: Texto original
        
        Returns:
            Tupla (é_válido, lista_de_erros)
        """
        errors = []
        
        # Validar comprimento
        is_valid_length, length_error = self.validate_length(summary, summary_type)
        if not is_valid_length:
            errors.append(f"Comprimento: {length_error}")
        
        # Validar qualidade do conteúdo
        is_valid_content, content_error = self.validate_content_quality(summary, original_text)
        if not is_valid_content:
            errors.append(f"Conteúdo: {content_error}")
        
        # Validar estrutura
        is_valid_structure, structure_error = self.validate_structure(summary, summary_type)
        if not is_valid_structure:
            errors.append(f"Estrutura: {structure_error}")
        
        is_valid = len(errors) == 0
        return is_valid, errors
    
    def validate_all_summaries(self, summaries: Dict[str, str], original_text: str) -> Dict[str, Tuple[bool, List[str]]]:
        """
        Valida todos os tipos de resumo.
        
        Args:
            summaries: Dicionário com todos os resumos
            original_text: Texto original
        
        Returns:
            Dicionário com resultados de validação para cada tipo
        """
        results = {}
        
        for summary_type in ["curto", "medio", "longo", "bullets"]:
            if summary_type in summaries:
                is_valid, errors = self.validate_summary(
                    summaries[summary_type],
                    summary_type,
                    original_text
                )
                results[summary_type] = (is_valid, errors)
        
        return results
    
    def should_regenerate(self, validation_results: Dict[str, Tuple[bool, List[str]]]) -> bool:
        """
        Decide se os resumos devem ser regenerados com base nos resultados de validação.
        
        Args:
            validation_results: Resultados da validação
        
        Returns:
            True se deve regenerar, False caso contrário
        """
        # Regenerar se mais da metade dos resumos falharam
        failed_count = sum(1 for is_valid, _ in validation_results.values() if not is_valid)
        total_count = len(validation_results)
        
        if total_count == 0:
            return False
        
        failure_rate = failed_count / total_count
        return failure_rate > 0.5  # Mais de 50% de falhas

    def validate_from_coverage_report(self, coverage_report_path: str) -> Tuple[bool, List[str]]:
        """
        Valida cobertura lendo apenas o coverage_report.json (não recalcula nada).
        
        Gate Z1 + Z5.2: Este método é a "fonte única de verdade" do Quality Gate.
        Usa schema rígido (Gate Z5.2) para validar estrutura e depois valida coverage == 100%.
        
        Args:
            coverage_report_path: Caminho para o arquivo coverage_report.json
            
        Returns:
            Tupla (passed, errors) onde:
            - passed: True se coverage == 100.0 e passed == true
            - errors: Lista de mensagens de erro (vazia se passed == True)
            
        Regras:
        - Se arquivo não existe → FAIL
        - Se JSON inválido → FAIL
        - Se schema inválido (campos faltando/tipos errados) → FAIL (Gate Z5.2)
        - Se overall_coverage_percentage < 100.0 → FAIL
        - Se passed == false → FAIL
        - NÃO recalcula nada, apenas lê o arquivo
        """
        errors: List[str] = []
        
        # Validar se arquivo existe
        if not os.path.exists(coverage_report_path):
            errors.append(f"coverage_report.json não encontrado: {coverage_report_path}")
            return (False, errors)
        
        try:
            # Gate Z5.2: Validar schema rígido
            from src.schemas.coverage_report import CoverageReport
            report = CoverageReport.from_json_file(coverage_report_path)
        except json.JSONDecodeError as e:
            errors.append(f"JSON inválido: {str(e)}")
            return (False, errors)
        except ValueError as e:
            # Erro de validação do schema (campos faltando, tipos errados)
            errors.append(f"Schema inválido: {str(e)}")
            return (False, errors)
        except FileNotFoundError:
            errors.append(f"coverage_report.json não encontrado: {coverage_report_path}")
            return (False, errors)
        except Exception as e:
            errors.append(f"Erro ao ler arquivo: {str(e)}")
            return (False, errors)
        
        # Validar overall_coverage_percentage == 100.0
        if report.overall_coverage_percentage < 100.0:
            errors.append(f"Cobertura insuficiente: {report.overall_coverage_percentage}% (requerido: 100.0%)")
        
        # Validar passed == true
        if not report.passed:
            errors.append("coverage_report.json indica que não passou (passed: false)")
        
        # Retornar resultado
        is_valid = len(errors) == 0
        return (is_valid, errors)


def format_validation_report(validation_results: Dict[str, Tuple[bool, List[str]]]) -> str:
    """
    Formata relatório de validação para exibição.
    
    Args:
        validation_results: Resultados da validação
    
    Returns:
        String formatada com o relatório
    """
    output = []
    output.append("=" * 70)
    output.append("QUALITY GATE - Relatório de Validação")
    output.append("=" * 70)
    output.append("")
    
    all_valid = True
    
    for summary_type, (is_valid, errors) in validation_results.items():
        status = "✅ APROVADO" if is_valid else "❌ REPROVADO"
        output.append(f"{summary_type.upper()}: {status}")
        
        if not is_valid:
            all_valid = False
            output.append("  Erros encontrados:")
            for error in errors:
                output.append(f"    • {error}")
        output.append("")
    
    if all_valid:
        output.append("✅ Todos os resumos passaram no Quality Gate!")
    else:
        output.append("⚠️  Alguns resumos falharam na validação.")
        output.append("   O sistema pode tentar regenerar automaticamente.")
    
    output.append("=" * 70)
    
    return "\n".join(output)
