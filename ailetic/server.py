from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from PIL import Image
from dataclasses import dataclass
from functools import wraps
from .file_handling import ndarray_to_base64, ndarray_to_base64_mp3

def process_pipeline(data, pipeline_type, pre=True):
    """
    Processes data based on the specified pipeline type.
    
    Args:
        data: The input data. This could be a file (during pre-processing) or a numpy.ndarray (during post-processing).
        pipeline_type (PipelineType): The type of processing pipeline.
        pre (bool): Flag indicating whether it's a pre-processing or post-processing step.
    
    Returns:
        The processed data, which varies depending on the pipeline and the step.
    """
    if pipeline_type == PipelineType.IMAGE_TO_IMAGE:
        if pre:
            # Handle file input during pre-processing
            image = Image.open(data.stream)
            image_array = np.array(image)
            return image_array
        else:
            # Handle numpy.ndarray during post-processing
            return ndarray_to_base64(data)
    
    elif pipeline_type == PipelineType.TEXT_TO_AUDIO:
        if pre:
            # Pre-processing for text-to-audio (placeholder logic here)
            return data
        else:
            # Convert numpy.ndarray to audio in post-processing
            return ndarray_to_base64_mp3(data)
    
    # Additional pipeline types can be added here with their respective logic
    
    else:
        raise ValueError("Unsupported pipeline type")


@dataclass
class PipelineType:
    TEXT_TO_AUDIO = 1   # text -> MODEL -> np.ndarray to mp3 to base64
    IMAGE_TO_IMAGE = 2  # file to np.ndarray -> MODEL -> np.ndarray to base64

class LocalServer:
    def __init__(self):
        self.base_url = "/api/compute/"
        self.app = self.create_app()
        self.routes = {}

    def add_route(self, rule, view_func, pipeline, **options):
        """
        Adds a route to the Flask application.
        
        Args:
            rule (str): The endpoint URL.
            view_func (callable): The function to execute for this route.
            pipeline (PipelineType): The type of processing pipeline.
            **options: Additional options for the route.
        """
        @wraps(view_func)
        def wrapped_view_func(*args, **kwargs):
            data = request.files.get('file') or request.form.get('data')
            if not data:
                return jsonify(error="Data not provided"), 400

            processed_input = process_pipeline(data, pipeline, pre=True)
            processed = view_func(processed_input)
            result = process_pipeline(processed, pipeline, pre=False)

            return jsonify({"result": result})

        self.routes[rule] = {"view_func": wrapped_view_func, "options": options}

    def run(self, **kwargs):
        for rule, details in self.routes.items():
            self.app.add_url_rule(self.base_url + rule, view_func=details["view_func"], **details["options"])
        self.app.run(**kwargs)

    def create_app(self):
        app = Flask(__name__)
        CORS(app)
        return app
