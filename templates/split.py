"""Manim code to visualize NumPy split operations."""

from typing import Optional, Union, List
import numpy as np
from manim import *


class SplitOperation(Scene):
    """A scene that visualizes split operations."""

    def __init__(self, array: np.ndarray, indices_or_sections=None,
                 axis: Optional[int] = 0, *,
                 result: List[np.ndarray], wait_time: float = 0.5):
        super().__init__()
        self.array = array
        self.axis = axis
        self.indices_or_sections = indices_or_sections
        self.result = result
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for split operation visualization."""
        original_matrix = Matrix(self.array)
        original_matrix.to_edge(ORIGIN)
        self.play(Write(original_matrix))
        self.wait(self.wait_time)

        split_matrices = [Matrix(arr) for arr in self.result]
        split_group = VGroup(*split_matrices).arrange(RIGHT, buff=1)

        if isinstance(self.indices_or_sections, int):
            split_size = self.array.shape[self.axis] // self.indices_or_sections
            split_indices = [split_size *
                             i for i in range(1, self.indices_or_sections)]
        else:
            split_indices = self.indices_or_sections

        highlights = self.create_highlights(original_matrix, split_indices)

        if highlights:
            self.play(*[FadeIn(h) for h in highlights])
            self.wait(self.wait_time)

        animations = self.create_split_animations(
            original_matrix, split_group, split_indices)

        self.play(
            *[FadeOut(h) for h in highlights],
            *animations,
            *[FadeIn(m.get_brackets()) for m in split_matrices],
            FadeOut(original_matrix),
            run_time=1.5
        )

        self.wait(self.wait_time)

        shape_text = Text(
            f"Shapes: {[arr.shape for arr in self.result]}", font_size=24).to_edge(DOWN)
        self.play(Write(shape_text))
        self.wait(self.wait_time)

    def create_highlights(self, matrix: Matrix, split_indices: List[int]) -> List[Line]:
        """Create highlight lines for split locations."""
        highlights = []
        for idx in split_indices:
            if self.axis == 1:  # Highlighting between columns
                if idx < len(matrix.get_columns()):
                    left_col = matrix.get_columns()[idx - 1].get_right()
                    right_col = matrix.get_columns()[idx].get_left()
                    mid_point = (left_col + right_col) / 2
                    highlight = Line(
                        start=mid_point + matrix.get_top() - matrix.get_center(),
                        end=mid_point + matrix.get_bottom() - matrix.get_center(),
                        color=YELLOW
                    )
                    highlights.append(highlight)
            else:  # Highlighting between rows
                if idx < len(matrix.get_rows()):
                    top_row = matrix.get_rows()[idx - 1].get_bottom()
                    bottom_row = matrix.get_rows()[idx].get_top()
                    mid_point = (top_row + bottom_row) / 2
                    highlight = Line(
                        start=mid_point + matrix.get_left() - matrix.get_center(),
                        end=mid_point + matrix.get_right() - matrix.get_center(),
                        color=YELLOW
                    )
                    highlights.append(highlight)
        return highlights

    def create_split_animations(self, original_matrix: Matrix, split_group: VGroup,
                                split_indices: List[int]) -> List[Transform]:
        """Create animations for the split operation."""
        animations = []
        for i, split_matrix in enumerate(split_group):
            start = split_indices[i-1] if i > 0 else 0
            end = split_indices[i] if i < len(
                split_indices) else self.array.shape[self.axis]

            if self.axis == 0:
                source_entries = original_matrix.get_entries(
                )[start*self.array.shape[1]:end*self.array.shape[1]]
            else:
                source_entries = [row[start:end]
                                  for row in original_matrix.get_rows()]
                source_entries = [
                    item for sublist in source_entries for item in sublist]  # Flatten

            for source, target in zip(source_entries, split_matrix.get_entries()):
                animations.append(Transform(source.copy(), target))

        return animations
