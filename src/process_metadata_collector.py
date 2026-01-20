"""
Coletor de metadados do processo de sumarização.

Gate Z10: Clean Code - responsabilidade única: coletar dados do processo.
Regra Canônica: "Processo que não deixa rastro não é produto, é experimento descartável."
"""

from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass, field, asdict


@dataclass
class RegenerationAttempt:
    """Dados de uma tentativa de regeneração de resumo."""
    attempt_number: int
    timestamp: str
    missing_markers: List[str]
    prompt_strategy: str = "standard"  # "standard" | "enhanced"
    temperature: float = 0.3
    result: str = "failed"  # "failed" | "passed"
    summary_preview: Optional[str] = None  # Primeiros 200 chars


@dataclass
class AddendumAttempt:
    """Dados de uma tentativa de addendum."""
    attempt_number: int
    timestamp: str
    missing_item_ids: List[str]
    prompt_strategy: str = "direct"  # "direct" | "fallback"
    temperature: float = 0.1
    addendum_content: str = ""
    validation_passed: bool = False
    validation_missing: List[str] = field(default_factory=list)
    result: str = "failed"  # "failed" | "passed"


@dataclass
class ChapterProcessData:
    """Dados completos do processamento de um capítulo."""
    chapter_number: str
    chapter_title: str
    regeneration_attempts: List[RegenerationAttempt] = field(default_factory=list)
    addendum_attempts: List[AddendumAttempt] = field(default_factory=list)
    final_regeneration_count: int = 0
    final_addendum_count: int = 0
    final_missing_markers: List[str] = field(default_factory=list)


@dataclass
class ProcessLog:
    """Log estruturado do processo."""
    timestamp: str
    level: str  # "INFO" | "WARNING" | "ERROR" | "DEBUG"
    chapter: Optional[str] = None
    message: str = ""


class ProcessMetadataCollector:
    """
    Coletor de metadados do processo de sumarização.
    
    Coleta todos os dados do processo para rastreabilidade completa:
    - Tentativas de regeneração (prompts, temperaturas, resultados)
    - Tentativas de addendum (conteúdo, validações, estratégias)
    - Logs detalhados de cada capítulo
    - Métricas de processamento
    """
    
    def __init__(self):
        """Inicializa o coletor."""
        self.chapters: Dict[str, ChapterProcessData] = {}
        self.logs: List[ProcessLog] = []
        self.start_time: Optional[datetime] = None
        self.end_time: Optional[datetime] = None
    
    def start_process(self) -> None:
        """Marca início do processo."""
        self.start_time = datetime.now()
        self.log("INFO", None, "Processo de sumarização iniciado")
    
    def end_process(self) -> None:
        """Marca fim do processo."""
        self.end_time = datetime.now()
        self.log("INFO", None, "Processo de sumarização concluído")
    
    def get_chapter_data(self, chapter_number: str, chapter_title: str = "") -> ChapterProcessData:
        """
        Obtém ou cria dados de processamento de um capítulo.
        
        Args:
            chapter_number: Número do capítulo
            chapter_title: Título do capítulo
            
        Returns:
            ChapterProcessData para o capítulo
        """
        if chapter_number not in self.chapters:
            self.chapters[chapter_number] = ChapterProcessData(
                chapter_number=chapter_number,
                chapter_title=chapter_title
            )
        return self.chapters[chapter_number]
    
    def log_regeneration_attempt(
        self,
        chapter_number: str,
        attempt_number: int,
        missing_markers: List[str],
        temperature: float = 0.3,
        prompt_strategy: str = "standard",
        result: str = "failed",
        summary_preview: Optional[str] = None
    ) -> None:
        """
        Registra uma tentativa de regeneração.
        
        Args:
            chapter_number: Número do capítulo
            attempt_number: Número da tentativa
            missing_markers: Lista de marcadores faltantes
            temperature: Temperatura usada
            prompt_strategy: Estratégia do prompt
            result: Resultado ("failed" | "passed")
            summary_preview: Preview do resumo gerado (primeiros 200 chars)
        """
        chapter_data = self.get_chapter_data(chapter_number)
        attempt = RegenerationAttempt(
            attempt_number=attempt_number,
            timestamp=datetime.now().isoformat(),
            missing_markers=missing_markers,
            prompt_strategy=prompt_strategy,
            temperature=temperature,
            result=result,
            summary_preview=summary_preview[:200] if summary_preview else None
        )
        chapter_data.regeneration_attempts.append(attempt)
        
        self.log(
            "INFO" if result == "passed" else "WARNING",
            chapter_number,
            f"Tentativa {attempt_number} de regeneração: {result}, {len(missing_markers)} marcadores faltando"
        )
    
    def log_addendum_attempt(
        self,
        chapter_number: str,
        attempt_number: int,
        missing_item_ids: List[str],
        addendum_content: str,
        prompt_strategy: str = "direct",
        temperature: float = 0.1,
        validation_passed: bool = False,
        validation_missing: Optional[List[str]] = None,
        result: str = "failed"
    ) -> None:
        """
        Registra uma tentativa de addendum.
        
        Args:
            chapter_number: Número do capítulo
            attempt_number: Número da tentativa
            missing_item_ids: IDs dos itens faltantes
            addendum_content: Conteúdo do addendum gerado
            prompt_strategy: Estratégia do prompt ("direct" | "fallback")
            temperature: Temperatura usada
            validation_passed: Se validação prévia passou
            validation_missing: Itens faltantes na validação
            result: Resultado ("failed" | "passed")
        """
        chapter_data = self.get_chapter_data(chapter_number)
        attempt = AddendumAttempt(
            attempt_number=attempt_number,
            timestamp=datetime.now().isoformat(),
            missing_item_ids=missing_item_ids,
            prompt_strategy=prompt_strategy,
            temperature=temperature,
            addendum_content=addendum_content,
            validation_passed=validation_passed,
            validation_missing=validation_missing or [],
            result=result
        )
        chapter_data.addendum_attempts.append(attempt)
        
        self.log(
            "INFO" if result == "passed" else "WARNING",
            chapter_number,
            f"Tentativa {attempt_number} de addendum: {result}, validação: {validation_passed}"
        )
    
    def finalize_chapter(
        self,
        chapter_number: str,
        regeneration_count: int,
        addendum_count: int,
        final_missing_markers: List[str]
    ) -> None:
        """
        Finaliza dados de um capítulo.
        
        Args:
            chapter_number: Número do capítulo
            regeneration_count: Contagem final de regenerações
            addendum_count: Contagem final de addendums
            final_missing_markers: Marcadores faltantes finais
        """
        chapter_data = self.get_chapter_data(chapter_number)
        chapter_data.final_regeneration_count = regeneration_count
        chapter_data.final_addendum_count = addendum_count
        chapter_data.final_missing_markers = final_missing_markers
    
    def log(self, level: str, chapter: Optional[str], message: str) -> None:
        """
        Registra um log.
        
        Args:
            level: Nível do log ("INFO" | "WARNING" | "ERROR" | "DEBUG")
            chapter: Número do capítulo (opcional)
            message: Mensagem do log
        """
        log_entry = ProcessLog(
            timestamp=datetime.now().isoformat(),
            level=level,
            chapter=chapter,
            message=message
        )
        self.logs.append(log_entry)
    
    def to_dict(self) -> Dict:
        """
        Converte coletor para dicionário (para persistência).
        
        Returns:
            Dicionário com todos os dados coletados
        """
        return {
            "chapters": [
                asdict(chapter_data) for chapter_data in self.chapters.values()
            ],
            "logs": [asdict(log) for log in self.logs],
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": (
                (self.end_time - self.start_time).total_seconds()
                if self.start_time and self.end_time else None
            )
        }
