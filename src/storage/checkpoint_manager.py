"""
Gerenciador de checkpoints para persistência progressiva.

Implementa o contrato de retomada segura (F3):
- Carregar checkpoints válidos
- Validar checkpoints
- Salvar checkpoints atomicamente
- Identificar último checkpoint válido

Regra Canônica: "Retomar não é recomeçar."
Regra Canônica: "Falha não pode apagar história."
"""
import json
import logging
from pathlib import Path
from typing import Optional, Dict, List, Tuple
from datetime import datetime
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class CheckpointData:
    """Estrutura de dados de um checkpoint conforme F3."""
    session_id: str
    chapter_number: str
    timestamp_checkpoint: str
    chapter_summary: Dict
    coverage_report: Dict
    metadata: Dict


class CheckpointManager:
    """
    Gerenciador de checkpoints conforme contrato F3.
    
    Implementa:
    - Carregar checkpoints válidos
    - Validar checkpoints
    - Salvar checkpoints atomicamente
    - Identificar último checkpoint válido
    """
    
    def __init__(self, checkpoints_dir: str = "/app/volumes/summaries/checkpoints"):
        """
        Inicializa o gerenciador de checkpoints.
        
        Args:
            checkpoints_dir: Diretório onde os checkpoints serão armazenados
        """
        self.checkpoints_dir = Path(checkpoints_dir)
        self.checkpoints_dir.mkdir(parents=True, exist_ok=True)
    
    def save_checkpoint(
        self,
        session_id: str,
        chapter_number: str,
        chapter_summary: Dict,
        coverage_report: Dict,
        metadata: Dict
    ) -> str:
        """Salva checkpoint atomicamente conforme F3."""
        checkpoint_data = self._create_checkpoint_data(
            session_id, chapter_number, chapter_summary, coverage_report, metadata
        )
        checkpoint_dict = asdict(checkpoint_data)
        file_path = self._get_checkpoint_file_path(session_id, chapter_number)
        return self._save_atomically(file_path, checkpoint_dict)
    
    def load_checkpoint(self, session_id: str, chapter_number: str) -> Optional[CheckpointData]:
        """Carrega checkpoint específico."""
        file_path = self._get_checkpoint_file_path(session_id, chapter_number)
        
        if not file_path.exists():
            return None
        
        try:
            data = self._load_json_file(file_path)
            if self._validate_checkpoint_structure(data):
                return CheckpointData(**data)
            logger.warning(f"⚠️ Checkpoint inválido: {file_path.name}")
            return None
        except Exception as e:
            logger.error(f"❌ Erro ao carregar checkpoint {file_path.name}: {e}")
            return None
    
    def find_last_valid_checkpoint(self, session_id: str) -> Optional[CheckpointData]:
        """Encontra último checkpoint válido da sessão conforme F3."""
        checkpoint_files = self._list_checkpoint_files(session_id)
        
        if not checkpoint_files:
            logger.info(f"ℹ️ Nenhum checkpoint encontrado para sessão {session_id}")
            return None
        
        sorted_checkpoints = self._load_and_sort_checkpoints(checkpoint_files)
        return self._find_first_valid_checkpoint(sorted_checkpoints, session_id)
    
    def get_processed_chapters(self, session_id: str) -> List[str]:
        """
        Retorna lista de capítulos já processados (baseado em checkpoints válidos).
        
        Args:
            session_id: ID da sessão
            
        Returns:
            Lista de números de capítulos já processados
        """
        last_checkpoint = self.find_last_valid_checkpoint(session_id)
        
        if last_checkpoint is None:
            return []
        
        return last_checkpoint.metadata.get('capitulos_processados', [])
    
    # Métodos privados (Clean Code: funções pequenas, responsabilidade única)
    
    def _create_checkpoint_data(
        self,
        session_id: str,
        chapter_number: str,
        chapter_summary: Dict,
        coverage_report: Dict,
        metadata: Dict
    ) -> CheckpointData:
        """Cria estrutura de checkpoint conforme F3."""
        return CheckpointData(
            session_id=session_id,
            chapter_number=chapter_number,
            timestamp_checkpoint=datetime.now().isoformat(),
            chapter_summary=chapter_summary,
            coverage_report=coverage_report,
            metadata=metadata
        )
    
    def _get_checkpoint_file_path(self, session_id: str, chapter_number: str) -> Path:
        """Retorna caminho do arquivo de checkpoint conforme F3."""
        return self.checkpoints_dir / f"{session_id}_checkpoint_{chapter_number}.json"
    
    def _save_atomically(self, file_path: Path, data: Dict) -> str:
        """Salva arquivo atomicamente (arquivo temporário + renomeação)."""
        temp_path = file_path.with_suffix('.tmp')
        
        try:
            self._write_json_file(temp_path, data)
            temp_path.replace(file_path)
            logger.info(f"✅ Checkpoint salvo: {file_path.name}")
            return str(file_path)
        except Exception as e:
            if temp_path.exists():
                temp_path.unlink()
            logger.error(f"❌ Erro ao salvar checkpoint: {e}")
            raise
    
    def _write_json_file(self, file_path: Path, data: Dict) -> None:
        """Escreve dados em arquivo JSON."""
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_json_file(self, file_path: Path) -> Dict:
        """Carrega dados de arquivo JSON."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _list_checkpoint_files(self, session_id: str) -> List[Path]:
        """Lista todos os arquivos de checkpoint da sessão."""
        pattern = f"{session_id}_checkpoint_*.json"
        return list(self.checkpoints_dir.glob(pattern))
    
    def _load_and_sort_checkpoints(
        self,
        checkpoint_files: List[Path]
    ) -> List[Tuple[str, Path, Dict]]:
        """Carrega checkpoints e ordena por timestamp (mais recente primeiro)."""
        checkpoint_with_times = []
        
        for file_path in checkpoint_files:
            try:
                data = self._load_json_file(file_path)
                timestamp = data.get('timestamp_checkpoint', '')
                checkpoint_with_times.append((timestamp, file_path, data))
            except Exception as e:
                logger.warning(f"⚠️ Erro ao ler checkpoint {file_path.name}: {e}")
                continue
        
        checkpoint_with_times.sort(key=lambda x: x[0], reverse=True)
        return checkpoint_with_times
    
    def _find_first_valid_checkpoint(
        self,
        sorted_checkpoints: List[Tuple[str, Path, Dict]],
        session_id: str
    ) -> Optional[CheckpointData]:
        """Encontra primeiro checkpoint válido na lista ordenada."""
        for timestamp, file_path, data in sorted_checkpoints:
            if self._validate_checkpoint(data):
                logger.info(f"✅ Checkpoint válido encontrado: {file_path.name}")
                return CheckpointData(**data)
            else:
                logger.warning(f"⚠️ Checkpoint inválido ignorado: {file_path.name}")
        
        logger.warning(f"⚠️ Nenhum checkpoint válido encontrado para sessão {session_id}")
        return None
    
    def _validate_checkpoint(self, data: Dict) -> bool:
        """Valida checkpoint conforme critério binário F3."""
        validations = [
            self._validate_checkpoint_structure(data),
            self._validate_chapter_summary(data.get('chapter_summary', {})),
            self._validate_coverage_report(data.get('coverage_report', {})),
            self._validate_metadata(data.get('metadata', {})),
            self._validate_consistency(data)
        ]
        return all(validations)
    
    def _validate_checkpoint_structure(self, data: Dict) -> bool:
        """Valida estrutura básica do checkpoint."""
        required_components = ['chapter_summary', 'coverage_report', 'metadata']
        for component in required_components:
            if component not in data:
                return False
        
        if 'session_id' not in data or 'chapter_number' not in data:
            return False
        
        return True
    
    def _validate_chapter_summary(self, chapter_summary: Dict) -> bool:
        """Valida chapter_summary completo."""
        required_fields = ['numero', 'titulo', 'resumo', 'pontos_chave', 'citacoes', 'exemplos']
        
        for field in required_fields:
            if field not in chapter_summary or not chapter_summary[field]:
                logger.debug(f"❌ chapter_summary incompleto: falta {field}")
                return False
        
        return True
    
    def _validate_coverage_report(self, coverage_report: Dict) -> bool:
        """Valida coverage_report completo."""
        required_fields = [
            'chapter_number', 'total_chunks', 'processed_chunks', 'chunk_coverage_percentage'
        ]
        
        for field in required_fields:
            if field not in coverage_report:
                logger.debug(f"❌ coverage_report incompleto: falta {field}")
                return False
        
        if 'recall_set' not in coverage_report:
            logger.debug(f"❌ coverage_report incompleto: falta recall_set")
            return False
        
        if 'audit_result' not in coverage_report:
            logger.debug(f"❌ coverage_report incompleto: falta audit_result")
            return False
        
        return True
    
    def _validate_metadata(self, metadata: Dict) -> bool:
        """Valida metadata atualizado."""
        required_fields = ['session_id', 'capitulos_processados']
        
        for field in required_fields:
            if field not in metadata:
                logger.debug(f"❌ metadata incompleto: falta {field}")
                return False
        
        return True
    
    def _validate_consistency(self, data: Dict) -> bool:
        """Valida consistência entre componentes do checkpoint."""
        chapter_number = data.get('chapter_number')
        metadata = data.get('metadata', {})
        capitulos_processados = metadata.get('capitulos_processados', [])
        
        if chapter_number not in capitulos_processados:
            logger.debug(f"❌ Inconsistência: chapter_number {chapter_number} não está em capitulos_processados")
            return False
        
        if metadata.get('session_id') != data.get('session_id'):
            logger.debug(f"❌ Inconsistência: session_id não corresponde")
            return False
        
        return True
