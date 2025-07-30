def create_module(name: str, base_path: str = "src"):
    import os
    module_path = os.path.join(base_path, name)
    os.makedirs(module_path, exist_ok=True)

    init_path = os.path.join(module_path, "__init__.py")
    file_path = os.path.join(module_path, f"{name}.py")

    with open(init_path, "w"): pass
    with open(file_path, "w") as f:
        f.write(f"# Módulo {name}\n")
