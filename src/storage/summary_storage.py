"""
Módulo de persistência de resumos.

Regra Canônica: "Processo que não deixa rastro não é produto, é experimento descartável."
Regra Canônica: "O usuário não deve perder acesso ao que o sistema já produziu para ele."
"""
import json
import uuid
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List
import hashlib

# Import relativo para funcionar dentro do container
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from schemas.summary_storage import SummaryStorage, FeedbackEntry, PipelineType


class SummaryStorageManager:
    """
    Gerenciador de persistência de resumos.
    
    Armazena resumos em formato JSON no diretório volumes/summaries/.
    Cada resumo é salvo em um arquivo separado: {summary_id}.json
    """
    
    def __init__(self, storage_dir: str = "/app/volumes/summaries"):
        """
        Inicializa o gerenciador de persistência.
        
        Args:
            storage_dir: Diretório onde os resumos serão armazenados
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Diretório para feedback
        self.feedback_dir = self.storage_dir / "feedback"
        self.feedback_dir.mkdir(parents=True, exist_ok=True)
    
    def save_summary(self, summary: SummaryStorage) -> str:
        """
        Salva um resumo no armazenamento.
        
        Args:
            summary: Objeto SummaryStorage a ser salvo
            
        Returns:
            Caminho do arquivo salvo
        """
        # Garantir que summary_id existe
        if not summary.summary_id or summary.summary_id == "":
            summary.summary_id = str(uuid.uuid4())
        
        # Atualizar timestamps
        if not summary.created_at:
            summary.created_at = datetime.now()
        summary.updated_at = datetime.now()
        
        # Converter para dict
        summary_dict = summary.model_dump(mode='json')
        
        # Converter datetime para string ISO
        if isinstance(summary_dict.get('created_at'), datetime):
            summary_dict['created_at'] = summary_dict['created_at'].isoformat()
        if isinstance(summary_dict.get('updated_at'), datetime):
            summary_dict['updated_at'] = summary_dict['updated_at'].isoformat()
        
        # Salvar arquivo
        file_path = self.storage_dir / f"{summary.summary_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(summary_dict, f, indent=2, ensure_ascii=False)
        
        return str(file_path)
    
    def load_summary(self, summary_id: str) -> Optional[SummaryStorage]:
        """
        Carrega um resumo do armazenamento.
        
        Args:
            summary_id: ID do resumo a ser carregado
            
        Returns:
            Objeto SummaryStorage ou None se não encontrado
        """
        file_path = self.storage_dir / f"{summary_id}.json"
        
        if not file_path.exists():
            return None
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Converter strings ISO de volta para datetime
        if 'created_at' in data and isinstance(data['created_at'], str):
            data['created_at'] = datetime.fromisoformat(data['created_at'])
        if 'updated_at' in data and isinstance(data['updated_at'], str):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        
        return SummaryStorage(**data)
    
    def list_summaries(
        self,
        pipeline_type: Optional[PipelineType] = None,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[SummaryStorage]:
        """
        Lista resumos armazenados.
        
        Args:
            pipeline_type: Filtrar por tipo de pipeline (opcional)
            limit: Limite de resultados (opcional)
            offset: Offset para paginação
            
        Returns:
            Lista de SummaryStorage
        """
        summaries = []
        
        # Listar todos os arquivos JSON
        for file_path in sorted(self.storage_dir.glob("*.json"), reverse=True):
            try:
                summary = self.load_summary(file_path.stem)
                if summary:
                    # Filtrar por pipeline_type se especificado
                    if pipeline_type is None or summary.pipeline_type == pipeline_type:
                        summaries.append(summary)
            except Exception as e:
                # Ignorar arquivos corrompidos
                print(f"Erro ao carregar {file_path}: {e}", file=sys.stderr)
                continue
        
        # Aplicar paginação
        if offset > 0:
            summaries = summaries[offset:]
        if limit:
            summaries = summaries[:limit]
        
        return summaries
    
    def save_feedback(self, feedback: FeedbackEntry) -> str:
        """
        Salva feedback vinculado a um resumo.
        
        Args:
            feedback: Objeto FeedbackEntry a ser salvo
            
        Returns:
            Caminho do arquivo salvo
        """
        # Garantir que feedback_id existe
        if not feedback.feedback_id:
            feedback.feedback_id = str(uuid.uuid4())
        
        # Atualizar timestamp
        if not feedback.created_at:
            feedback.created_at = datetime.now()
        
        # Converter para dict
        feedback_dict = feedback.model_dump(mode='json')
        
        # Converter datetime para string ISO
        if isinstance(feedback_dict.get('created_at'), datetime):
            feedback_dict['created_at'] = feedback_dict['created_at'].isoformat()
        if isinstance(feedback_dict.get('responded_at'), datetime):
            feedback_dict['responded_at'] = feedback_dict['responded_at'].isoformat()
        
        # Salvar arquivo (organizado por summary_id)
        summary_feedback_dir = self.feedback_dir / feedback.summary_id
        summary_feedback_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = summary_feedback_dir / f"{feedback.feedback_id}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(feedback_dict, f, indent=2, ensure_ascii=False)
        
        return str(file_path)
    
    def load_feedback(self, summary_id: str) -> List[FeedbackEntry]:
        """
        Carrega todos os feedbacks de um resumo.
        
        Args:
            summary_id: ID do resumo
            
        Returns:
            Lista de FeedbackEntry
        """
        feedback_dir = self.feedback_dir / summary_id
        
        if not feedback_dir.exists():
            return []
        
        feedbacks = []
        for file_path in feedback_dir.glob("*.json"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Converter strings ISO de volta para datetime
                if 'created_at' in data and isinstance(data['created_at'], str):
                    data['created_at'] = datetime.fromisoformat(data['created_at'])
                if 'responded_at' in data and isinstance(data['responded_at'], str):
                    data['responded_at'] = datetime.fromisoformat(data['responded_at'])
                
                feedbacks.append(FeedbackEntry(**data))
            except Exception as e:
                print(f"Erro ao carregar feedback {file_path}: {e}", file=sys.stderr)
                continue
        
        # Ordenar por data de criação (mais recente primeiro)
        feedbacks.sort(key=lambda f: f.created_at, reverse=True)
        
        return feedbacks


# Instância global do gerenciador
_storage_manager: Optional[SummaryStorageManager] = None


def get_storage_manager() -> SummaryStorageManager:
    """Retorna a instância global do gerenciador de persistência."""
    global _storage_manager
    if _storage_manager is None:
        _storage_manager = SummaryStorageManager()
    return _storage_manager
