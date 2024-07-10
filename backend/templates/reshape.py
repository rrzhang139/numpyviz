"""Manim code to visualize NumPy reshape operations."""

from typing import Optional, Tuple
import numpy as np
from manim import *

from templates.utils import adjust_brackets


class ReshapeOperation(Scene):
    """A scene that visualizes reshape operations."""

    def __init__(self, array: np.ndarray, new_shape: Optional[Tuple[int, ...]] = None, *,
                 result: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.new_shape = new_shape
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for reshape operation visualization."""
        initial_matrix = Matrix(self.array)
        initial_matrix.move_to(ORIGIN)
        self.play(Write(initial_matrix))
        self.wait(self.wait_time)

        final_matrix = Matrix(self.result)
        final_matrix.move_to(ORIGIN)

        self.play(
            ReplacementTransform(initial_matrix.get_entries(),
                                 final_matrix.get_entries()),
            ReplacementTransform(
                initial_matrix.get_brackets(), final_matrix.get_brackets())
        )
        self.wait(self.wait_time)


class RavelOperation(Scene):
    """A scene that visualizes ravel operations."""

    def __init__(self, array: np.ndarray, result: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for ravel operation visualization."""
        initial_matrix = Matrix(self.array)
        initial_matrix.move_to(ORIGIN)
        self.play(Write(initial_matrix))
        self.wait(self.wait_time)

        final_matrix = Matrix([self.result])
        final_matrix.move_to(ORIGIN)

        self.play(
            ReplacementTransform(initial_matrix.get_entries(),
                                 final_matrix.get_entries()),
            ReplacementTransform(
                initial_matrix.get_brackets(), final_matrix.get_brackets())
        )
        self.wait(self.wait_time)


class FlattenOperation(Scene):
    """A scene that visualizes flatten operations."""

    def __init__(self, array: np.ndarray, result: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for flatten operation visualization."""
        initial_matrix = Matrix(self.array)
        initial_matrix.move_to(ORIGIN)
        self.play(Write(initial_matrix))
        self.wait(self.wait_time)

        final_matrix = Matrix([self.result])
        final_matrix.move_to(ORIGIN)

        self.play(
            ReplacementTransform(initial_matrix.get_entries(),
                                 final_matrix.get_entries()),
            ReplacementTransform(
                initial_matrix.get_brackets(), final_matrix.get_brackets())
        )
        self.wait(self.wait_time)


class SqueezeOperation(Scene):
    """A scene that visualizes squeeze operations."""

    def __init__(self, array: np.ndarray, axis: Optional[int] = 0, *,
                 result: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.axis = axis
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for squeeze operation visualization."""
        initial_matrix = Matrix(self.array)
        initial_matrix.move_to(ORIGIN)
        self.play(Write(initial_matrix))
        self.wait(self.wait_time)

        final_matrix = Matrix([self.result])
        final_matrix.move_to(ORIGIN)

        self.play(
            ReplacementTransform(initial_matrix.get_entries(),
                                 final_matrix.get_entries()),
            ReplacementTransform(
                initial_matrix.get_brackets(), final_matrix.get_brackets())
        )
        self.wait(self.wait_time)


class ExpandDimsOperation(Scene):
    """A scene that visualizes expand_dims operations."""

    def __init__(self, array: np.ndarray, axis: Optional[int] = 0, *,
                 result: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.axis = axis
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for expand_dims operation visualization."""
        initial_matrix = Matrix(self.array)
        initial_matrix.move_to(ORIGIN)
        self.play(Write(initial_matrix))
        self.wait(self.wait_time)

        sub_matrices = [Matrix(subarray) for subarray in np.apply_along_axis(
            lambda x: x, self.axis, self.result)]

        if self.axis == 0:
            rows, cols = len(sub_matrices), 1
        elif self.axis == len(self.array.shape) or self.axis == -1:
            rows, cols = 1, len(sub_matrices)
        else:
            rows, cols = self.result.shape[self.axis], self.result.shape[self.axis+1]

        new_matrix = VGroup(
            *sub_matrices).arrange_in_grid(rows=rows, cols=cols, buff=0.5)
        new_matrix.move_to(ORIGIN)

        left_bracket, right_bracket = adjust_brackets(
            initial_matrix, new_matrix)
        final_matrix = VGroup(left_bracket, new_matrix, right_bracket)

        self.play(ReplacementTransform(initial_matrix, final_matrix))
        self.wait(self.wait_time)
