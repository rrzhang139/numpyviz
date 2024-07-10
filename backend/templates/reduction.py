"""Manim code to visualize NumPy reduction operations."""

from typing import Optional
import numpy as np
from manim import *

from templates.utils import adjust_brackets


class ReductionOperation(Scene):
    """A scene that visualizes reduction operations."""

    def __init__(self, array: np.ndarray, axis: Optional[int] = None,
                 weights: Optional[np.ndarray] = None, *,
                 result: np.ndarray, operation: str = 'sum',
                 wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.operation = operation
        self.axis = axis
        self.weights = weights
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for reduction operation visualization."""
        m = Matrix(self.array)
        m.shift(ORIGIN)

        # Add matrix and operation label to the scene
        self.play(Write(m), run_time=self.wait_time)
        self.wait(self.wait_time)

        if self.axis is None:
            rect = SurroundingRectangle(m)
            self.play(Create(rect), run_time=self.wait_time)

            result_text = MathTex(str(self.result))
            result_text.move_to(m)

            self.play(
                *[ReplacementTransform(entry, result_text)
                  for entry in m.get_entries()],
                FadeOut(m.get_brackets()),
                FadeOut(rect),
                run_time=self.wait_time*2
            )
        elif self.axis == 0:
            self.column_reduction(m, self.result, self.wait_time)
        else:
            self.row_reduction(m, self.result, self.wait_time)

        self.wait(self.wait_time * 2)

    def row_reduction(self, matrix: Matrix, result: np.ndarray, wait_time: float):
        """Animate row-wise reduction."""
        rows = matrix.get_rows()
        rects = VGroup(*[SurroundingRectangle(row) for row in rows])
        self.play(Create(rects), run_time=wait_time)

        result_texts = VGroup(
            *[MathTex(str(val)).move_to(row[0]) for val, row in zip(result, rows)])

        left_bracket, right_bracket = adjust_brackets(
            matrix, result_texts)

        self.play(
            *[ReplacementTransform(row, text)
              for row, text in zip(rows, result_texts)],
            Transform(matrix.get_brackets()[0], left_bracket),
            Transform(matrix.get_brackets()[1], right_bracket),
            FadeOut(rects),
            run_time=wait_time*2
        )

    def column_reduction(self, matrix: Matrix, result: np.ndarray, wait_time: float):
        """Animate column-wise reduction."""
        columns = matrix.get_columns()
        rects = VGroup(*[SurroundingRectangle(column) for column in columns])
        self.play(Create(rects), run_time=wait_time)

        result_texts = VGroup(
            *[MathTex(str(val)).move_to(column[0]) for val, column in zip(result, columns)])

        left_bracket, right_bracket = adjust_brackets(
            matrix, result_texts)

        self.play(
            *[ReplacementTransform(column, text)
              for column, text in zip(columns, result_texts)],
            Transform(matrix.get_brackets()[0], left_bracket),
            Transform(matrix.get_brackets()[1], right_bracket),
            FadeOut(rects),
            run_time=wait_time*2
        )
