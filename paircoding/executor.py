"""Code execution utilities for collaborative notebooks."""

from __future__ import annotations

import io
from contextlib import redirect_stdout
from datetime import datetime, timezone
from time import perf_counter
from typing import Dict

from .datasets import DatasetRegistry
from .models import Cell, ExecutionResult


class ExecutionEngine:
    """Runs notebook cells in isolated namespaces per session."""

    def __init__(self) -> None:
        self._namespaces: Dict[str, Dict[str, object]] = {}

    def _safe_builtins(self) -> Dict[str, object]:
        allowed = {
            "abs": abs,
            "min": min,
            "max": max,
            "sum": sum,
            "len": len,
            "range": range,
            "enumerate": enumerate,
            "sorted": sorted,
            "print": print,
            "map": map,
            "filter": filter,
            "zip": zip,
        }
        return allowed

    def run_cell(self, session_id: str, cell: Cell, datasets: DatasetRegistry) -> ExecutionResult:
        if cell.cell_type != "code":
            return ExecutionResult(
                success=True,
                stdout=cell.source,
                error=None,
                duration=0.0,
                timestamp=datetime.now(timezone.utc).isoformat(),
                variables=[],
            )

        namespace = self._namespaces.setdefault(
            session_id,
            {"__builtins__": self._safe_builtins(), "datasets": datasets},
        )

        buffer = io.StringIO()
        start = perf_counter()
        error_message = None
        try:
            with redirect_stdout(buffer):
                exec(cell.source, namespace)
        except Exception as exc:  # noqa: PERF203 raised for clarity
            error_message = f"{exc.__class__.__name__}: {exc}"
        duration = perf_counter() - start

        variable_names = sorted(
            key
            for key, value in namespace.items()
            if not key.startswith("__")
            and key not in {"datasets"}
            and not callable(value)
        )

        return ExecutionResult(
            success=error_message is None,
            stdout=buffer.getvalue(),
            error=error_message,
            duration=duration,
            timestamp=datetime.now(timezone.utc).isoformat(),
            variables=variable_names,
        )

    def reset(self, session_id: str) -> None:
        self._namespaces.pop(session_id, None)
