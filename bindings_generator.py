import os.path
import re
from pathlib import Path
from typing import List, Tuple

import requests


def parse_cgo_exported_functions(header_content: str) -> List[Tuple[str, Tuple[str, ...], str]]:
    content = re.sub(r'/\*.*?\*/', '', header_content, flags=re.DOTALL)
    content = re.sub(r'//.*', '', content)

    pattern = r'extern\s+__declspec\(dllexport\)\s+([\w\s*]+?)\s+(\w+)\s*\((.*?)\)\s*;'

    results = []

    for match in re.finditer(pattern, content, re.DOTALL):
        return_types = match.group(1).strip()
        func_name = match.group(2).strip()
        params_str = match.group(3).strip()

        param_types = []
        if params_str and params_str != 'void':
            param_decls = [p.strip() for p in params_str.split(',') if p.strip()]

            for decl in param_decls:
                parts = decl.split()
                if not parts:
                    continue

                type_parts = parts[:-1]
                param_type = ' '.join(type_parts).strip()

                if '*' in parts[-1] and not type_parts:
                    param_type = parts[-1].rstrip('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')

                param_types.append(param_type.strip())

        param_tuple = tuple(param_types) if param_types else ()

        results.append((func_name, param_tuple, return_types))

    return results


def to_python_function_name(c_name: str) -> str:
    if not c_name:
        return ""

    result = []
    for i, char in enumerate(c_name):
        if char.isupper():
            if i > 0:
                result.append('_')
            result.append(char.lower())
        else:
            result.append(char)

    return ''.join(result)


type_mapping = {
    "char*": "str",
    "int": "int",
}


def main():
    print("Downloading nknu core header file...")
    req = requests.get(
        "https://github.com/GDG-on-Campus-NKNU/NKNU-Core/releases/latest/download/windows_x86_64_nknu_core.h")
    extracted_functions = parse_cgo_exported_functions(req.text)
    print("Download finished. Generating nknu core binding file...")

    binding_content = [
        """from ctypes import cdll, c_void_p, string_at
import os
import json
from typing import Any
from base64 import b64decode
from pathlib import Path

core_path = Path(__file__).resolve().parent

_dll = cdll.LoadLibrary(os.path.join(core_path, "core.dll"))

"""
    ]

    parsed_funcs = []

    for func_name, param_tuple, return_type in extracted_functions:
        python_func = f"""
def {to_python_function_name(func_name)}({", ".join([f"arg{i}: {type_mapping[param_tuple[i]]}" for i in range(len(param_tuple))])}) -> Any:
    {"result_ptr = " if return_type != "void" else ""}_dll.{func_name}({", ".join([f"arg{i}" for i in range(len(param_tuple))])})"""
        if return_type != "void":
            python_func += f"""
    result_str = b64decode(string_at(result_ptr).decode("utf-8")).decode("utf-8")
    free(result_ptr)
    return result_str"""

        parsed_funcs.append(python_func)

        if len(param_tuple) > 0:
            binding_content.append(
                f"_dll.Free.argtypes = [{', '.join(["c_void_p" for _ in param_tuple])}]\n"
            )
        if len(return_type) > 0 and return_type != "void":
            binding_content.append(
                f"_dll.{func_name}.restype = c_void_p\n"
            )

    base_path = os.path.join(Path(__file__).resolve().parent, "nknu_core")

    with open(os.path.join(base_path, "bindings.py"), "w+") as f:
        f.write("".join([*binding_content, *parsed_funcs]))

    print("Downloading nknu core file...")
    req = requests.get(
        "https://github.com/GDG-on-Campus-NKNU/NKNU-Core/releases/latest/download/windows_x86_64_nknu_core.dll")

    with open(os.path.join(base_path, "core.dll"), "wb") as f:
        f.write(req.content)
    print("Download finished.")


if __name__ == '__main__':
    main()
