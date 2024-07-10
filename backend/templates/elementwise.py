# pylint: disable=no-member
"""Manim code to visualize elementwise operations"""

from typing import Optional, Dict, Any
import numpy as np
from manim import *

OPS: Dict[str, Any] = {
    'add': (np.add, "+"),
    'sub': (np.subtract, "-"),
    'mul': (np.multiply, r"\times"),
    'div': (np.divide, r"\div"),
    'floor_divide': (np.floor_divide, r"\texttt{//}"),
    'mod': (np.mod, r"\%"),
    'power': (np.power, r"^"),
    'sin': (np.sin, r"\sin"),
    'cos': (np.cos, r"\cos"),
    'tan': (np.tan, r"\tan"),
    'arcsin': (np.arcsin, r"\arcsin"),
    'arccos': (np.arccos, r"\arccos"),
    'arctan': (np.arctan, r"\arctan"),
    'sinh': (np.sinh, r"\sinh"),
    'cosh': (np.cosh, r"\cosh"),
    'tanh': (np.tanh, r"\tanh"),
    'arcsinh': (np.arcsinh, r"\operatorname{arcsinh}"),
    'arccosh': (np.arccosh, r"\operatorname{arccosh}"),
    'arctanh': (np.arctanh, r"\operatorname{arctanh}"),
    'exp': (np.exp, r"\exp"),
    'expm1': (np.expm1, r"\exp(x)-1"),
    'exp2': (np.exp2, r"2^x"),
    'log': (np.log, r"\log"),
    'log10': (np.log10, r"\log_{10}"),
    'log2': (np.log2, r"\log_2"),
    'log1p': (np.log1p, r"\log(1+x)"),
    'round': (np.round, r"\operatorname{round}"),
    'floor': (np.floor, r"\lfloor x \rfloor"),
    'ceil': (np.ceil, r"\lceil x \rceil"),
    'trunc': (np.trunc, r"\operatorname{trunc}"),
    'real': (np.real, r"\operatorname{Re}"),
    'imag': (np.imag, r"\operatorname{Im}"),
    'conj': (np.conj, r"\overline{z}"),
    'abs': (np.abs, r"|x|"),
    'angle': (np.angle, r"\operatorname{arg}"),
    'logical_not': (np.logical_not, r"\neg"),
    'logical_and': (np.logical_and, r"\wedge"),
    'logical_or': (np.logical_or, r"\vee"),
    'logical_xor': (np.logical_xor, r"\oplus"),
    'equal': (np.equal, "="),
    'not_equal': (np.not_equal, r"\neq"),
    'less': (np.less, "<"),
    'less_equal': (np.less_equal, r"\leq"),
    'greater': (np.greater, ">"),
    'greater_equal': (np.greater_equal, r"\geq"),
    'sqrt': (np.sqrt, r"\sqrt"),
    'cbrt': (np.cbrt, r"\sqrt[3]"),
    'square': (np.square, "x^2"),
    'fabs': (np.fabs, r"|x|"),
    'sign': (np.sign, r"\operatorname{sign}"),
    'heaviside': (np.heaviside, r"H"),
    'maximum': (np.maximum, r"\max"),
    'minimum': (np.minimum, r"\min"),
}


class ElementWiseOperation(Scene):
    """A scene that visualizes elementwise operations with broadcasting support."""

    def __init__(self, array1: np.ndarray, array2: Optional[np.ndarray] = None,
                 operation: str = 'add', result: Optional[np.ndarray] = None,
                 wait_time: float = 0.5):
        super().__init__()
        self.array1 = array1
        self.array2 = array2
        self.operation = operation
        self.result = np.atleast_2d(
            result if result is not None else OPS[operation][0](array1, array2))
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for elementwise operation visualization with broadcasting."""
        m1 = Matrix(self.array1)
        m1.shift(LEFT * 4)

        if self.array2 is not None:
            m2 = Matrix(self.array2)
            op_symbol = MathTex(OPS[self.operation][1]).next_to(m1, RIGHT)
            m2.next_to(op_symbol, RIGHT)
            equals = MathTex("=").next_to(m2, RIGHT)
        else:
            op_symbol = MathTex(OPS[self.operation][1]).next_to(m1, RIGHT)
            equals = MathTex("=").next_to(op_symbol, RIGHT)

        m_result = Matrix(self.result)
        m_result.next_to(equals, RIGHT)

        self.play(Write(m1))
        if self.array2 is not None:
            self.play(Write(m2))
        self.play(Write(op_symbol), Write(equals), Write(m_result))
        self.wait(self.wait_time)

        rect1 = None
        rect2 = None

        for i in range(self.result.shape[0]):
            for j in range(self.result.shape[1]):
                # Handle array1
                if self.array1.shape[1] == 1:  # Column vector
                    elem1 = m1.get_entries()[i % self.array1.shape[0]]
                elif self.array1.shape[0] == 1:  # Row vector
                    elem1 = m1.get_entries()[j % self.array1.shape[1]]
                else:  # 2D array
                    elem1 = m1.get_entries()[
                        i * self.array1.shape[1] + (j % self.array1.shape[1])]
                rect1 = SurroundingRectangle(elem1)

                # Handle array2
                if self.array2 is not None:
                    if self.array2.shape[1] == 1:  # Column vector
                        elem2 = m2.get_entries()[i % self.array2.shape[0]]
                    elif self.array2.shape[0] == 1:  # Row vector
                        elem2 = m2.get_entries()[j % self.array2.shape[1]]
                    else:  # 2D array
                        elem2 = m2.get_entries()[i * self.array2.shape[1] + j]
                    rect2 = SurroundingRectangle(elem2)

                self.play(Create(rect1), Create(
                    rect2), run_time=self.wait_time)

                # Create operation text
                if self.array2 is not None:
                    operation_text = MathTex(
                        f"{self.array1[i % self.array1.shape[0], j % self.array1.shape[1]]}",
                        OPS[self.operation][1],
                        f"{self.array2[i % self.array2.shape[0], j % self.array2.shape[1]]}",
                        "=",
                        f"{self.result[i, j]}"
                    )
                else:
                    operation_text = MathTex(
                        OPS[self.operation][1],
                        f"({self.array1[i % self.array1.shape[0], j % self.array1.shape[1]]})",
                        "=",
                        f"{self.result[i, j]}"
                    )
                operation_text.next_to(m_result, DOWN)

                self.play(Write(operation_text), run_time=self.wait_time)
                self.wait(self.wait_time)

                result_elem = m_result.get_entries(
                )[i * self.result.shape[1] + j]
                self.play(ReplacementTransform(operation_text,
                          result_elem), run_time=self.wait_time)

                self.play(FadeOut(rect1), FadeOut(rect2))

        # Clean up any remaining highlights
        if rect1:
            self.play(FadeOut(rect1))
        if rect2:
            self.play(FadeOut(rect2))

        self.wait(2 * self.wait_time)
