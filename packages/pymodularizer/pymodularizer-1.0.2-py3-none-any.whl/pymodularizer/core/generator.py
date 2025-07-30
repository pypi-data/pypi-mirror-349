import os

def create_structure(base_path, structure):
    for name, content in structure.items():
        # Corrige para garantir que o path seja sempre absoluto
        path = os.path.join(str(base_path), name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            # Garante que o diretório do arquivo existe
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
