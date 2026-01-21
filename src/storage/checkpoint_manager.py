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
from typing import Optional, Dict, List
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
        """
        Salva checkpoint atomicamente conforme F3.
        
        Args:
            session_id: ID da sessão
            chapter_number: Número do capítulo
            chapter_summary: ChapterSummary completo
            coverage_report: CoverageReport parcial do capítulo
            metadata: Metadados de processamento atualizados
            
        Returns:
            Caminho do arquivo salvo
            
        Raises:
            Exception: Se persistência falhar (atomicidade)
        """
        # Criar estrutura de checkpoint conforme F3
        checkpoint_data = CheckpointData(
            session_id=session_id,
            chapter_number=chapter_number,
            timestamp_checkpoint=datetime.now().isoformat(),
            chapter_summary=chapter_summary,
            coverage_report=coverage_report,
            metadata=metadata
        )
        
        # Converter para dict
        checkpoint_dict = asdict(checkpoint_data)
        
        # Nome do arquivo conforme F3: {session_id}_checkpoint_{chapter_number}.json
        file_path = self.checkpoints_dir / f"{session_id}_checkpoint_{chapter_number}.json"
        
        # Salvar atomicamente (escrever em arquivo temporário primeiro)
        temp_path = file_path.with_suffix('.tmp')
        
        try:
            # Escrever em arquivo temporário
            with open(temp_path, 'w', encoding='utf-8') as f:
                json.dump(checkpoint_dict, f, indent=2, ensure_ascii=False)
            
            # Renomear para arquivo final (operação atômica)
            temp_path.replace(file_path)
            
            logger.info(f"✅ Checkpoint salvo: {file_path.name}")
            return str(file_path)
            
        except Exception as e:
            # Se falhar, remover arquivo temporário
            if temp_path.exists():
                temp_path.unlink()
            logger.error(f"❌ Erro ao salvar checkpoint: {e}")
            raise
    
    def load_checkpoint(self, session_id: str, chapter_number: str) -> Optional[CheckpointData]:
        """
        Carrega checkpoint específico.
        
        Args:
            session_id: ID da sessão
            chapter_number: Número do capítulo
            
        Returns:
            CheckpointData se encontrado e válido, None caso contrário
        """
        file_path = self.checkpoints_dir / f"{session_id}_checkpoint_{chapter_number}.json"
        
        if not file_path.exists():
            return None
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Validar checkpoint antes de retornar
            if self._validate_checkpoint_structure(data):
                return CheckpointData(**data)
            else:
                logger.warning(f"⚠️ Checkpoint inválido: {file_path.name}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Erro ao carregar checkpoint {file_path.name}: {e}")
            return None
    
    def find_last_valid_checkpoint(self, session_id: str) -> Optional[CheckpointData]:
        """
        Encontra último checkpoint válido da sessão conforme F3.
        
        Algoritmo F3:
        1. Listar todos os checkpoints da sessão
        2. Ordenar por timestamp (mais recente primeiro)
        3. Validar cada checkpoint (do mais recente para o mais antigo)
        4. Selecionar primeiro checkpoint válido encontrado
        
        Args:
            session_id: ID da sessão
            
        Returns:
            CheckpointData do último checkpoint válido, ou None se nenhum válido
        """
        # Listar todos os checkpoints da sessão
        pattern = f"{session_id}_checkpoint_*.json"
        checkpoint_files = list(self.checkpoints_dir.glob(pattern))
        
        if not checkpoint_files:
            logger.info(f"ℹ️ Nenhum checkpoint encontrado para sessão {session_id}")
            return None
        
        # Ordenar por timestamp (mais recente primeiro)
        # Extrair timestamp do arquivo ou do conteúdo
        checkpoint_with_times = []
        for file_path in checkpoint_files:
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    timestamp = data.get('timestamp_checkpoint', '')
                    checkpoint_with_times.append((timestamp, file_path, data))
            except Exception as e:
                logger.warning(f"⚠️ Erro ao ler checkpoint {file_path.name}: {e}")
                continue
        
        # Ordenar por timestamp (mais recente primeiro)
        checkpoint_with_times.sort(key=lambda x: x[0], reverse=True)
        
        # Validar cada checkpoint (do mais recente para o mais antigo)
        for timestamp, file_path, data in checkpoint_with_times:
            if self._validate_checkpoint(data):
                logger.info(f"✅ Checkpoint válido encontrado: {file_path.name}")
                return CheckpointData(**data)
            else:
                logger.warning(f"⚠️ Checkpoint inválido ignorado: {file_path.name}")
        
        logger.warning(f"⚠️ Nenhum checkpoint válido encontrado para sessão {session_id}")
        return None
    
    def _validate_checkpoint(self, data: Dict) -> bool:
        """
        Valida checkpoint conforme critério binário F3.
        
        Critério F3:
        SE arquivo existe E é JSON válido
        E chapter_summary está completo (todos os campos obrigatórios)
        E coverage_report está completo (todos os campos obrigatórios)
        E metadata está atualizado (todos os campos obrigatórios)
        E validação de schema passa
        ENTÃO checkpoint é VÁLIDO
        
        Args:
            data: Dados do checkpoint (dict)
            
        Returns:
            True se válido, False caso contrário
        """
        # 1. Validar estrutura básica
        if not self._validate_checkpoint_structure(data):
            return False
        
        # 2. Validar chapter_summary completo
        chapter_summary = data.get('chapter_summary', {})
        required_summary_fields = ['numero', 'titulo', 'resumo', 'pontos_chave', 'citacoes', 'exemplos']
        for field in required_summary_fields:
            if field not in chapter_summary or not chapter_summary[field]:
                logger.debug(f"❌ chapter_summary incompleto: falta {field}")
                return False
        
        # 3. Validar coverage_report completo
        coverage_report = data.get('coverage_report', {})
        required_coverage_fields = ['chapter_number', 'total_chunks', 'processed_chunks', 'chunk_coverage_percentage']
        for field in required_coverage_fields:
            if field not in coverage_report:
                logger.debug(f"❌ coverage_report incompleto: falta {field}")
                return False
        
        # Validar recall_set e audit_result (devem existir)
        if 'recall_set' not in coverage_report:
            logger.debug(f"❌ coverage_report incompleto: falta recall_set")
            return False
        if 'audit_result' not in coverage_report:
            logger.debug(f"❌ coverage_report incompleto: falta audit_result")
            return False
        
        # 4. Validar metadata atualizado
        metadata = data.get('metadata', {})
        required_metadata_fields = ['session_id', 'capitulos_processados']
        for field in required_metadata_fields:
            if field not in metadata:
                logger.debug(f"❌ metadata incompleto: falta {field}")
                return False
        
        # Validar consistência: chapter_number deve estar em capitulos_processados
        chapter_number = data.get('chapter_number')
        capitulos_processados = metadata.get('capitulos_processados', [])
        if chapter_number not in capitulos_processados:
            logger.debug(f"❌ Inconsistência: chapter_number {chapter_number} não está em capitulos_processados")
            return False
        
        # Validar consistência: session_id deve corresponder
        if metadata.get('session_id') != data.get('session_id'):
            logger.debug(f"❌ Inconsistência: session_id não corresponde")
            return False
        
        return True
    
    def _validate_checkpoint_structure(self, data: Dict) -> bool:
        """
        Valida estrutura básica do checkpoint.
        
        Args:
            data: Dados do checkpoint (dict)
            
        Returns:
            True se estrutura básica está correta, False caso contrário
        """
        # Verificar se contém os 3 componentes obrigatórios
        required_components = ['chapter_summary', 'coverage_report', 'metadata']
        for component in required_components:
            if component not in data:
                return False
        
        # Verificar se session_id e chapter_number estão presentes
        if 'session_id' not in data or 'chapter_number' not in data:
            return False
        
        return True
    
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
        
        metadata = last_checkpoint.metadata
        return metadata.get('capitulos_processados', [])
