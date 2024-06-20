from manim import *


class RiemannSums(Scene):
    def construct(self):
        # Block 1: Define the problem
        problem = Tex(
            "Visualize the definitions of Lower and Upper Riemann sums.")
        self.play(Write(problem))
        self.wait(2)
        self.play(FadeOut(problem))

        # Block 2: Define initial objects
        axes = Axes(
            x_range=[-1, 6],
            y_range=[-1, 6],
            x_length=7,
            y_length=7,
            axis_config={"include_tip": False},
        )
        axes_labels = axes.get_axis_labels(x_label="x", y_label="f(x)")

        def func(x):
            return 0.5 * (x - 2)**2 + 1
        graph = axes.plot(func, color=BLUE)

        self.play(Create(axes), Write(axes_labels), Create(graph))

        # Block 3: Define partition P
        n = 5
        a = 0
        b = 5
        partition = [a + i * (b - a) / n for i in range(n + 1)]
        partition_dots = VGroup(*[Dot(axes.c2p(p, 0)) for p in partition])
        partition_lines = VGroup(*[axes.get_vertical_line(axes.c2p(p, 0), line_config={
                                 "dashed_ratio": 0.5, "color": GRAY}) for p in partition])
        self.play(Create(partition_dots), Create(partition_lines))

        # Block 4: Define lower sum
        lower_sum = sum(func(
            partition[i - 1]) * (partition[i] - partition[i - 1]) for i in range(1, n + 1))
        lower_sum_label = MathTex("L(f, P)=", f"{lower_sum:.2f}")
        lower_sum_label.to_corner(UP + LEFT)
        lower_sum_rects = VGroup(*[
            axes.get_riemann_rectangles(
                graph,
                x_range=[partition[i - 1], partition[i]],
                dx=(partition[i] - partition[i - 1]),
                color=YELLOW,
                fill_opacity=0.5,
                stroke_width=0.5,
                # start_color=YELLOW,
                # end_color=YELLOW,
                input_sample_type="left",
            )
            for i in range(1, n + 1)
        ])
        self.play(Write(lower_sum_label), Create(lower_sum_rects))

        # Block 5: Define upper sum
        upper_sum = sum(
            func(partition[i]) * (partition[i] - partition[i - 1]) for i in range(1, n + 1))
        upper_sum_label = MathTex("U(f, P)=", f"{upper_sum:.2f}")
        upper_sum_label.to_corner(UP + RIGHT)
        upper_sum_rects = VGroup(*[
            axes.get_riemann_rectangles(
                graph,
                x_range=[partition[i - 1], partition[i]],
                dx=(partition[i] - partition[i - 1]),
                color=RED,
                fill_opacity=0.5,
                stroke_width=0.5,
                # start_color=RED,
                # end_color=RED,
                input_sample_type="right",
            )
            for i in range(1, n + 1)
        ])
        self.play(Write(upper_sum_label), Create(upper_sum_rects))

        # Block 6: Highlight the bounds
        lower_sum_rect = SurroundingRectangle(lower_sum_label, color=YELLOW)
        upper_sum_rect = SurroundingRectangle(upper_sum_label, color=RED)
        self.play(Create(lower_sum_rect), Create(upper_sum_rect))
        self.wait(2)
        self.play(FadeOut(lower_sum_rect), FadeOut(upper_sum_rect))

        # Block 7: Fade out the elements
        self.play(
            FadeOut(partition_dots),
            FadeOut(partition_lines),
            FadeOut(lower_sum_label),
            FadeOut(upper_sum_label),
            FadeOut(lower_sum_rects),
            FadeOut(upper_sum_rects),
            FadeOut(graph),
            FadeOut(axes),
            FadeOut(axes_labels)
        )

        # Block 8: Conclusion
        conclusion = Tex(
            "This visualization illustrates the definitions of Lower and Upper Riemann sums.")
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))
