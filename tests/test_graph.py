import pytest
import onedrive_graph

@pytest.mark.parametrize("name, expected", [
    ("report.PDF", "Documents"),
    ("pic.png", "Images"),
    ("notes.txt", None),
])
def test_pick_folder(name, expected):
    assert onedrive_graph.pick_folder(name) == expected

def test_organise_moves_matched_file(monkeypatch):
    moved = []
    monkeypatch.setattr(onedrive_graph, "get_root_folders", lambda t: {"ML": "folder-id"})
    monkeypatch.setattr(onedrive_graph, "get_root_files", lambda t: [{"id": "f1", "name": "nn.pdf"}])
    monkeypatch.setattr(onedrive_graph, "groq_folder_match", lambda names, folders: {"nn.pdf": "ML"})
    monkeypatch.setattr(onedrive_graph, "move_file", lambda t, item, folder: moved.append((item, folder)) or True)

    msgs = onedrive_graph.organise_root("fake-token")

    assert moved == [("f1", "folder-id")]
    assert msgs == ["Moved nn.pdf -> ML"]