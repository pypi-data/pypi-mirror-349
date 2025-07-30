import typer
from pathlib import Path
from .generator import create_structure
from ..helpers.module import create_module
from .utils import get_default_structure

app = typer.Typer(help="Gerador de projetos Python modularizados.")

@app.command()
def new(
    name: str = typer.Option("meu_projeto", help="Nome do projeto"),
    version: str = typer.Option("0.1.0", help="Versão do projeto"),
    src: str = typer.Option("src", help="Nome da pasta de código fonte"),
    main: str = typer.Option("main.py", help="Nome do arquivo principal"),
    type: str = typer.Option("custom", help="Tipo do projeto: custom, simple_script, python_package, modular_application, fastapi_api, flask_api, kyvi_app")
):
    """Cria um novo projeto Python."""
    import json
    from pathlib import Path
    project_path = Path(name)
    project_path.mkdir(parents=True, exist_ok=True)

    # Suporte a tipos customizados via arquivos JSON em models
    if type in ["kyvi_app", "fastapi_api", "flask_api", "modular_application", "python_package", "simple_script"]:
        model_path = Path(__file__).parent.parent / "models" / f"{type}.json"
        if model_path.exists():
            with open(model_path, encoding="utf-8") as f:
                data = json.load(f)
                structure = data[type]["structure"]
        else:
            typer.echo(f"❌ Modelo '{type}' não encontrado em models.")
            raise typer.Exit(code=1)
    elif type == "custom":
        structure = get_default_structure(src, main)
    else:
        typer.echo("❌ Tipo de projeto inválido. Use 'custom' ou um dos tipos predefinidos.")
        raise typer.Exit(code=1)

    create_structure(project_path, structure)

    typer.echo(f"✅ Projeto '{name}' do tipo '{type}' criado com sucesso!")

@app.command()
def module(
    name: str = typer.Argument(..., help="Nome do módulo"),
    path: str = typer.Option("src", help="Pasta onde o módulo será criado")
):
    """Cria um novo módulo dentro da pasta fonte."""
    from pathlib import Path
    if not Path(path).exists():
        typer.echo(f"❌ O caminho '{path}' não existe. Crie o projeto primeiro.")
        raise typer.Exit(code=1)
    create_module(name, path)
    typer.echo(f"📦 Módulo '{name}' criado dentro de '{path}'")

@app.command()
def list_templates():
    """
    Lista os tipos de projeto disponíveis no gerador.
    """
    import os
    models_path = Path(__file__).parent.parent / "models"
    typer.echo("\n📦 Tipos de projeto disponíveis:\n")
    for file in os.listdir(models_path):
        if file.endswith(".json"):
            with open(models_path / file, encoding="utf-8") as f:
                import json
                data = json.load(f)
                for name, meta in data.items():
                    typer.echo(f"🔹 {name} - {meta.get('description', '')}")

@app.command()
def project_types():
    """
    Mostra os tipos de projeto disponíveis para criação.
    """
    import os
    import json
    models_path = Path(__file__).parent.parent / "models"
    typer.echo("\n📦 Tipos de projeto disponíveis para --type:\n")
    for file in os.listdir(models_path):
        if file.endswith(".json"):
            with open(models_path / file, encoding="utf-8") as f:
                data = json.load(f)
                for name, meta in data.items():
                    typer.echo(f"🔹 {name} - {meta.get('description', '')}")


