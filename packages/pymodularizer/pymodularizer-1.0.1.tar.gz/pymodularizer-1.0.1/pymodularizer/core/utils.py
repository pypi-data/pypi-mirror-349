def slugify(name: str) -> str:
    return name.strip().lower().replace(" ", "_")

def validate_choice(choices: list, idx: int) -> str:
    try:
        return choices[idx]
    except IndexError:
        raise ValueError("Escolha inválida")

def get_default_structure(src: str, main: str) -> dict:
    return {
        src: {
            "__init__.py": "",
            main: f"# Arquivo principal: {main}\n"
        },
        "tests": {
            "__init__.py": "",
            f"test_{main.replace('.py', '')}.py": "# Teste inicial\n"
        },
        "projectgen": {
            "__init__.py": "",
            "core": {
                "__init__.py": "",
                "generator.py": "# Lógica de criação\n",
                "templates.py": "# Templates\n",
                "helpers": {
                    "__init__.py": "",
                    "module.py": "# Lógica de criação de módulos\n",
                    "utils.py": "# Funções utilitárias\n"
                }
            }
        }
    }
