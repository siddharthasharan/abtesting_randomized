"""Data models for the pair coding IDE workspace."""

from __future__ import annotations

import dataclasses
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class Collaborator:
    """Represents a participant in a collaboration session."""

    id: str
    name: str
    role: str = "navigator"

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Collaborator":
        return cls(**data)


@dataclass
class ChatMessage:
    """A simple chat message shared in a session."""

    author: str
    content: str
    timestamp: str

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ChatMessage":
        return cls(**data)


@dataclass
class ExecutionResult:
    """Result of executing a cell."""

    success: bool
    stdout: str
    error: Optional[str]
    duration: float
    timestamp: str
    variables: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ExecutionResult":
        return cls(**data)


@dataclass
class Cell:
    """A notebook cell."""

    id: str
    cell_type: str
    source: str
    last_result: Optional[ExecutionResult] = None

    def to_dict(self) -> Dict[str, Any]:
        payload = dataclasses.asdict(self)
        if self.last_result:
            payload["last_result"] = self.last_result.to_dict()
        return payload

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Cell":
        last_result_data = data.get("last_result")
        last_result = None
        if last_result_data:
            last_result = ExecutionResult.from_dict(last_result_data)
        return cls(
            id=data["id"],
            cell_type=data.get("cell_type", "code"),
            source=data.get("source", ""),
            last_result=last_result,
        )


@dataclass
class Notebook:
    """A collaborative notebook with ordered cells."""

    id: str
    title: str
    description: str
    cells: List[Cell] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "cells": [cell.to_dict() for cell in self.cells],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Notebook":
        return cls(
            id=data["id"],
            title=data.get("title", "Untitled Notebook"),
            description=data.get("description", ""),
            cells=[Cell.from_dict(item) for item in data.get("cells", [])],
        )


@dataclass
class DatasetReference:
    """Metadata describing a dataset that collaborators can share."""

    name: str
    path: str
    format: str = "csv"
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return dataclasses.asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatasetReference":
        return cls(**data)


@dataclass
class Session:
    """A collaboration session binds people and notebooks together."""

    id: str
    name: str
    notebook_id: str
    collaborators: List[Collaborator] = field(default_factory=list)
    chat: List[ChatMessage] = field(default_factory=list)
    checkpoints: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "notebook_id": self.notebook_id,
            "collaborators": [person.to_dict() for person in self.collaborators],
            "chat": [message.to_dict() for message in self.chat],
            "checkpoints": list(self.checkpoints),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Session":
        return cls(
            id=data["id"],
            name=data.get("name", "Session"),
            notebook_id=data["notebook_id"],
            collaborators=[
                Collaborator.from_dict(item) for item in data.get("collaborators", [])
            ],
            chat=[ChatMessage.from_dict(item) for item in data.get("chat", [])],
            checkpoints=list(data.get("checkpoints", [])),
        )


@dataclass
class WorkspaceState:
    """Persisted representation of the IDE workspace."""

    notebooks: Dict[str, Notebook] = field(default_factory=dict)
    sessions: Dict[str, Session] = field(default_factory=dict)
    datasets: Dict[str, DatasetReference] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "notebooks": {key: value.to_dict() for key, value in self.notebooks.items()},
            "sessions": {key: value.to_dict() for key, value in self.sessions.items()},
            "datasets": {key: value.to_dict() for key, value in self.datasets.items()},
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorkspaceState":
        notebooks = {
            key: Notebook.from_dict(value) for key, value in data.get("notebooks", {}).items()
        }
        sessions = {
            key: Session.from_dict(value) for key, value in data.get("sessions", {}).items()
        }
        datasets = {
            key: DatasetReference.from_dict(value)
            for key, value in data.get("datasets", {}).items()
        }
        return cls(notebooks=notebooks, sessions=sessions, datasets=datasets)
