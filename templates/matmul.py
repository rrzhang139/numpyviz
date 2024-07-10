"""Manim code to visualize matrix multiplication."""

from manim import *


class MatrixMultiplication(Scene):
    """A scene that visualizes matrix multiplication."""

    def __init__(self, matrix1: np.ndarray,
                 matrix2: np.ndarray, wait_time: float = 0.5):
        super().__init__()
        self.array1 = matrix1
        self.array2 = matrix2
        self.wait_time = wait_time

    def construct(self):
        """Construct the scene for matrix multiplication visualization."""
        # Ensure matrices can be multiplied
        assert len(self.array1[0]) == len(
            self.array2), "Matrices cannot be multiplied. Inner dimensions must match."

        # Create matrix mobjects
        m1 = Matrix(self.array1)
        m2 = Matrix(self.array2)
        result = Matrix([[0 for _ in range(len(self.array2[0]))]
                        for _ in range(len(self.array1))])

        # Position matrices and operation symbols
        m1.shift(LEFT * 4)
        times = Tex("×").next_to(m1, RIGHT)
        m2.next_to(times, RIGHT)
        equals = Tex("=").next_to(m2, RIGHT)
        result.next_to(equals, RIGHT)

        # Add everything to the scene
        self.play(
            Write(m1),
            Write(m2),
            Write(times),
            Write(equals),
            Write(result),
            run_time=self.wait_time
        )
        self.wait(self.wait_time)

        # Animate the multiplication process
        for i in range(len(self.array1)):
            for j in range(len(self.array2[0])):
                # Highlight row and column
                row_rect = SurroundingRectangle(m1.get_rows()[i])
                col_rect = SurroundingRectangle(m2.get_columns()[j])
                self.play(Create(row_rect), Create(
                    col_rect), run_time=self.wait_time)

                # Calculate the result
                value = sum(self.array1[i][k] * self.array2[k][j]
                            for k in range(len(self.array2)))
                value = round(value, 2)

                # Create a temporary element to show the calculation
                temp_element = MathTex(str(value)).next_to(result, DOWN)
                self.play(Write(temp_element), run_time=self.wait_time)

                # Move the temporary element to its position in the result matrix
                target_position = result.get_entries(
                )[i*len(self.array2[0]) + j].get_center()
                self.play(temp_element.animate.move_to(
                    target_position), run_time=self.wait_time)

                # Update the result matrix
                result.get_entries()[i*len(self.array2[0]) +
                                     j].become(temp_element)

                self.wait(self.wait_time)
                self.play(FadeOut(row_rect), FadeOut(
                    col_rect), run_time=self.wait_time)
