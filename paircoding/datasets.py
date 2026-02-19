"""Dataset registry utilities for collaborative analysis."""

from __future__ import annotations

import csv
import statistics
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Optional

from .models import DatasetReference


class DatasetNotFoundError(KeyError):
    """Raised when a dataset name is unknown."""


@dataclass
class Preview:
    """Lightweight preview of a dataset."""

    headers: List[str]
    rows: List[List[str]]


class DatasetRegistry:
    """Stores dataset metadata and simple statistical summaries."""

    def __init__(self, entries: Optional[Dict[str, DatasetReference]] = None):
        self._datasets: Dict[str, DatasetReference] = entries or {}

    def register(self, name: str, path: Path, description: str = "", format: str = "csv") -> DatasetReference:
        normalized_path = Path(path).expanduser().resolve()
        if not normalized_path.exists():
            raise FileNotFoundError(f"Dataset {name!r} not found at {normalized_path}")

        reference = DatasetReference(
            name=name,
            path=str(normalized_path),
            format=format,
            description=description,
        )
        self._datasets[name] = reference
        return reference

    def get(self, name: str) -> DatasetReference:
        try:
            return self._datasets[name]
        except KeyError as exc:  # noqa: PERF203 used for clarity
            raise DatasetNotFoundError(name) from exc

    def list(self) -> Iterable[DatasetReference]:
        return self._datasets.values()

    def preview_rows(self, name: str, limit: int = 5) -> Preview:
        reference = self.get(name)
        if reference.format.lower() != "csv":
            raise ValueError("Only CSV previews are supported")

        path = Path(reference.path)
        with path.open() as handle:
            reader = csv.reader(handle)
            headers = next(reader, [])
            rows = [row for _, row in zip(range(limit), reader)]
        return Preview(headers=headers, rows=rows)

    def column_summary(self, name: str) -> Dict[str, Dict[str, float]]:
        reference = self.get(name)
        if reference.format.lower() != "csv":
            raise ValueError("Only CSV summaries are supported")

        path = Path(reference.path)
        with path.open() as handle:
            reader = csv.DictReader(handle)
            columns: Dict[str, List[float]] = {header: [] for header in reader.fieldnames or []}
            for row in reader:
                for key, value in row.items():
                    try:
                        number = float(value)
                        columns[key].append(number)
                    except (TypeError, ValueError):
                        continue

        summary: Dict[str, Dict[str, float]] = {}
        for column, values in columns.items():
            if not values:
                continue
            summary[column] = {
                "min": min(values),
                "max": max(values),
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "count": float(len(values)),
            }
        return summary

    def to_state(self) -> Dict[str, DatasetReference]:
        return dict(self._datasets)
