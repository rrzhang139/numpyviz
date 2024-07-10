"""Utility functions for Manim visualizations."""

from typing import Tuple
from manim import VGroup, LEFT, RIGHT


def adjust_brackets(matrix: VGroup, new_matrix: VGroup) -> Tuple[VGroup, VGroup]:
    """
    Adjust the brackets of a matrix to fit a new matrix.

    Args:
        matrix (VGroup): The original matrix.
        new_matrix (VGroup): The new matrix to fit the brackets to.
        is_width (bool, optional): Whether to adjust width instead of height. Defaults to False.

    Returns:
        Tuple[VGroup, VGroup]: The adjusted left and right brackets.
    """
    left_bracket = matrix.get_brackets()[0].copy()
    right_bracket = matrix.get_brackets()[1].copy()
    new_height = new_matrix.get_height() + 0.5
    left_bracket.set_height(new_height)
    right_bracket.set_height(new_height)
    left_bracket.next_to(new_matrix, LEFT)
    right_bracket.next_to(new_matrix, RIGHT)
    return left_bracket, right_bracket
