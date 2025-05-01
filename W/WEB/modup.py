import ast
import subprocess
import sys

def get_imports(script_path):
    """Extracts all imported modules from a Python script."""
    with open(script_path, "r", encoding="utf-8") as file:
        tree = ast.parse(file.read(), script_path)

    imports = {name.name for node in ast.walk(tree) if isinstance(node, ast.Import) for name in node.names}
    imports |= {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}

    return sorted(imports)

def install_missing_modules(modules):
    """Installs modules that aren't already installed."""
    for module in modules:
        try:
            __import__(module)  # Check if module is installed
        except ImportError:
            print(f"Installing {module}...")
            subprocess.run([sys.executable, "-m", "pip", "install", module])

abc = input("script path: ")

if __name__ == "__main__":
    script_path = abc  # Replace with your actual script path
    required_modules = get_imports(script_path)
    install_missing_modules(required_modules)
    print("All missing modules have been installed!")
