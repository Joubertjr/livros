"""
Pydantic schemas for API request/response validation.
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class SummarizeRequest(BaseModel):
    """Request schema for summarization endpoint."""
    text: Optional[str] = None
    export_formats: List[str] = Field(default=["md"])

    class Config:
        json_schema_extra = {
            "example": {
                "text": "Texto para resumir...",
                "export_formats": ["md", "pdf"]
            }
        }


class SummarizeResponse(BaseModel):
    """
    Canonical contract between backend and frontend.
    
    The frontend does NOT know about gates, Z0-Z9, RecallSet, or internal logic.
    It only consumes this contract.
    """
    session_id: str
    status: str = Field(..., description="PASS or FAIL - determines if summary is available")
    summary: Optional[str] = Field(None, description="Final summary - only present if status == PASS")
    summaries: Optional[Dict[str, str]] = Field(None, description="Legacy format - chapter-based summaries")
    coverage_report: Optional[Dict] = Field(None, description="Coverage metrics and evidence")
    addendum_metrics: Optional[Dict] = Field(None, description="Addendum usage metrics")
    errors: List[str] = Field(default_factory=list, description="Errors if status == FAIL")
    referencias: Optional[Dict] = None
    validation_report: Optional[str] = None
    validation: Optional[Dict] = None
    exported_files: Dict[str, str] = Field(default_factory=dict)
    tracker_info: Optional[Dict] = None

    class Config:
        json_schema_extra = {
            "example": {
                "session_id": "123e4567-e89b-12d3-a456-426614174000",
                "summaries": {
                    "curto": "Resumo curto...",
                    "medio": "Resumo médio...",
                    "longo": "Resumo longo...",
                    "bullets": "• Ponto 1\n• Ponto 2"
                },
                "exported_files": {
                    "markdown": "/app/volumes/resumo_20260112.md"
                }
            }
        }


class ProgressUpdate(BaseModel):
    """Progress update for SSE streaming."""
    stage: str
    percentage: int
    message: str
    complete: bool = False

    class Config:
        json_schema_extra = {
            "example": {
                "stage": "processing",
                "percentage": 50,
                "message": "Gerando resumo médio...",
                "complete": False
            }
        }


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
