#!/usr/bin/env python
# -*- coding: utf-8 -*-

import ast
from typing import Generator, Optional

from .interfaces import INTERFACES, CInterface, CMethod


def get_thunk_error_handler(return_type: str) -> ast.AST:
    """
    Get the AST subtree for a method thunk's error handler.
    """
    return_value: Optional[ast.AST]
    if return_type == "void":
        return_value = None
    elif return_type == "HRESULT":
        return_value = ast.Attribute(
            value=ast.Name(id="HRESULT", ctx=ast.Load()),
            attr="E_UNEXPECTED",
            ctx=ast.Load(),
        )
    elif return_type == "uint32_t":
        return_value = ast.Constant(value=0)
    else:
        raise NotImplementedError()

    return ast.ExceptHandler(
        type=ast.Name(id="Exception", ctx=ast.Load()),
        body=[
            ast.Expr(
                value=ast.Call(
                    func=ast.Attribute(
                        value=ast.Name(id="log", ctx=ast.Load()),
                        attr="exception",
                        ctx=ast.Load(),
                    ),
                    args=[
                        ast.Constant(value="Unhandled exception in callback thunk."),
                    ],
                    keywords=[],
                )
            ),
            ast.Return(value=return_value),
        ],
    )


def build_thunk_function(interface: CInterface, method: CMethod) -> ast.AST:
    """
    Build the AST subtree for a method thunk.
    """
    return ast.FunctionDef(
        name=f"FFI7Z_Py_{interface.name}_{method.name}",
        args=ast.arguments(
            posonlyargs=[],
            args=[ast.Name(id=arg_name) for _, arg_name in ((None, "this"), *method.arguments)],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        ),
        body=[
            ast.Expr(
                value=ast.Constant(
                    value=f"Thunk for {interface.name}.{method.name}",
                )
            ),
            ast.Try(
                body=[
                    ast.Assign(
                        targets=[ast.Name(id="self", ctx=ast.Store())],
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="ffi", ctx=ast.Load()),
                                attr="from_handle",
                                ctx=ast.Load(),
                            ),
                            args=[
                                ast.Attribute(
                                    value=ast.Subscript(
                                        value=ast.Call(
                                            func=ast.Attribute(
                                                value=ast.Name(id="ffi", ctx=ast.Load()),
                                                attr="cast",
                                                ctx=ast.Load(),
                                            ),
                                            args=[
                                                ast.Constant(value=f"FFI7Z_Py{interface.name} *"),
                                                ast.Name(id="this", ctx=ast.Load()),
                                            ],
                                            keywords=[],
                                        ),
                                        slice=ast.Constant(value=0),
                                        ctx=ast.Load(),
                                    ),
                                    attr="self_handle",
                                    ctx=ast.Load(),
                                )
                            ],
                            keywords=[],
                        ),
                    ),
                    ast.Return(
                        value=ast.Call(
                            func=ast.Attribute(
                                value=ast.Name(id="self", ctx=ast.Load()),
                                attr=method.name,
                                ctx=ast.Load(),
                            ),
                            args=[ast.Name(id=arg_name) for _, arg_name in method.arguments],
                            keywords=[],
                        ),
                    ),
                ],
                handlers=[get_thunk_error_handler(method.return_type)],
                orelse=[],
                finalbody=[],
            ),
        ],
        decorator_list=[
            ast.Call(
                func=ast.Attribute(
                    value=ast.Name(id="ffi", ctx=ast.Load()),
                    attr="def_extern",
                    ctx=ast.Load(),
                ),
                args=[],
                keywords=[],
            )
        ],
    )


def build_thunk_functions() -> Generator[ast.AST, None, None]:
    """
    Build the AST subtrees for each method thunk.
    """
    for interface in INTERFACES:
        for method in interface.methods:
            yield build_thunk_function(interface, method)


def build_thunks_ast() -> ast.AST:
    """
    Build the AST for the thunks file.
    """
    return ast.Module(
        body=[
            ast.Expr(value=ast.Constant(value="Generated COM thunks for lib7zip.")),
            ast.ImportFrom(module="logging", names=[ast.alias(name="getLogger")], level=0),
            ast.ImportFrom(module="ffi7zip", names=[ast.alias(name="ffi")], level=1),
            ast.ImportFrom(module="hresult", names=[ast.alias(name="HRESULT")], level=1),
            ast.Assign(
                targets=[ast.Name(id="log", ctx=ast.Store())],
                value=[
                    ast.Call(
                        func=ast.Name(id="getLogger", ctx=ast.Load()),
                        args=[ast.Constant(value="ffi7zip")],
                        keywords=[],
                    ),
                ],
            ),
            *build_thunk_functions(),
        ],
        type_ignores=[],
    )


def build_thunks_py() -> bytes:
    """
    Generate conents of thunks.py.
    """
    return (
        """#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pylint: disable=broad-exception-caught,invalid-name,no-name-in-module
# type: ignore"""
        + ast.unparse(ast.fix_missing_locations(build_thunks_ast()))
    ).encode("utf-8")


if __name__ == "__main__":
    print(str(build_thunks_py(), encoding="utf-8"))
