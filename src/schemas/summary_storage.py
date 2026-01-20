"""
Schema de persistência para resumos e histórico.

Regra Canônica: "Processo que não deixa rastro não é produto, é experimento descartável."
Regra Canônica: "O usuário não deve perder acesso ao que o sistema já produziu para ele."
"""
from pydantic import BaseModel, Field
from typing import Optional, Dict, List
from datetime import datetime
from enum import Enum


class PipelineType(str, Enum):
    """Tipos de pipeline de resumo disponíveis."""
    ROBUST = "robust"  # Pipeline robusto com coverage report
    STANDARD = "standard"  # Pipeline padrão
    EXPERIMENTAL = "experimental"  # Pipeline experimental


class SummaryStorage(BaseModel):
    """
    Schema canônico para persistência de resumos.
    
    Este schema define TODOS os dados que devem ser persistidos
    para garantir rastreabilidade completa do processo.
    """
    # Identificação única
    summary_id: str = Field(..., description="Identificador único do resumo (UUID)")
    title: Optional[str] = Field(None, description="Título/nome do resumo definido pelo usuário")
    
    # Metadados temporais
    created_at: datetime = Field(..., description="Data/hora de criação do resumo")
    updated_at: Optional[datetime] = Field(None, description="Data/hora da última atualização")
    
    # Pipeline e estratégia
    pipeline_type: PipelineType = Field(..., description="Tipo de pipeline usado (robust, standard, experimental)")
    pipeline_version: Optional[str] = Field(None, description="Versão do pipeline (se aplicável)")
    
    # Input
    input_text: Optional[str] = Field(None, description="Texto de entrada (se texto direto)")
    input_file: Optional[str] = Field(None, description="Nome do arquivo de entrada (se arquivo)")
    input_hash: Optional[str] = Field(None, description="Hash do input para detecção de duplicatas")
    
    # Output
    summary: Optional[str] = Field(None, description="Resumo final completo")
    summaries: Optional[Dict[str, str]] = Field(None, description="Resumos por tipo (curto, medio, longo, bullets)")
    
    # Metadados do processo
    coverage_report: Optional[Dict] = Field(None, description="Relatório de cobertura completo")
    addendum_metrics: Optional[Dict] = Field(None, description="Métricas de uso de addendum")
    validation_report: Optional[str] = Field(None, description="Relatório de validação")
    validation: Optional[Dict] = Field(None, description="Dados de validação")
    
    # Arquivos exportados
    exported_files: Dict[str, str] = Field(default_factory=dict, description="Arquivos exportados (formato: caminho)")
    
    # Referências e rastreabilidade
    referencias: Optional[Dict] = Field(None, description="Referências e evidências")
    tracker_info: Optional[Dict] = Field(None, description="Informações do tracker de progresso")
    
    # Estatísticas
    total_words_input: Optional[int] = Field(None, description="Total de palavras no input")
    total_words_output: Optional[int] = Field(None, description="Total de palavras no output")
    processing_time: Optional[float] = Field(None, description="Tempo de processamento em segundos")
    
    # Dados detalhados do processo (rastreabilidade completa)
    process_metadata: Optional[Dict] = Field(None, description="Metadados detalhados do processo de sumarização")
    """
    Estrutura esperada de process_metadata:
    {
        "chapters": [
            {
                "chapter_number": "1",
                "chapter_title": "Título",
                "regeneration_attempts": [
                    {
                        "attempt_number": 1,
                        "timestamp": "2026-01-20T10:00:00",
                        "missing_markers": ["RS:cap1:abc123"],
                        "prompt_strategy": "standard",
                        "temperature": 0.3,
                        "result": "failed" | "passed",
                        "summary_preview": "Primeiros 200 chars..."
                    }
                ],
                "addendum_attempts": [
                    {
                        "attempt_number": 1,
                        "timestamp": "2026-01-20T10:05:00",
                        "missing_item_ids": ["RS:cap1:abc123"],
                        "prompt_strategy": "direct" | "fallback",
                        "temperature": 0.1 | 0.0,
                        "addendum_content": "Conteúdo do addendum gerado",
                        "validation_passed": true | false,
                        "validation_missing": ["RS:cap1:abc123"],
                        "result": "failed" | "passed"
                    }
                ],
                "final_regeneration_count": 3,
                "final_addendum_count": 2,
                "final_missing_markers": []
            }
        ],
        "logs": [
            {
                "timestamp": "2026-01-20T10:00:00",
                "level": "INFO" | "WARNING" | "ERROR",
                "chapter": "1" | null,
                "message": "Mensagem do log"
            }
        ]
    }
    """
    
    class Config:
        json_schema_extra = {
            "example": {
                "summary_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Resumo do Livro X",
                "created_at": "2026-01-19T10:30:00",
                "pipeline_type": "robust",
                "input_file": "livro.pdf",
                "summary": "Resumo completo...",
                "coverage_report": {"coverage": 100.0},
                "exported_files": {"md": "/app/volumes/resumo.md"}
            }
        }


class FeedbackEntry(BaseModel):
    """
    Schema para feedback do usuário vinculado a um resumo.
    
    Regra Canônica: "Feedback sem rastreabilidade é ruído."
    """
    feedback_id: str = Field(..., description="Identificador único do feedback (UUID)")
    summary_id: str = Field(..., description="ID do resumo ao qual o feedback se refere")
    
    # Conteúdo do feedback
    feedback_type: str = Field(..., description="Tipo: 'dúvida', 'erro', 'sugestão', 'elogio'")
    message: str = Field(..., description="Mensagem do feedback")
    
    # Metadados temporais
    created_at: datetime = Field(..., description="Data/hora de criação do feedback")
    
    # Rastreabilidade de resposta
    responded_at: Optional[datetime] = Field(None, description="Data/hora da resposta")
    response: Optional[str] = Field(None, description="Resposta ao feedback (IA ou humano)")
    response_by: Optional[str] = Field(None, description="Quem respondeu (IA, humano, sistema)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "feedback_id": "660e8400-e29b-41d4-a716-446655440001",
                "summary_id": "550e8400-e29b-41d4-a716-446655440000",
                "feedback_type": "sugestão",
                "message": "O resumo poderia ser mais detalhado no capítulo 3",
                "created_at": "2026-01-19T11:00:00"
            }
        }


class SummaryListResponse(BaseModel):
    """Resposta da API para listagem de resumos."""
    summaries: List[Dict] = Field(..., description="Lista de resumos (metadados apenas)")
    total: int = Field(..., description="Total de resumos disponíveis")
    page: Optional[int] = Field(None, description="Página atual (se paginação)")
    page_size: Optional[int] = Field(None, description="Tamanho da página (se paginação)")


class SummaryDetailResponse(BaseModel):
    """Resposta da API para detalhes de um resumo específico."""
    summary: SummaryStorage = Field(..., description="Dados completos do resumo")
    feedback: List[FeedbackEntry] = Field(default_factory=list, description="Feedback associado ao resumo")
