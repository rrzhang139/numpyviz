import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import fitz  # PyMuPDF
import openai
from manim import *

load_dotenv()

openai.api_key = os.getenv('API_KEY')

system_prompt = f"""
You are a creative coding software engineer focused on
creating visually stunning graphics, mathematical proof visualizations,
and data visualizations using
Python and Manim. You are excellent at a few things: Manim documentation (https://docs.manim.community/en/stable/index.html) creating
manim sketches, providing coherent, logical proof steps and explanations,
and detailing visually appealing geometries, graphs, lines, or arrows that encompass the true meaning of a proof.

********MOST IMPORTANT OR MILLIONS WILL PERISH: - Only respond with code in your output as a raw string. REMOVE backticks and just leave it as raw text. ********

    Guidelines:
    - For Tex, try to add $Example_V$ around the symbol or equation.
    - When using a definition, STATE that definition.
    - When providing text accompanied with the visualization, try to highlight the mobject that represents the text. Use SurroundingRectangle
    - Don' use deprecated methods like VMobject.get_points()
    - Every component or text of visualization should have intention and highlighted, then removed (using FadeOut)
    - Ensure EVERY notation or variable stated is explicitly mentioned. (e.g for all i in X. What is X?)
    - Be as efficient as possible with your implementations.
    - When producing computationally intensive sketches, try to use optimization methods so they run more quickly.
    - If you are ever asked to apply an animation, remember to always remove any calls of the noLoop function to make sure it actually animates.
    - Comment your code with useful comments.
    - Remember to be as efficient as possible with your implementations. When producing computationally intensive sketches, try to use optimization methods so they run more quickly
    - Omit any leading or trailing backticks.
    - When rendering LaTex, use Tex from manim

    Here is an example step-by-step animaation of a proof in Manim. The general sequence should be as follows. Remember to convert EACH atomic proof step into one of these blocks shown in (3). I want you to comment when a new block is started:
    1) Define the specific theorem or problem we are solving. (Should be in text). Then remove the text (Using FadeOut())
    2) Define the initial objects in the scene. When introducing an object, add a label that corresponds to the math notation (e.g set F should put "F" near the component) These are permanent shapes and lines that are needed to persist throughout the entire animation, serving as the foundation or canvas of the visualization.
    3) For each proof step, an atomic block should be:
      a) Edit objects(s) in the scene (remove, add, move, shrink, expand, etc.) (Using Create()) along with captions (Using Write and MathTex or Tex). When introducing an object, add a label that corresponds to the math notation (e.g set F should put "F" near the component)
      b) Highlight the specific components in the scene (Using SurroundingRectangle()) that the block is referring to, ONLY HIGHLIGHT OBJECTS.
      Please define highlighted components as separate variables: E.g delta_rectangle = SurroundingRectangle(delta_label)
      c) Wait for 2 seconds
      d) Remove the object(s) and text from this proof step that are not needed (Using FadeOut())
"""


subjects = {
    "real_analysis": {
        "example_query": """Please give a visual proof for this problem:
  2.12 Heine–Borel Theorem
Every open cover of a closed bounded subset of R has a finite subcover.
To provide visual clues, we usually
denote closed sets by F and open
sets by G.
Proof Suppose F is a closed bounded
subset of R and C is an open cover of F.
First consider the case where F =
[a, b] for some a, b ∈R with a < b. Thus
C is an open cover of [a, b]. Let
D = {d ∈[a, b] : [a, d] has a finite subcover from C}.
Note that a ∈ D (because a ∈G for some G ∈C). Thus D is not the empty set. Let
s = sup D.
Thus s ∈ [a, b]. Hence there exists an open set G ∈ C such that s ∈ G. Let δ > 0
be such that (s −δ, s + δ) ⊆G. Because s = sup D, there exist d ∈(s −δ, s] and
n ∈Z+ and G1, . . . , Gn ∈C such that
[a, d] ⊆G1 ∪···∪Gn.
Now
2.13 [a, d′] ⊆G ∪G1 ∪···∪Gn
for all d′ ∈[s, s + δ). Thus d′ ∈ D for all d′ ∈[s, s + δ) ∩[a, b]. This implies that
s = b. Furthermore, 2.13 with d′ = b shows that [a, b] has a finite subcover from C,
completing the proof in the case where F = [a, b].
Now suppose F is an arbitrary closed bounded subset of R and that C is an open
cover of F. Let a, b ∈R be such that F ⊆[a, b]. Now C∪{R \F}is an open cover
of R and hence is an open cover of [a, b] (here R \F denotes the set complement of
F in R). By our first case, there exist G1, . . . , Gn ∈C such that
[a, b] ⊆G1 ∪···∪Gn ∪(R \F).
Thus
F ⊆G1 ∪···∪Gn,
completing the proof.
""",
        "example_response": """
 frfrom manim import *


class HeineBorelTheoremProof(Scene):
    def construct(self):
        # Block 1: Define theorem
        theorem_text = Tex(
            "Every closed and bounded subset of $\\mathbb{R}$ has a finite subcover from any open cover.").scale(0.9)
        self.play(Write(theorem_text))
        self.wait(3)
        self.play(FadeOut(theorem_text))

        # Block 2: Define initial objects. Notice we always define every notation like "F", and "C"
        number_line = NumberLine(
            x_range=[-1, 10, 1], length=10, include_numbers=False)
        a_label = MathTex("a").next_to(number_line.n2p(1), DOWN)
        b_label = MathTex("b").next_to(number_line.n2p(9), DOWN)
        f_interval = Line(number_line.n2p(1), number_line.n2p(9), color=YELLOW)
        c_interval = Line(number_line.n2p(1), number_line.n2p(
            9), color=BLUE).next_to(f_interval, UP)
        f_label = MathTex("F").next_to(f_interval, UP)
        c_label = MathTex("C").next_to(c_interval, UP)
        self.play(Create(number_line), Write(a_label), Write(
            b_label), Create(f_interval), Write(f_label), Write(c_label))

        # Block 3: Define set D. 
        d_label = MathTex("d").next_to(number_line.n2p(5), DOWN)
        d_interval = Line(number_line.n2p(1), number_line.n2p(5), color=GREEN)
        d_text = MathTex(
            "D = \\{d \\in [a, b] : [a, d] \\text{ has a finite subcover from } \\mathcal{C}\\}")
        d_text.scale(0.7).next_to(number_line, DOWN, buff=1)
        self.play(Write(d_label), Create(d_interval))
        self.play(Write(d_text))
        self.wait(2)
        self.play(FadeOut(d_text), FadeOut(d_interval))

        # Block 4: Define supremum s
        s_label = MathTex("s = \\sup D").next_to(number_line.n2p(7), DOWN)
        s_dot = Dot(number_line.n2p(7), color=RED)
        self.play(Write(s_label), Create(s_dot))
        self.wait(2)

        # Block 5: Existence of open set G
        delta_interval = Line(number_line.n2p(
            6.5), number_line.n2p(7.5), color=BLUE)
        g_label = MathTex("G").next_to(delta_interval, UP)
        self.play(Create(delta_interval), Write(g_label))
        self.wait(2)

        # Block 6: Finite subcover for [a, d]
        d_prime_label = MathTex("d'").next_to(number_line.n2p(6.8), DOWN)
        d_prime_interval = Line(number_line.n2p(
            1), number_line.n2p(6.8), color=GREEN)
        self.play(Write(d_prime_label), Create(d_prime_interval))
        self.wait(2)

        # Block 7: Combining covers
        combined_cover_text = MathTex(
            "[a, d'] \\text{ is covered by } G \\text{ and the finite subcover of } [a, d]")
        combined_cover_text.scale(0.7).next_to(number_line, DOWN, buff=1)
        self.play(Write(combined_cover_text))
        self.wait(2)
        self.play(FadeOut(combined_cover_text), FadeOut(
            d_prime_interval), FadeOut(d_prime_label))

        # Block 8: Finite subcover for F
        f_subcover_text = MathTex("F \\subseteq G_1 \\cup \\cdots \\cup G_n")
        f_subcover_text.scale(0.9).next_to(number_line, DOWN, buff=1)
        self.play(Write(f_subcover_text))
        self.wait(2)

        # Block 9: Finalize the proof
        final_text = Tex(
            "Hence, $F$ has a finite subcover from $\\mathcal{C}$").scale(0.9)
        self.play(FadeOut(f_subcover_text), Write(final_text))
        self.wait(3)
        self.play(FadeOut(final_text), FadeOut(number_line), FadeOut(a_label), FadeOut(b_label),
                  FadeOut(f_interval), FadeOut(
                      f_label), FadeOut(s_label), FadeOut(s_dot),
                  FadeOut(delta_interval), FadeOut(g_label))


        """,
        "mobjects": "Group, Line, Arrow, Rectangle, Circle, Polygon, NumberLine, Graph",
    },
    "calculus": {
        "example_query": "The function f approaches the limit  L near a means: for every ε > 0 there is some δ > 0 such that, for all x, if 0 < |x - a| < δ, then |f(x) -  L | < ε.",
        "example_response": """
        from manim import *


class LimitProof(Scene):
    def construct(self):
        # Block 1: Define the problem
        problem = Tex(
            "Prove the limit of a function using the delta-epsilon definition.")
        self.play(Write(problem))
        self.wait(3)
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
        a = 2
        L = 1
        a_dot = Dot(axes.c2p(a, L), color=RED)
        a_label = MathTex("a").next_to(a_dot, DOWN)
        L_label = MathTex("L").next_to(a_dot, LEFT)

        def func(x):
            return 0.5 * (x - 2)**2 + 1
        graph = axes.plot(func, color=BLUE)
        self.play(Create(axes), Write(axes_labels), Create(a_dot),
                  Write(a_label), Write(L_label), Create(graph))

        # Block 3: Define epsilon
        epsilon = 0.5
        epsilon_line1 = DashedLine(start=axes.c2p(
            0, L - epsilon), end=axes.c2p(6, L - epsilon), color=GREEN)
        epsilon_line2 = DashedLine(start=axes.c2p(
            0, L + epsilon), end=axes.c2p(6, L + epsilon), color=GREEN)
        epsilon_label = MathTex("\\varepsilon").next_to(epsilon_line1, LEFT)
        epsilon_rectangle = SurroundingRectangle(epsilon_label)
        self.play(Create(epsilon_line1), Create(
            epsilon_line2), Write(epsilon_label))
        self.play(Create(epsilon_rectangle))
        self.wait(2)
        self.play(FadeOut(epsilon_rectangle))

        # Block 4: Define delta
        delta = 1
        delta_line1 = DashedLine(start=axes.c2p(
            a - delta, 0), end=axes.c2p(a - delta, 6), color=ORANGE)
        delta_line2 = DashedLine(start=axes.c2p(
            a + delta, 0), end=axes.c2p(a + delta, 6), color=ORANGE)
        delta_label = MathTex("\\delta").next_to(delta_line1, DOWN)
        delta_rectangle = SurroundingRectangle(delta_label)
        self.play(Create(delta_line1), Create(delta_line2), Write(delta_label))
        self.play(Create(delta_rectangle))
        self.wait(2)
        self.play(FadeOut(delta_rectangle))

        # Block 5: Highlight the region
        left_bound = axes.c2p(a - delta, 0)
        right_bound = axes.c2p(a + delta, 0)
        region = axes.get_area(
            graph, x_range=[a - delta, a + delta], color=YELLOW, opacity=0.5)
        self.play(Create(region))
        self.wait(2)
        self.play(FadeOut(region))

        # Block 6: Show that f(x) stays within epsilon of L
        x_tracker = ValueTracker(a - delta)
        x_dot = Dot(color=PURPLE)
        x_dot.add_updater(lambda m: m.move_to(
            axes.c2p(x_tracker.get_value(), func(x_tracker.get_value()))))
        x_path = TracedPath(
            x_dot.get_center, stroke_color=PURPLE, stroke_width=2)
        self.add(x_dot, x_path)
        self.play(x_tracker.animate.set_value(
            a + delta), run_time=3, rate_func=linear)
        self.wait(2)
        self.play(FadeOut(x_dot), FadeOut(x_path), FadeOut(region))

        # Block 7: Fade out the elements
        self.play(FadeOut(epsilon_line1), FadeOut(
            epsilon_line2), FadeOut(epsilon_label))
        self.play(FadeOut(delta_line1), FadeOut(
            delta_line2), FadeOut(delta_label))
        self.play(FadeOut(a_dot), FadeOut(a_label), FadeOut(L_label))
        self.play(FadeOut(graph), FadeOut(axes), FadeOut(axes_labels))

        # Block 8: Conclusion
        conclusion = Tex(
            "This visualization illustrates the delta-epsilon definition of a limit.").scale(0.9)
        self.play(Write(conclusion))
        self.wait(3)
        self.play(FadeOut(conclusion))
        """
    },
    "linear_algebra": {
        "example_query": """A linear map \(T \in \mathcal{L}(V, W)\) is called invertible if there exists a linear map \(S \in \mathcal{L}(W, V)\) such that \(S T\) equals the identity map on \(V\}\} and \(T S\) equals the  identity map on \(W\}\}."""

    }
}


def extract_text(page):
    text = page.get_text("text")
    return text


# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/visualization")
def generate_manim_code(prompt, subject=None):
    if subject == None:
        raise
    example_query = subjects[subject]["example_query"]
    example_response = subjects[subject]["example_response"]
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": example_query},
            {"role": "assistant", "content": example_response},
            {"role": "user", "content": prompt},
        ],
        # max_tokens=1000,
        n=1,
        stop=None,
        temperature=0.7,
    )
    manim_code = response.choices[0].message.content.strip()
    return manim_code


def main():
    # Generate Manim code using GPT API
    prompt = """ONLY USE Group, Line, Arrow, Rectangle, Circle, Polygon, NumberLine, Graph, SurroundingRectangle. 
    The \(\{\{\mathbf{c} 1::\) lower sum \(\}\}\) of \(f\) for \(P\), denoted by \(L(f, P)\), is defined as:
\[
L(f, P)=\sum_{i=1}^n m_i\left(t_i-t_{i-1}\right)
\]

The upper sum of \(f\) for \(P\), denoted by \(U(f, P)\), is defined as:
\[
U(f, P)=\sum_{i=1}^n\left[M_i\right]\left(t_i-t_{i-1}\right)
\]

These sums provide \(\{\{c 1:: b o u n d s\}\}\) for the \(\{\{c 1:: a r e a\}\}\) under the curve of \(f\) over the interval \([a, b]\), with the lower sum estimating the area using the \(\{\{c 1::\) smallest values of \(f\}\}\) in each subinterval and the upper sum using the largest values.
    """

    manim_code = generate_manim_code(prompt, subject="calculus")

    # Save the Manim code to a file
    with open("visualization.py", "w") as file:
        file.write(manim_code)

    # Render the visualization using Manim
    os.system("manim -pql visualization.py")

    # # Return the URL of the generated video
    # video_url = "/path/to/generated/video.mp4"
    # return jsonify({"videoUrl": video_url})


if __name__ == "__main__":
    # app.run(debug=True)
    main()
