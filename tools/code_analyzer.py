import ast
import autopep8

def analyze_code_structure(code: str):
    try:
        tree = ast.parse(code)
        functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
        classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        return {
            "functions": functions,
            "classes": classes
        }
    except Exception as e:
        return {"error": str(e)}

def format_code(code: str):
    try:
        return autopep8.fix_code(code)
    except Exception as e:
        return f"Formatting failed: {e}"
