import os
import typing as _typing

from py_mini_racer import MiniRacer

from rawjs2dict.transformers import JSTransformer as _JSTransformer
from rawjs2dict.utils import clean_dict as _clean_dict

_ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

_ctx = MiniRacer()
with open(os.path.join(_ROOT_DIR, "acorn.js"), "r") as f:
    _ctx.eval(f.read())


def transform(script: str) -> dict[str, _typing.Any]:
    ast = _ctx.call("acorn.parse", script)
    output = _JSTransformer.transform(ast)
    cleaned_output: dict[str, _typing.Any] = _clean_dict(output)

    return cleaned_output
