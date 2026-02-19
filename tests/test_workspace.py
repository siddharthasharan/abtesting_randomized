from pathlib import Path

from paircoding.workspace import Workspace


def test_create_and_run_cell(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    workspace = Workspace(state_path)

    notebook = workspace.create_notebook("Exploration", "Testing notebook")
    cell = workspace.add_cell(notebook.id, "code", "value = 21 * 2\nprint(value)")
    session = workspace.create_session("Pairing", notebook.id, [("Kai", "driver")])

    updated_cell = workspace.run_cell(session.id, notebook.id, cell.id)

    assert updated_cell.last_result
    assert updated_cell.last_result.success is True
    assert "42" in updated_cell.last_result.stdout
    assert updated_cell.last_result.error is None

    reloaded = Workspace(state_path)
    persisted_cell = reloaded.state.notebooks[notebook.id].cells[0]
    assert persisted_cell.last_result
    assert persisted_cell.last_result.variables == ["value"]


def test_dataset_preview_and_summary(tmp_path: Path) -> None:
    csv_path = tmp_path / "data.csv"
    csv_path.write_text("col1,col2\n1,5\n2,6\n3,7\n")

    workspace = Workspace(tmp_path / "state.json")
    workspace.register_dataset("sample", csv_path, description="Example data")

    preview = workspace.preview_dataset("sample", limit=2)
    assert preview["headers"] == ["col1", "col2"]
    assert len(preview["rows"]) == 2

    summary = workspace.dataset_summary("sample")
    assert summary["col1"]["min"] == 1.0
    assert summary["col2"]["max"] == 7.0


def test_chat_and_collaborators(tmp_path: Path) -> None:
    state_path = tmp_path / "state.json"
    workspace = Workspace(state_path)

    notebook = workspace.create_notebook("Chat Notebook")
    session = workspace.create_session("Analysts", notebook.id)

    collaborator = workspace.add_collaborator(session.id, "Sky", role="navigator")
    assert collaborator.name == "Sky"

    message = workspace.post_message(session.id, "Sky", "Looking at the data")
    assert message.content.startswith("Looking")

    restored = Workspace(state_path)
    restored_session = restored.state.sessions[session.id]
    assert restored_session.collaborators[0].name == "Sky"
    assert restored_session.chat[0].content == "Looking at the data"
