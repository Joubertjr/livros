"""
Progress tracking system with Server-Sent Events (SSE) support.
"""
import asyncio
import json
from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class ProgressState:
    """State of a progress session."""
    session_id: str
    stage: str
    percentage: int
    message: str
    complete: bool = False
    result: Optional[Dict[str, Any]] = None
    created_at: datetime = None
    updated_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
        if self.updated_at is None:
            self.updated_at = datetime.now()


class ProgressTracker:
    """
    Manages progress tracking for summarization sessions with SSE support.

    Thread-safe progress updates with automatic cleanup of old sessions.
    """

    def __init__(self, ttl_hours: int = 1):
        """
        Initialize progress tracker.

        Args:
            ttl_hours: Time-to-live for sessions in hours (default: 1)
        """
        self.sessions: Dict[str, ProgressState] = {}
        self.queues: Dict[str, asyncio.Queue] = {}
        self.ttl_hours = ttl_hours

    def create_session(self, session_id: str) -> None:
        """
        Create a new progress tracking session.

        Args:
            session_id: Unique identifier for the session
        """
        self.sessions[session_id] = ProgressState(
            session_id=session_id,
            stage="initializing",
            percentage=0,
            message="Inicializando..."
        )
        self.queues[session_id] = asyncio.Queue()

    def update_progress(
        self,
        session_id: str,
        stage: str,
        percentage: int,
        message: str
    ) -> None:
        """
        Update progress for a session.

        Args:
            session_id: Session identifier
            stage: Current stage (reading, processing, validating, etc.)
            percentage: Progress percentage (0-100)
            message: Human-readable progress message
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        self.sessions[session_id].stage = stage
        self.sessions[session_id].percentage = min(100, max(0, percentage))
        self.sessions[session_id].message = message
        self.sessions[session_id].updated_at = datetime.now()

        # Enqueue update for SSE streaming
        if session_id in self.queues:
            try:
                self.queues[session_id].put_nowait({
                    "stage": stage,
                    "percentage": percentage,
                    "message": message,
                    "complete": False
                })
            except asyncio.QueueFull:
                pass  # Skip if queue is full

    def mark_complete(self, session_id: str, result: Optional[Dict] = None) -> None:
        """
        Mark a session as complete.

        Args:
            session_id: Session identifier
            result: Optional result data to store
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        self.sessions[session_id].complete = True
        self.sessions[session_id].result = result
        self.sessions[session_id].updated_at = datetime.now()

        # Send final update
        if session_id in self.queues:
            try:
                self.queues[session_id].put_nowait({
                    "stage": "complete",
                    "percentage": 100,
                    "message": "Processamento concluído!",
                    "complete": True
                })
            except asyncio.QueueFull:
                pass

    def mark_error(self, session_id: str, error_message: str, error_result: Optional[Dict] = None) -> None:
        """
        Mark a session as failed with error.

        Args:
            session_id: Session identifier
            error_message: Error description
            error_result: Optional error result to store (for API retrieval)
        """
        # Se sessão não existe, criar uma para preservar o erro
        if session_id not in self.sessions:
            print(f"[ProgressTracker] Session {session_id} not found, creating error session")
            self.sessions[session_id] = ProgressState(
                session_id=session_id,
                stage="error",
                percentage=0,
                message=error_message
            )
            self.queues[session_id] = asyncio.Queue()

        self.sessions[session_id].stage = "error"
        self.sessions[session_id].message = error_message
        self.sessions[session_id].complete = True
        self.sessions[session_id].updated_at = datetime.now()
        
        # Armazenar resultado de erro se fornecido
        if error_result:
            self.sessions[session_id].result = error_result

        # Send error update
        if session_id in self.queues:
            try:
                self.queues[session_id].put_nowait({
                    "stage": "error",
                    "percentage": self.sessions[session_id].percentage,
                    "message": error_message,
                    "complete": True,
                    "error": True
                })
            except asyncio.QueueFull:
                pass

    def get_state(self, session_id: str) -> Optional[ProgressState]:
        """
        Get current state of a session.

        Args:
            session_id: Session identifier

        Returns:
            ProgressState if session exists, None otherwise
        """
        return self.sessions.get(session_id)

    def _serialize_state(self, state: ProgressState) -> dict:
        """Serialize ProgressState to JSON-compatible dict."""
        return {
            "session_id": state.session_id,
            "stage": state.stage,
            "percentage": state.percentage,
            "message": state.message,
            "complete": state.complete
        }

    async def stream_progress(self, session_id: str):
        """
        SSE generator for streaming progress updates.

        Args:
            session_id: Session identifier

        Yields:
            Server-Sent Event formatted strings
        """
        print(f"[SSE] Starting stream for session {session_id}")

        if session_id not in self.sessions:
            print(f"[SSE] Session {session_id} not found")
            yield f"data: {json.dumps({'error': 'Session not found'})}\n\n"
            return

        queue = self.queues.get(session_id)
        if not queue:
            print(f"[SSE] No queue for session {session_id}")
            yield f"data: {json.dumps({'error': 'No queue for session'})}\n\n"
            return

        # Send current state immediately
        state = self.sessions[session_id]
        initial_data = self._serialize_state(state)
        # Incluir session_id no estado inicial
        initial_data["session_id"] = session_id
        print(f"[SSE] Sending initial state: {initial_data}")
        yield f"data: {json.dumps(initial_data)}\n\n"

        # Stream updates
        while True:
            try:
                # Wait for update with timeout (aumentado para 60s para processamentos longos)
                update = await asyncio.wait_for(queue.get(), timeout=60.0)
                # Incluir session_id em todas as atualizações
                update["session_id"] = session_id
                print(f"[SSE] Sending update: {update}")
                yield f"data: {json.dumps(update)}\n\n"

                # Break if complete
                if update.get("complete"):
                    print(f"[SSE] Stream complete for session {session_id}")
                    break

            except asyncio.TimeoutError:
                # Send keepalive
                print(f"[SSE] Sending keepalive for session {session_id}")
                yield f": keepalive\n\n"

                # Check if session completed while waiting
                if session_id in self.sessions and self.sessions[session_id].complete:
                    final_update = {
                        "session_id": session_id,
                        "stage": self.sessions[session_id].stage,
                        "percentage": self.sessions[session_id].percentage,
                        "message": self.sessions[session_id].message,
                        "complete": True
                    }
                    if self.sessions[session_id].stage == "error":
                        final_update["error"] = True
                    print(f"[SSE] Sending final update: {final_update}")
                    yield f"data: {json.dumps(final_update)}\n\n"
                    break
            except Exception as e:
                # Handle unexpected errors in SSE stream
                print(f"[SSE] Error in stream for session {session_id}: {e}")
                import traceback
                traceback.print_exc()
                
                # Verificar se a sessão foi completada enquanto ocorria o erro
                if session_id in self.sessions and self.sessions[session_id].complete:
                    final_update = {
                        "session_id": session_id,
                        "stage": self.sessions[session_id].stage,
                        "percentage": self.sessions[session_id].percentage,
                        "message": self.sessions[session_id].message,
                        "complete": True
                    }
                    if self.sessions[session_id].stage == "error":
                        final_update["error"] = True
                    print(f"[SSE] Sending final update after stream error: {final_update}")
                    yield f"data: {json.dumps(final_update)}\n\n"
                else:
                    # Se não está completa, enviar erro de stream
                    error_data = {
                        "session_id": session_id,
                        "error": True,
                        "message": f"Erro no stream: {str(e)}",
                        "complete": True
                    }
                    yield f"data: {json.dumps(error_data)}\n\n"
                break

    def cleanup_old_sessions(self) -> int:
        """
        Remove sessions older than TTL.

        Returns:
            Number of sessions removed
        """
        now = datetime.now()
        cutoff = now - timedelta(hours=self.ttl_hours)

        to_remove = [
            sid for sid, state in self.sessions.items()
            if state.updated_at < cutoff
        ]

        for sid in to_remove:
            del self.sessions[sid]
            if sid in self.queues:
                del self.queues[sid]

        return len(to_remove)


# Global progress tracker instance
_progress_tracker: Optional[ProgressTracker] = None


def get_progress_tracker() -> ProgressTracker:
    """Get or create the global progress tracker instance."""
    global _progress_tracker
    if _progress_tracker is None:
        _progress_tracker = ProgressTracker()
    return _progress_tracker
