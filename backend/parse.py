"""Parse Numpy code into an operation tree."""
# pylint: disable=no-member

import ast
from typing import List, Dict, Any, Union
import numpy as np


class OperationNode:
    """Class representing a node in the operation tree."""

    operations: Dict[str, Any] = {
        "add": np.add,
        "matmul": np.matmul,
        "subtract": np.subtract,
        "multiply": np.multiply,
        "divide": np.divide,
        "floor_divide": np.floor_divide,
        "mod": np.mod,
        "power": np.power,
        "sin": np.sin,
        "cos": np.cos,
        "tan": np.tan,
        "arcsin": np.arcsin,
        "arccos": np.arccos,
        "arctan": np.arctan,
        "sinh": np.sinh,
        "cosh": np.cosh,
        "tanh": np.tanh,
        "arcsinh": np.arcsinh,
        "arccosh": np.arccosh,
        "arctanh": np.arctanh,
        "exp": np.exp,
        "expm1": np.expm1,
        "exp2": np.exp2,
        "log": np.log,
        "log10": np.log10,
        "log2": np.log2,
        "log1p": np.log1p,
        "round": np.round,
        "floor": np.floor,
        "ceil": np.ceil,
        "trunc": np.trunc,
        "real": np.real,
        "imag": np.imag,
        "conj": np.conj,
        "abs": np.abs,
        "angle": np.angle,
        "logical_not": np.logical_not,
        "logical_and": np.logical_and,
        "logical_or": np.logical_or,
        "logical_xor": np.logical_xor,
        "equal": np.equal,
        "not_equal": np.not_equal,
        "less": np.less,
        "less_equal": np.less_equal,
        "greater": np.greater,
        "greater_equal": np.greater_equal,
        "sqrt": np.sqrt,
        "cbrt": np.cbrt,
        "square": np.square,
        "fabs": np.fabs,
        "sign": np.sign,
        "heaviside": np.heaviside,
        "maximum": np.maximum,
        "minimum": np.minimum,
        "sum": np.sum,
        "mean": np.mean,
        "max": np.max,
        "min": np.min,
        "median": np.median,
        "std": np.std,
        "var": np.var,
        "prod": np.prod,
        "average": np.average,
        "concatenate": np.concatenate,
        "reshape": np.reshape,
        "squeeze": np.squeeze,
        "expand_dims": np.expand_dims,
        "transpose": np.transpose,
        "split": np.split,
        "broadcast_to": np.broadcast_to,
        "flatten": np.ravel,  # type: ignore
        "ravel": np.ravel,
        "dot": np.dot,
    }

    def __init__(self, operation: str, operands: List[Any], **kwargs: Any) -> None:
        """Initialize an operation node."""
        self.operation = operation
        self.operands = operands
        self.kwargs = kwargs
        self.result = None

    def compute(self) -> Any:
        """Compute the result of the operation."""
        if self.operation not in self.operations:
            raise ValueError(f"Unsupported operation: {self.operation}")

        op_func = self.operations[self.operation]

        def unwrap(arg: Any) -> Any:
            if isinstance(arg, (OperationNode, ArrayNode)):
                result = arg.result
                if isinstance(result, (list, np.ndarray)):
                    result = np.array(result)
                    # if result.ndim == 1 or (result.ndim == 2 and result.shape[0] == 1):
                    #     return result.reshape(-1, 1)
                    return np.atleast_2d(result)
                return result
            elif isinstance(arg, (list, tuple)):
                return [unwrap(item) for item in arg]
            return arg

        self.operands = [unwrap(op) for op in self.operands]
        self.kwargs = {k: unwrap(v) for k, v in self.kwargs.items()}

        print(
            f"Computing {self.operation} with args: {self.operands}, {self.kwargs}")
        raw_result = op_func(*self.operands, **self.kwargs)
        # if raw_result.ndim == 1 or (raw_result.ndim == 2 and raw_result.shape[0] == 1):
        #     return raw_result.reshape(-1, 1)
        self.result = np.around(raw_result, 2)
        print("Result: ", self.result)

        return self.result


class ArrayNode(OperationNode):
    """Class representing an array node in the operation tree."""

    def __init__(self, name: str, value: Any) -> None:
        """Initialize an array node."""
        super().__init__("array", [])
        self.name = name
        self.result = value

    def __repr__(self) -> str:
        """Return a string representation of the array node."""
        return f"ArrayNode({self.name})"


def parse_numpy_code(code: str) -> List[OperationNode]:
    """Parse a string of Numpy code into a list of operation nodes."""
    tree = ast.parse(code)
    nodes: Dict[str, Any] = {}
    operation_nodes: List[OperationNode] = []

    binary_ops: Dict[Any, str] = {
        ast.Add: "add",
        ast.Sub: "subtract",
        ast.Mult: "multiply",
        ast.Div: "divide",
        ast.FloorDiv: "floor_divide",
        ast.Mod: "mod",
        ast.Pow: "power",
        ast.MatMult: "matmul"
    }
    unary_ops: Dict[Any, str] = {ast.USub: "negative", ast.UAdd: "positive"}

    numpy_funcs = set(OperationNode.operations.keys())

    def parse_node(node: ast.AST) -> Union[OperationNode, Any]:
        """Parse an AST node into an operation node or a value."""
        if isinstance(node, ast.Name):
            return nodes.get(node.id, node.id)
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.UnaryOp):
            op = unary_ops[type(node.op)]
            operand = parse_node(node.operand)
            return -operand if op == "negative" and isinstance(operand, (int, float)) else OperationNode(op, [operand])
            # return OperationNode(op, [operand])
        elif isinstance(node, (ast.List, ast.Tuple)):
            return [parse_node(elt) for elt in node.elts]
        elif isinstance(node, ast.BinOp) and type(node.op) in binary_ops:
            op = binary_ops[type(node.op)]
            op_node = OperationNode(
                op, [parse_node(node.left), parse_node(node.right)])
            operation_nodes.append(op_node)
            return op_node
        elif isinstance(node, ast.Attribute) and node.attr == 'T':
            value = parse_node(node.value)
            op_node = OperationNode("transpose", [value])
            operation_nodes.append(op_node)
            return op_node
        elif isinstance(node, ast.Call):
            if (
                isinstance(node.func, ast.Attribute)
                and node.func.attr in numpy_funcs
            ):
                op = node.func.attr
                if node.func.value.id == "np":
                    operands = [parse_node(arg) for arg in node.args]
                elif node.func.value.id in nodes:
                    operands = [nodes[node.func.value.id]] + \
                        [parse_node(arg) for arg in node.args]
                kwargs = {kw.arg: parse_node(kw.value) for kw in node.keywords}
                op_node = OperationNode(op, operands, **kwargs)
                operation_nodes.append(op_node)
                return op_node
            elif isinstance(node.func, ast.Attribute) and node.func.attr == "array":
                return ArrayNode(f"array_{len(nodes)}", parse_node(node.args[0]))
        return node

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            target = node.targets[0].id
            nodes[target] = parse_node(node.value)
        elif isinstance(node, ast.Expr):
            parse_node(node.value)

    return operation_nodes


def parse(code: str) -> List[OperationNode]:
    """Entry point for parsing Numpy code."""
    operation_nodes = parse_numpy_code(code)

    print("\nOperation Nodes:")
    for node in operation_nodes:
        print(f"Operands: {node.operands}, Keyword Args: {node.kwargs}")

    return operation_nodes
