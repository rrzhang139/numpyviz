"""Manim code to visualize NumPy concatenation operations."""

from typing import List, Optional
import numpy as np
from manim import *


class ConcatenationOperation(Scene):
    """A scene that visualizes concatenation operations."""

    def __init__(self, array: np.ndarray, axis: Optional[int] = 0, *,
                 result: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.axis = axis
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for concatenation operation visualization."""
        # Show original arrays
        matrices = [Matrix(arr) for arr in self.array]
        group = VGroup(*matrices).arrange(RIGHT, buff=1)
        self.play(Write(group))
        self.wait(self.wait_time)

        # Create new matrix
        new_matrix = Matrix(self.result)
        new_matrix.move_to(group.get_center())

        # Prepare animations for all elements
        element_animations = []
        total_entries = 0

        for idx, matrix in enumerate(matrices):
            entries = matrix.get_entries()
            if self.axis == 0:  # Concatenating along rows
                for i, elem in enumerate(entries):
                    target_index = total_entries + i
                    if target_index < len(new_matrix.get_entries()):
                        target_entry = new_matrix.get_entries()[target_index]
                        element_animations.append(
                            Transform(elem.copy(), target_entry))
                total_entries += len(entries)
            else:  # Concatenating along columns (axis == 1)
                for i, row in enumerate(matrix.get_rows()):
                    start_col = sum(len(m.get_columns())
                                    for m in matrices[:idx])
                    for j, elem in enumerate(row):
                        target_row = new_matrix.get_rows()[i]
                        if start_col + j < len(target_row):
                            target_entry = target_row[start_col + j]
                            element_animations.append(
                                Transform(elem.copy(), target_entry))

            # Fade out all original matrices' brackets
            element_animations.append(FadeOut(matrix))

        # Add animation for new matrix brackets
        element_animations.extend([FadeIn(bracket)
                                  for bracket in new_matrix.get_brackets()])

        # Play all animations simultaneously
        self.play(
            *element_animations,
            run_time=1.5
        )

        self.wait(self.wait_time)

        # Show final shape
        shape_text = Text(
            f"Final Shape: {self.result.shape}", font_size=24).to_edge(DOWN)
        self.play(Write(shape_text))
        self.wait(self.wait_time)
