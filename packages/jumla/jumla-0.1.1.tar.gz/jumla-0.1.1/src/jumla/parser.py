import ast

from typing import Dict, List, Tuple


class Parser:
    TYPE_MAPPING = {
        "int": "Int",
        "float": "Float",
        "bool": "Bool",
        "str": "String",
        "None": "Unit",
        "Any": "Type",
    }

    def __init__(self, function: str):
        self.function = function

    def extract_function_signature(self) -> Tuple[str, List[Dict[str, str]], str]:
        try:
            tree = ast.parse(self.function)
            func_def = tree.body[0]

            if not isinstance(func_def, ast.FunctionDef):
                raise ValueError("Not a valid function")

            function_name = func_def.name

            params = []
            for arg in func_def.args.args:
                raw_type = "Any"
                if arg.annotation:
                    raw_type = ast.unparse(arg.annotation)
                lean_type = self.TYPE_MAPPING.get(raw_type, "Type")
                params.append({"param_name": arg.arg, "param_type": lean_type})

            raw_return_type = "Any"
            if func_def.returns:
                raw_return_type = ast.unparse(func_def.returns)

            lean_return_type = self.TYPE_MAPPING.get(raw_return_type, "Type")

            return function_name, params, lean_return_type

        except Exception as e:
            raise ValueError(f"Failed to parse function: {e}")
