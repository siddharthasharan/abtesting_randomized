# Pair Coding IDE for Data Science

This repository provides a lightweight foundation for building a collaborative, pair-programming IDE tailored for data science work. It focuses on the core primitives you need to coordinate notebooks, collaborators, datasets, and repeatable execution—all backed by a simple JSON workspace.

## What’s included

- **Workspace orchestration**: Manage notebooks, sessions, and collaborators with the `paircoding` package.
- **Cell execution engine**: Run code cells per session with isolated namespaces and captured output.
- **Dataset registry**: Register CSV datasets, preview rows, and compute quick numeric summaries without heavy dependencies.
- **CLI tools**: Scriptable commands to bootstrap workspaces, add cells, execute code, chat with teammates, and inspect datasets.
- **Tests**: Pytest coverage for the critical workflows (notebook execution, dataset handling, and collaboration metadata).

## Quick start

1. Create and activate a virtual environment (optional but recommended).
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Initialize a workspace and create a notebook:

   ```bash
   python -m paircoding.cli init --title "Exploration" --description "Joint analysis scratchpad"
   ```

   The command prints the new notebook ID and stores state at `.pairide/state.json` by default.

4. Start a collaboration session and add a code cell:

   ```bash
   python -m paircoding.cli create-session "Morning pairing" <NOTEBOOK_ID>
   python -m paircoding.cli add-cell <NOTEBOOK_ID> code --source "print('hello collaborators')"
   ```

5. Execute the cell inside the session:

   ```bash
   python -m paircoding.cli run-cell <SESSION_ID> <NOTEBOOK_ID> <CELL_ID>
   ```

6. Register and preview a dataset:

   ```bash
   python -m paircoding.cli register-dataset flights data/flights.csv --description "Aggregated flight stats"
   python -m paircoding.cli preview-dataset flights --limit 3
   ```

## Package overview

- `paircoding/models.py` — Dataclasses for notebooks, cells, sessions, collaborators, execution results, and datasets.
- `paircoding/storage.py` — JSON persistence for the workspace state.
- `paircoding/datasets.py` — CSV preview and numeric summaries for registered datasets.
- `paircoding/executor.py` — Simple execution engine with isolated namespaces per session.
- `paircoding/workspace.py` — High-level orchestration of notebooks, sessions, datasets, and execution.
- `paircoding/cli.py` — Command-line interface for common workflows.

## Running the test suite

After installing dependencies, run:

```bash
python -m pytest
```

The tests exercise notebook execution, dataset previews, and collaboration metadata to ensure the core workflows stay reliable as the IDE evolves.
