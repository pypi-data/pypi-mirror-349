import os
from pymodularizer.core.generator import create_structure  # Use o caminho absoluto do pacote

def test_create_structure(tmp_path):
    structure = {
        "folder/": {
            "file.py": "print('Hello')"
        }
    }

    create_structure(tmp_path, structure)

    file_path = tmp_path / "folder" / "file.py"

    assert file_path.exists()
    assert file_path.read_text() == "print('Hello')"
