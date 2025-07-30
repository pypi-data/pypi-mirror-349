import pytest
from pymodularizer.core.templates import project_templates

def test_project_types_have_description_and_structure():
    types = project_templates.get("project_types", {})
    assert types, "Nenhum tipo de projeto definido em templates."

    for key, data in types.items():
        assert "description" in data, f"O tipo '{key}' não possui descrição."
        assert "structure" in data, f"O tipo '{key}' não possui estrutura definida."
        assert isinstance(data["structure"], dict), f"A estrutura de '{key}' deve ser um dicionário."

def test_common_files_exist():
    common_files = project_templates.get("common_files", [])
    expected = ["README.md", "pyproject.toml", "setup.cfg", "requirements.txt", ".gitignore", ".env.example"]
    for f in expected:
        assert f in common_files, f"{f} deveria estar em common_files"
