import inspect
import sys
from abc import ABC
from typing import Any

from rawjs2dict.utils import LITERAL_VALUE
from rawjs2dict.utils import merge_dicts


class JSTransformer:
    @staticmethod
    def __get_transformer__(transformer_name: str) -> "type[BaseJSTransformer] | None":
        transformer = dict(inspect.getmembers(sys.modules[__name__], inspect.isclass)).get(
            f"{transformer_name}Transformer"
        )

        return transformer if transformer and issubclass(transformer, BaseJSTransformer) else None

    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        transformer = cls.__get_transformer__(ast.get("type", ""))
        return transformer.transform(ast) if transformer else {}


class BaseJSTransformer(ABC):
    fields: list[str] = []

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return ""

    @classmethod
    def __transform_single_field__(cls, ast: dict[str, Any], field: str) -> dict[str, Any]:
        output: dict[str, Any] = {}
        name = cls.__get_name__(ast)
        if field in ast:
            data = ast[field]
            if isinstance(data, list):
                for statement in data:
                    result = JSTransformer.transform(statement)
                    output = merge_dicts(output, result)
            elif isinstance(data, dict):
                output = JSTransformer.transform(data)

        return {name: output} if name else output

    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        output: dict[str, Any] = {}
        for field in cls.fields:
            output = merge_dicts(output, cls.__transform_single_field__(ast, field))

        return output


class LiteralTransformer(BaseJSTransformer):
    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        return {LITERAL_VALUE: ast["value"]}


class ArrayExpressionTransformer(BaseJSTransformer):
    fields = ["elements"]


class ObjectExpressionTransformer(BaseJSTransformer):
    fields = ["properties"]


class PropertyTransformer(BaseJSTransformer):
    fields = ["value"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        name = None
        if ast["value"]:
            if ast["key"]["type"] == "Identifier":
                name = ast["key"]["name"]
            else:
                name = "_".join([str(v) for v in JSTransformer.transform(ast["key"]).values()])

        return name or super().__get_name__(ast)


class FunctionExpressionTransformer(BaseJSTransformer):
    fields = ["body"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class ArrowFunctionExpressionTransformer(FunctionExpressionTransformer):
    fields = ["body"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class ClassExpressionTransformer(FunctionExpressionTransformer):
    fields = ["body"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class ClassBodyTransformer(BaseJSTransformer):
    fields = ["body"]


class MethodDefinitionTransformer(PropertyTransformer):
    pass


class CallExpressionTransformer(BaseJSTransformer):
    fields = ["arguments", "callee"]


class NewExpressionTransformer(BaseJSTransformer):
    fields = ["arguments", "callee"]


class SpreadElementTransformer(BaseJSTransformer):
    fields = ["argument"]


class YieldExpressionTransformer(SpreadElementTransformer):
    fields = ["argument"]


class AssignmentExpressionTransformer(BaseJSTransformer):
    fields = ["right"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        left = ast["left"]
        if "name" in left:
            name = left["name"]
        elif "name" in left["object"]:
            name = f"{left['object']['name']}_{left['property']['name']}"
        elif "object" in left["property"]:
            name = cls.__get_name__({"left": left["property"]})
        else:
            name = f"{left['property']['name']}"

        return name or super().__get_name__(ast)


class ClassDeclarationTransformer(BaseJSTransformer):
    fields = ["body"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class FunctionDeclarationTransformer(BaseJSTransformer):
    fields = ["body"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class VariableDeclaratorTransformer(BaseJSTransformer):
    fields = ["init"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return (ast.get("id", {}) or {}).get("name", "") or super().__get_name__(ast)


class VariableDeclarationTransformer(BaseJSTransformer):
    fields = ["declarations"]


class BlockStatementTransformer(BaseJSTransformer):
    fields = ["body"]


class ExpressionStatementTransformer(BaseJSTransformer):
    fields = ["expression"]


class IfStatementTransformer(BaseJSTransformer):
    fields = ["consequent", "alternate"]


class LabeledStatementTransformer(BaseJSTransformer):
    fields = ["body"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return ast.get("label", {}).get("name", "") or super().__get_name__(ast)


class SwitchStatementTransformer(BaseJSTransformer):
    fields = ["cases"]


class SwitchCaseTransformer(BaseJSTransformer):
    fields = ["consequent"]


class TryStatementTransformer(BaseJSTransformer):
    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        output = {}

        output["try"] = JSTransformer.transform(ast["block"])
        if ast["handler"]:
            output["catch"] = JSTransformer.transform(ast["handler"])
        if ast["finalizer"]:
            output["finally"] = JSTransformer.transform(ast["finalizer"])

        return output


class CatchClauseTransformer(BaseJSTransformer):
    fields = ["body"]


class WithStatementTransformer(BaseJSTransformer):
    fields = ["body"]


class ProgramTransformer(BaseJSTransformer):
    fields = ["body"]


class ReturnStatementTransformer(BaseJSTransformer):
    fields = ["argument"]

    @classmethod
    def __get_name__(cls, ast: dict[str, Any]) -> str:
        return "return"


class UnaryExpressionTransformer(BaseJSTransformer):
    @classmethod
    def transform(cls, ast: dict[str, Any]) -> dict[str, Any]:
        if ast["argument"]["type"] == "Literal" and ast["prefix"] and ast["operator"] in ["!", "~", "-", "+"]:
            value = JSTransformer.transform(ast["argument"])[LITERAL_VALUE]
            if ast["operator"] == "!" and isinstance(value, bool):
                return {LITERAL_VALUE: not value}
            if ast["operator"] == "-" and isinstance(value, (int, float)):
                return {LITERAL_VALUE: -value}
            if ast["operator"] == "+" and isinstance(value, (int, float)):
                return {LITERAL_VALUE: value}
            if ast["operator"] == "~" and isinstance(value, int):
                return {LITERAL_VALUE: ~value}

            return {LITERAL_VALUE: value}
        return super().transform(ast)
