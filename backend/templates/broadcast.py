"""Manim code to visualize NumPy broadcast operations."""

from typing import Optional, List
import numpy as np
from manim import *

from templates.utils import adjust_brackets


class BroadcastingAnimation(Scene):
    """A scene that visualizes broadcasting operations."""

    def __init__(self, arrays: List[np.ndarray],
                 target_shape: Optional[tuple] = None, *,
                 result: np.ndarray,
                 wait_time: float = 0.5):
        super().__init__()
        self.arrays = arrays if arrays is not None else []
        self.target_shape = target_shape
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for broadcasting operation visualization."""
        matrices = [Matrix(arr) if arr.ndim != 1 else Matrix(
            [[x] for x in arr]) for arr in self.arrays]

        for i, matrix in enumerate(matrices):
            matrix.shift(LEFT * (len(matrices) - 1) * 2 + RIGHT * i * 4)

        self.play(*[Write(matrix) for matrix in matrices])
        self.wait(self.wait_time)

        if self.target_shape:
            self.show_broadcast_to(matrices[0], self.result)
        elif len(self.arrays) > 1:
            self.show_broadcast_arrays(matrices, self.result)
        else:
            self.show_simple_broadcast(matrices[0])

    def show_broadcast_to(self, matrix: Matrix, result: np.ndarray):
        """Animate broadcasting to a target shape."""
        new_elements = [MathTex(str(value)) for value in result.flatten()]
        new_matrix = VGroup(*new_elements).arrange_in_grid(
            rows=result.shape[0], cols=result.shape[1], buff=0.6
        )

        left_bracket, right_bracket = adjust_brackets(matrix, new_matrix)

        self.play(
            *[Transform(matrix.get_entries()[i], new_elements[i])
              for i in range(len(matrix.get_entries()))],
            *[FadeIn(elem)
              for elem in new_elements[len(matrix.get_entries())::]],
            Transform(matrix.get_brackets()[0], left_bracket),
            Transform(matrix.get_brackets()[1], right_bracket)
        )

        self.wait(self.wait_time)

    def show_broadcast_arrays(self, matrices: List[Matrix], results: List[np.ndarray]):
        """Animate broadcasting between arrays."""
        # Implementation for broadcasting between arrays
        pass

    def show_simple_broadcast(self, matrix: Matrix):
        """Animate a simple broadcast operation."""
        broadcast_text = Text("broadcast").next_to(matrix, DOWN)
        self.play(Write(broadcast_text))
        self.wait(self.wait_time)

        operation_text = Text("(in operations)").next_to(broadcast_text, DOWN)
        self.play(Write(operation_text))
        self.wait(self.wait_time)
