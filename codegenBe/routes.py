from flask import Blueprint, request, jsonify
from utils.code_generation import generate_code_from_logic
from utils.algorithm import generate_algorithm
from utils.flowchart import generate_flowchart
from transformers import pipeline
import subprocess

# Define the Blueprint for generating code
generate_code_route = Blueprint('generate_code', __name__)

# Initialize the Hugging Face model pipeline (optional, for efficiency, could be moved to code_generation.py)
pipe = pipeline("text-generation", model="HuggingFaceTB/SmolLM2-1.7B-Instruct", device=0)

@generate_code_route.route('/generate', methods=['POST'])
def generate_code():
    try:
        data = request.get_json()
        logic = data.get('logic', '')

        # Generate Python code using Hugging Face model
        generated_code = generate_code_from_logic(logic, pipe)

        # Generate algorithm and flowchart from the generated code
        algorithm=generate_algorithm(generated_code)
        flowchart_filename = generate_flowchart(algorithm)

        return jsonify({"generated_code": generated_code, "algorithm": algorithm, "flowchart_filename": flowchart_filename})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Define the Blueprint for running code
run_code_route = Blueprint('run_code', __name__)

@run_code_route.route('/run', methods=['POST'])
def run_code():
    try:
        data = request.get_json()
        code = data.get('code', '')

        # Execute the generated Python code using subprocess (sandboxing it)
        result = subprocess.run(
            ['python', '-c', code],
            capture_output=True,
            text=True
        )

        # Return the output of the code execution
        if result.returncode == 0:
            return jsonify({"output": result.stdout})
        else:
            return jsonify({"error": result.stderr}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500
