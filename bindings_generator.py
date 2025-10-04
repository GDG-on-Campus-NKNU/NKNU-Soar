import os
import re

import requests


def extract_exported_signatures(text: str):
    pattern = re.compile(
        r'extern\s+__declspec\s*\(\s*dllexport\s*\)\s*([^;]+;)',
        re.IGNORECASE | re.DOTALL
    )
    return [m.strip() for m in pattern.findall(text)]


def strip_param_names(signature: str) -> str:
    sig = signature.strip()
    if not sig.endswith(';'):
        sig += ';'
    p_open = sig.find('(')
    p_close = sig.rfind(')')
    if p_open == -1 or p_close == -1:
        return sig
    prefix = sig[:p_open].strip()
    args_str = sig[p_open + 1:p_close].strip()
    if args_str == '' or args_str.lower() == 'void':
        return f"{prefix}();"
    args = []
    for arg in args_str.split(','):
        tokens = arg.strip().split()
        if not tokens:
            continue
        if '*' in arg:
            args.append("char*")
        else:
            args.append(tokens[0])
    return f"{prefix}({', '.join(args)});"


def parse_func(signature: str):
    sig = signature.strip().rstrip(';')
    m = re.match(r'(.+?)\s+(\w+)\s*\((.*)\)', sig)
    if not m:
        return None
    ret_type, name, args = m.groups()
    args = [a.strip() for a in args.split(',') if a.strip() and a.strip() != 'void']
    return ret_type.strip(), name.strip(), args


def map_ctype_to_pyhint(ctype: str) -> str:
    if "char*" in ctype:
        return "str | bytes"
    elif "int" in ctype or "long" in ctype:
        return "int"
    elif "float" in ctype or "double" in ctype:
        return "float"
    else:
        return "Any"


def map_creturn_to_pyhint(ctype: str) -> str:
    if "char*" in ctype:
        return "str | None"
    elif "int" in ctype or "long" in ctype:
        return "int"
    elif "float" in ctype or "double" in ctype:
        return "float"
    else:
        return "Any"


def download_bindings():
    req = requests.get(
        "https://github.com/GDG-on-Campus-NKNU/NKNU-Core/releases/latest/download/windows_x86_64_nknu_core.dll")
    current_path = os.path.dirname(os.path.abspath(__file__))
    core_folder = os.path.join(current_path, "nknu_core")
    dll_path = os.path.join(core_folder, "core.dll")
    with open(dll_path, "wb") as f:
        f.write(req.content)


def generate_bindings():
    req = requests.get(
        "https://github.com/GDG-on-Campus-NKNU/NKNU-Core/releases/latest/download/windows_x86_64_nknu_core.h")

    current_path = os.path.dirname(os.path.abspath(__file__))
    core_folder = os.path.join(current_path, "nknu_core")
    dll_path = os.path.join(core_folder, "core.dll")

    sigs = extract_exported_signatures(req.text)
    clean_sigs = [strip_param_names(s) for s in sigs]
    parsed = [parse_func(s) for s in clean_sigs if parse_func(s)]

    with open(os.path.join(core_folder, "bindings.py"), "w", encoding="utf-8") as f:
        f.write("from cffi import FFI\n")
        f.write("from typing import Any\n\n")
        f.write("ffi = FFI()\n")
        f.write('ffi.cdef("""\n')
        for s in clean_sigs:
            f.write(f"    {s}\n")
        f.write('""")\n\n')
        f.write(f'C = ffi.dlopen("{dll_path.replace("\\", "\\\\")}")\n\n')
        f.write("def _decode(ptr) -> str | None:\n")
        f.write("    if ptr == ffi.NULL:\n")
        f.write("        return None\n")
        f.write("    return ffi.string(ptr).decode('utf-8')\n\n")

        for ret_type, fname, args in parsed:
            py_args = [f"arg{i}" for i in range(len(args))]
            py_sig = []
            for i, a in enumerate(args):
                hint = map_ctype_to_pyhint(a)
                py_sig.append(f"{py_args[i]}: {hint}")
            sig_str = ", ".join(py_sig)
            ret_hint = map_creturn_to_pyhint(ret_type)

            f.write(f"def {fname}({sig_str}) -> {ret_hint}:\n" if sig_str else f"def {fname}() -> {ret_hint}:\n")

            call_args = []
            for i, a in enumerate(args):
                if "char*" in a:
                    call_args.append(f"{py_args[i]}.encode() if isinstance({py_args[i]}, str) else {py_args[i]}")
                else:
                    call_args.append(py_args[i])
            call_args_str = ", ".join(call_args)

            if ret_type == "char*":
                f.write(f"    return _decode(C.{fname}({call_args_str}))\n\n")
            else:
                f.write(f"    return C.{fname}({call_args_str})\n\n")

    print(f"[OK] Bindings generated")


if __name__ == "__main__":
    download_bindings()
    generate_bindings()
