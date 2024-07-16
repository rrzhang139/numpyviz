"""
This module provides a Flask application for visualizing numpy operations using manim.
"""

from templates.broadcast import BroadcastingAnimation
from templates.split import SplitOperation
from templates.transpose import MatrixTransposition
from templates.elementwise import ElementWiseOperation
import os
from manim import tempconfig
from typing import List, Dict
import numpy as np
from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from parse import ArrayNode, OperationNode, parse

from templates.matmul import MatrixMultiplication
from templates.reduction import ReductionOperation
from templates.concat import ConcatenationOperation
from templates.reshape import (ExpandDimsOperation, FlattenOperation,
                               RavelOperation, ReshapeOperation, SqueezeOperation)

app = Flask(__name__)
CORS(app, resources={
     r"/visualize": {"origins": ["http://127.0.0.1:3000", "https://numpyviz.vercel.app/"]}})

ELEMENTWISE_OPS = ["add", "subtract", "multiply", "divide", "floor_divide", "mod", "power",
                   "sin", "cos", "tan", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh",
                   "arcsinh", "arccosh", "arctanh", "exp", "expm1", "exp2", "log", "log10",
                   "log2", "log1p", "round", "floor", "ceil", "trunc", "sqrt", "cbrt",
                   "square", "abs", "fabs", "sign", "heaviside", "maximum", "minimum"]

MEDIA_DIR = os.path.join(os.getcwd(), 'media')
VIDEO_DIR = os.path.join(MEDIA_DIR, 'videos')
os.makedirs(VIDEO_DIR, exist_ok=True)


@app.route('/')
def index() -> str:
    """Serves the index page."""
    return send_file('index.html')


@app.route('/visualize', methods=['POST'])
def visualize() -> str:
    """
    Main handler for generating visualization.
    Returns a JSON response with the results of the visualization.
    """
    numpy_code = request.json['code']

    try:
        # Sanity check: run python code
        # safe_globals = {"np": np}
        # exec(numpy_code, safe_globals)
        # print("after exec")

        op_nodes = parse(numpy_code)
        print("after parse")
        results = process_operations(op_nodes)
        print("after operations")
        return jsonify(results)
    except Exception as e:
        # If parsing or processing fails, return an error response
        return jsonify({"error": str(e)}), 400


def process_operations(operation_nodes: List[OperationNode]) -> List[Dict[str, str]]:
    """
    Processes the operations and generates the manim animations.
    Returns a list of dictionaries with the results of the operations.
    """
    results = []
    for i, node in enumerate(operation_nodes):
        node.compute()
        animation_generated = generate_manim_animation(node, i)
        result = {
            "operation": node.operation,
            "input": f"Operands: {node.operands}, Keyword Args: {node.kwargs}",
            "output": str(node.result),
        }
        if animation_generated:
            result["video_url"] = f"/video/{i}"
        else:
            result["message"] = "This operation is not supported for Manim animation."
        results.append(result)
    return results


def generate_manim_animation(node: OperationNode, index: int) -> bool:
    """
    Generates a manim animation for the given operation node.
    The animation is saved to a file with the given index.
    """
    operation = node.operation
    op_args = node.operands
    kwargs = node.kwargs
    output_file = f'Visualization_{index}'

    for operand in op_args:
        if not isinstance(operand, (np.ndarray, list, tuple, int, float)):
            raise ValueError(f"Invalid operand type: {type(operand)}")

    custom_config = {
        "output_file": output_file,
        "format": "mp4",
        "media_dir": MEDIA_DIR,
        "video_dir": VIDEO_DIR,
        "images_dir": os.path.join(MEDIA_DIR, "images"),
        "tex_dir": os.path.join(MEDIA_DIR, "Tex"),
        "text_dir": os.path.join(MEDIA_DIR, "texts"),
        "partial_movie_dir": os.path.join(MEDIA_DIR, "partial_movie_files"),
        "quality": "low_quality",
        "frame_rate": 5,
        "pixel_width": 854,
        "pixel_height": 480
    }

    with tempconfig(custom_config):
        if operation in ELEMENTWISE_OPS:
            scene = ElementWiseOperation(
                *op_args, operation=operation, result=node.result, ** kwargs)
        elif operation in ["matmul", "dot"]:
            scene = MatrixMultiplication(
                *op_args, **kwargs)
        elif operation in ["sum", "mean", "max", "min", "median", "std", "var", "prod", "average"]:
            scene = ReductionOperation(
                *op_args, operation=operation, result=node.result, ** kwargs)
        elif operation == "reshape":
            scene = ReshapeOperation(*op_args, result=node.result, ** kwargs)
        elif operation == "ravel":
            scene = RavelOperation(*op_args, result=node.result, **kwargs)
        elif operation == "flatten":
            scene = FlattenOperation(*op_args, result=node.result, **kwargs)
        elif operation == "squeeze":
            scene = SqueezeOperation(*op_args, result=node.result, **kwargs)
        elif operation == "expand_dims":
            scene = ExpandDimsOperation(*op_args, result=node.result, **kwargs)
        elif operation == "concatenate":
            scene = ConcatenationOperation(
                *op_args, result=node.result, **kwargs)
        elif operation == "split":
            scene = SplitOperation(*op_args, result=node.result, **kwargs)
        elif operation == "transpose":
            scene = MatrixTransposition(*op_args, **kwargs)
        elif operation == "broadcast_to":
            scene = BroadcastingAnimation(
                *op_args, result=node.result, **kwargs)
        else:
            return False
        print("render")

        scene.render()
    return True


@app.route('/video/<int:index>')
def serve_video(index: int):
    video_path = os.path.join(VIDEO_DIR, f'Visualization_{index}.mp4')
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        abort(404, description="Video file not found")

    try:
        return send_file(video_path, mimetype='video/mp4', as_attachment=False)
    except Exception as e:
        print(f"Error serving video: {str(e)}")
        abort(500, description="Error serving video")


if __name__ == '__main__':
    app.run(port=5000, debug=True)
