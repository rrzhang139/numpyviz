import os
from dotenv import load_dotenv
from flask import Flask, render_template, jsonify
import fitz  # PyMuPDF
import openai
from manim import *

load_dotenv()

openai.api_key = os.getenv('API_KEY')


def extract_text(page):
    text = page.get_text("text")
    return text


# app = Flask(__name__)


# @app.route("/")
# def index():
#     return render_template("index.html")


# @app.route("/visualization")
def generate_manim_code(prompt):
    manim_prompt = f"""
    Generate Manim code to visualize the following text:
    ```
    {prompt}
    ```

    Guidelines:
    - DO NOT JUST USE TEXT. TRY TO BE IMAGINATIVE AND GENERATE ONLY VISUALIZATIONS.
    - if its a proof, please try to show some visualizations, like line graphs or vectors, whatever seems fit.
    - Create mobjects (e.g., shapes, equations, graphs) to enhance the visualization.
    - Use the play method to animate the shapes and visualization mobjects sequentially.
    - Add wait methods between animations to provide enough time for the viewer to read and understand the content.
    - Ensure the code is complete, well-formatted, and follows Manim best practices.
    - Omit any leading or trailing backticks.

    Manim Code:
    ```python
    """
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
    # Open the PDF file
    pdf_path = "Introduction_to_Linear_Algebra-_Fourth_Edition.pdf"
    doc = fitz.open(pdf_path)

    # Iterate over each page
    # for page in doc:
    # Extract text from the page
    text = extract_text(doc[196])

    # Generate Manim code using GPT API
    prompt = f"Generate Manim code to visualize the following proof or text:\n{
        text}"
    manim_code = generate_manim_code(prompt)

    # Save the Manim code to a file
    with open("visualization.py", "w") as file:
        file.write(manim_code)

    # Render the visualization using Manim
    os.system("manim -pql visualization.py")

    # Close the PDF document
    doc.close()

    # # Return the URL of the generated video
    # video_url = "/path/to/generated/video.mp4"
    # return jsonify({"videoUrl": video_url})


if __name__ == "__main__":
    # app.run(debug=True)
    main()
