"""High-level workspace orchestration for the pair coding IDE."""

from __future__ import annotations

import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Optional

from .datasets import DatasetRegistry
from .executor import ExecutionEngine
from .models import (
    Cell,
    ChatMessage,
    Collaborator,
    Notebook,
    Session,
    WorkspaceState,
)
from .storage import StorageEngine


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


class Workspace:
    """Coordinates notebooks, datasets, and pair-programming sessions."""

    def __init__(self, storage_path: Path | str = Path(".pairide/state.json"), *, auto_save: bool = True):
        self.storage = StorageEngine(storage_path)
        self.state: WorkspaceState = self.storage.load_state()
        self.datasets = DatasetRegistry(entries=self.state.datasets)
        self.executor = ExecutionEngine()
        self.auto_save = auto_save

    def _save(self) -> None:
        self.state.datasets = self.datasets.to_state()
        self.storage.save_state(self.state)

    def _maybe_save(self) -> None:
        if self.auto_save:
            self._save()

    def create_notebook(self, title: str, description: str = "") -> Notebook:
        notebook_id = str(uuid.uuid4())
        notebook = Notebook(id=notebook_id, title=title, description=description)
        self.state.notebooks[notebook_id] = notebook
        self._maybe_save()
        return notebook

    def add_cell(self, notebook_id: str, cell_type: str, source: str) -> Cell:
        notebook = self._get_notebook(notebook_id)
        cell = Cell(id=str(uuid.uuid4()), cell_type=cell_type, source=source)
        notebook.cells.append(cell)
        self._maybe_save()
        return cell

    def update_cell(self, notebook_id: str, cell_id: str, source: str) -> Cell:
        notebook = self._get_notebook(notebook_id)
        cell = self._get_cell(notebook, cell_id)
        cell.source = source
        self._maybe_save()
        return cell

    def create_session(
        self,
        name: str,
        notebook_id: str,
        collaborators: Optional[list[tuple[str, str]]] = None,
    ) -> Session:
        self._get_notebook(notebook_id)
        session_id = str(uuid.uuid4())
        collaborator_models = [
            Collaborator(id=str(uuid.uuid4()), name=person, role=role)
            for person, role in (collaborators or [])
        ]
        session = Session(
            id=session_id,
            name=name,
            notebook_id=notebook_id,
            collaborators=collaborator_models,
        )
        self.state.sessions[session_id] = session
        self._maybe_save()
        return session

    def add_collaborator(self, session_id: str, name: str, role: str = "navigator") -> Collaborator:
        session = self._get_session(session_id)
        collaborator = Collaborator(id=str(uuid.uuid4()), name=name, role=role)
        session.collaborators.append(collaborator)
        self._maybe_save()
        return collaborator

    def post_message(self, session_id: str, author: str, content: str) -> ChatMessage:
        session = self._get_session(session_id)
        message = ChatMessage(author=author, content=content, timestamp=_now())
        session.chat.append(message)
        self._maybe_save()
        return message

    def register_dataset(self, name: str, path: Path, description: str = "") -> None:
        self.datasets.register(name, path, description=description)
        self._maybe_save()

    def preview_dataset(self, name: str, limit: int = 5) -> dict:
        preview = self.datasets.preview_rows(name, limit=limit)
        return {"headers": preview.headers, "rows": preview.rows}

    def dataset_summary(self, name: str) -> dict:
        return self.datasets.column_summary(name)

    def run_cell(self, session_id: str, notebook_id: str, cell_id: str) -> Cell:
        session = self._get_session(session_id)
        if session.notebook_id != notebook_id:
            raise ValueError("Session is not attached to the given notebook")

        notebook = self._get_notebook(notebook_id)
        cell = self._get_cell(notebook, cell_id)
        result = self.executor.run_cell(session_id, cell, self.datasets)
        cell.last_result = result
        session.checkpoints.append(f"{cell.id}:{result.timestamp}")
        self._maybe_save()
        return cell

    def list_notebooks(self) -> Iterable[Notebook]:
        return self.state.notebooks.values()

    def list_sessions(self) -> Iterable[Session]:
        return self.state.sessions.values()

    def _get_notebook(self, notebook_id: str) -> Notebook:
        try:
            return self.state.notebooks[notebook_id]
        except KeyError as exc:  # noqa: PERF203 clarity
            raise KeyError(f"Unknown notebook {notebook_id}") from exc

    def _get_session(self, session_id: str) -> Session:
        try:
            return self.state.sessions[session_id]
        except KeyError as exc:  # noqa: PERF203 clarity
            raise KeyError(f"Unknown session {session_id}") from exc

    def _get_cell(self, notebook: Notebook, cell_id: str) -> Cell:
        for cell in notebook.cells:
            if cell.id == cell_id:
                return cell
        raise KeyError(f"Unknown cell {cell_id}")

    def save(self) -> None:
        self._save()
