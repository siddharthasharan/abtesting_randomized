"""Persistence helpers for the pair coding IDE state."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Union

from .models import WorkspaceState


class StorageEngine:
    """Reads and writes workspace state to disk."""

    def __init__(self, path: Union[str, Path]):
        self.path = Path(path)

    def load_state(self) -> WorkspaceState:
        if not self.path.exists():
            return WorkspaceState()
        raw = json.loads(self.path.read_text())
        return WorkspaceState.from_dict(raw)

    def save_state(self, state: WorkspaceState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = state.to_dict()
        self.path.write_text(json.dumps(payload, indent=2))
