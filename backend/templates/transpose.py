"""Manim code to visualize matrix transposition."""

import numpy as np
from manim import *


class MatrixTransposition(Scene):
    """A scene that visualizes matrix transposition."""

    def __init__(self, array: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for matrix transposition visualization."""
        matrix = np.array(self.array)

        if matrix.ndim == 1 or (matrix.ndim == 2 and 1 in matrix.shape):
            self.vector_transposition(matrix)
        else:
            self.matrix_transposition(matrix)

    def vector_transposition(self, vector: np.ndarray):
        """Animate the transposition of a vector."""
        is_row = vector.ndim == 2 and vector.shape[0] == 1

        m = Matrix([vector[0]] if is_row else [[x] for x in vector])
        m.move_to(ORIGIN)

        self.play(Write(m))
        self.wait(self.wait_time)

        transposed = Matrix([[x] for x in vector[0]] if is_row else [vector])
        transposed.move_to(ORIGIN)

        self.play(
            ReplacementTransform(m.get_entries(), transposed.get_entries()),
            ReplacementTransform(m.get_brackets(), transposed.get_brackets()),
            run_time=1.5
        )

        self.wait(2 * self.wait_time)

    def matrix_transposition(self, matrix: np.ndarray):
        """Animate the transposition of a matrix."""
        m = Matrix(matrix)
        m.move_to(ORIGIN)

        self.play(Write(m))
        self.wait(self.wait_time)

        animations = []
        for i in range(matrix.shape[0]):
            for j in range(i+1, matrix.shape[1]):  # Only upper triangle
                elem1 = m.get_entries()[i*matrix.shape[1] + j]
                elem2 = m.get_entries()[j*matrix.shape[0] + i]
                animations.extend([
                    elem1.animate.move_to(elem2.get_center()),
                    elem2.animate.move_to(elem1.get_center())
                ])

        self.play(*animations, run_time=1.5)
        self.wait(2 * self.wait_time)
