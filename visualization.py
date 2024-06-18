import numpy as np
from manim import *


class PyTorchOperation(Scene):
    def construct(self):
        # Define matrix for demonstration
        matrix = np.array([[1, 2], [3, 4]])

        # Create Matrix Mobject from numpy array
        m = Matrix(matrix).scale(0.7)

        # Position matrix on the scene
        m.to_edge(LEFT)
        self.add(m)

        # Label matrix
        label = Text("Input Tensor", color=BLUE).next_to(m, UP)
        self.add(label)

        # Demonstrate unsqueeze operation
        unsqueeze_label = Text("torch.unsqueeze(0)",
                               color=RED).next_to(m, DOWN)
        self.play(Write(unsqueeze_label))
        self.wait(1)

        # Show result of unsqueeze operation
        result_matrix = np.array([[[1, 2], [3, 4]]])
        result_mobject = Matrix(result_matrix).scale(
            0.7).next_to(unsqueeze_label, DOWN)
        result_label = Text("Output Tensor", color=GREEN).next_to(
            result_mobject, UP)

        self.play(Transform(m.copy(), result_mobject))
        self.add(result_mobject, result_label)
        self.wait(2)

        # Cleanup for end scene
        self.play(FadeOut(m), FadeOut(result_mobject),
                  FadeOut(label), FadeOut(result_label), FadeOut(unsqueeze_label))
        self.wait(1)
