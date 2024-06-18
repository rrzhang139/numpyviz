import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import openai

load_dotenv()

openai.api_key = os.getenv('API_KEY')


def matrix_op(prompt): return f"""
    Generate Manim code to visualize the following machine learning code:
    ```
    {prompt}
    ```
    ==========================================
    Guidelines:
    - Generate manim code for any type of pytorch operation. Make sure it looks clean.
    - don't provide text
    - Omit any leading or trailing backticks.
    - USE EXACTLY THE template under "Template: " for the code generation
    - Create Matrix mobjects to enhance matrix operations. (Parameters: matrix (Iterable) A numpy 2d array or list of lists.)
    - Before performing a calculation of some rows or columns, highlight the specified row or column (e.g m0.add(SurroundingRectangle(m0.get_columns()[1])))
    - JUST PRINT THE CODE, NOTHING ELSE.
    - USE THE EXACT TEMPLATE SHOWN BELOW UNDER MANIM CODE.
    - Use the template above, **INSERT** are places where context needs to be inserted based on user's request.
    - Use the play method to animate the shapes and visualization mobjects sequentially. (You CANNOT play objects directly: self.play(SurroundingRectangle(m2.get_columns()[1], color=RED)))
    - Add wait methods between animations to provide enough time for the viewer to read and understand the content.
    - Ensure the code is complete, well-formatted, and follows Manim best practices.
    ==========================================
    Template:
    class MatrixManipulationScene(Scene):
        def construct(self):
            # Define matrices for demonstration
            matrix1 = np.array([[1, 2], [3, 4]])
            **DEFINE MORE MATRICES**

            # Create Matrix Mobjects from numpy arrays
            m1 = Matrix(matrix1).scale(0.7)
            **DEFINE MORE MATRICES**

            # Position matrices on the scene
            m1.to_edge(LEFT)
            **DEFINE MORE MATRICES**
            self.add(m1)

            # Label matrices
            label1 = Text("Matrix A", color=BLUE).next_to(m1, UP)
            self.add(label1)
            **DEFINE MORE MATRICES**

            # Highlight a specific column before operation (customizable)
            rect = SurroundingRectangle(m1.get_columns()[1], color=YELLOW)
            self.play(Create(rect))
            self.wait(1)

            # Operation: Matrix Multiplication (Add your operations here)

            # Animate the transformation for matrix operation
            self.play(Transform(m1.copy(), result_mobject))
            self.add(result_mobject, result_label)
            self.wait(2)

            # Remove highlighting
            self.play(FadeOut(rect))

            # Cleanup for next operation or end scene
            self.play(FadeOut(m1), FadeOut(m2), FadeOut(result_mobject),
                      FadeOut(label1), FadeOut(label2), FadeOut(result_label))
            self.wait(1)

    == == == == == == == == == == == == == == == == == == == == ==
    Manim Code:
    ```python
    """


def pytorch_op(prompt): return f"""
    Generate Manim code to visualize the following machine learning code:
    ```
    {prompt}
    ```
    ==========================================
    Guidelines:
    - Omit any leading or trailing backticks.
    - USE EXACTLY THE template under "Template: " for the code generation
    - JUST PRINT THE CODE, NOTHING ELSE.
    - USE THE EXACT TEMPLATE SHOWN BELOW UNDER MANIM CODE.
    - Use the template above, **INSERT** are places where context needs to be inserted based on user's request.
    - Use the play method to animate the shapes and visualization mobjects sequentially. (You CANNOT play objects directly: self.play(SurroundingRectangle(m2.get_columns()[1], color=RED)))
    - Add wait methods between animations to provide enough time for the viewer to read and understand the content.
    - Ensure the code is complete, well-formatted, and follows Manim best practices.
    ==========================================
    Template:
    from manim import *
    from manim_ml.neural_network import Convolutional2DLayer, FeedForwardLayer, NeuralNetwork

    input_size = **INSERT** (default: 10)
    hidden_size0 = ...
    ...
    class BasicScene(Scene):
        # The code for generating our scene goes here
        def construct(self):
            # Make the neural network
            nn = NeuralNetwork([
                **INSERT NETWORK LAYERS (e.g FeedForwardLayer(num_nodes=3),)**
                ..
            ],
                layer_spacing=0.25,
            )
            # Center the neural network
            nn.move_to(ORIGIN)
            self.add(nn)
            # Make a forward pass animation
            forward_pass = nn.make_forward_pass_animation()
            # Play animation
            self.play(forward_pass)

    ==========================================
    Manim Code:
    ```python
    """


def extract_text(page):
    text = page.get_text("text")
    return text


# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/visualization")
def generate_manim_code(prompt, op="pytorch"):
    if op == "pytorch":
        manim_prompt = pytorch_op(prompt)
    else:
        manim_prompt = matrix_op(prompt)
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful assistant that generates Manim code. Just write the code nothing else",
            },
            {"role": "user", "content": manim_prompt},
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
    # [[1, 2, 3], [1, 2, 3]] @ [[1, 2, 3], [1, 2, 3]]
    prompt = f"""Generate Manim code to visualize the following machine learning code:\n
      torch.unsqueeze(0)
    """
    manim_code = generate_manim_code(prompt, op="asdf")

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
