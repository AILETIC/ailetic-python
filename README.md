# Ailetic

Ailetic is a powerful and flexible pip package that simplifies the process of creating customizable Flask web server backends. Designed with dynamic route and pipeline registration, it allows for efficient preprocessing and handling of various types of input data, making it an ideal choice for AI and ML applications, image processing, audio processing, and more.

## Features

- **Dynamic Route Definition**: Easily define routes with associated HTTP methods and custom processing functions.
- **Customizable Preprocessing Pipelines**: Support for multiple types of preprocessing pipelines, such as image-to-image and text-to-audio conversions.
- **Error Handling and Validation**: Robust input validation and error handling ensure the reliability and security of your backend services.
- **Flexible and Extensible**: Tailor the server to meet your specific needs, whether for AI model inference, data preprocessing, or any custom backend logic.

## Installation

Install Ailetic using pip:

```sh
pip install ailetic
```

## Getting Started

To get started with Ailetic, create a new Python file (e.g., `app.py`) and import the necessary components from the Ailetic package:

```python
from ailetic import LocalServer, PipelineType
```

Define your custom processing functions and use the `LocalServer` class to set up your routes and start the server:

```python
# Define custom processing function
def custom_processing_function(input_data):
    # Processing logic here
    return processed_data

# Initialize server
server = LocalServer()

# Add route with a preprocessing pipeline
server.add_route(
    "your-route",
    view_func=custom_processing_function,
    pipeline=PipelineType.YOUR_PIPELINE_TYPE,
    methods=["POST"]
)

# Run server
server.run(host="0.0.0.0", port=5001, debug=True)
```

Replace `"your-route"`, `custom_processing_function`, and `PipelineType.YOUR_PIPELINE_TYPE` with your actual route, processing function, and pipeline type.

## Usage Example

Below is an example of setting up a route for an image upscaling service:

```python
from ailetic import LocalServer, PipelineType
import numpy as np

def upscale_image(image_array: np.ndarray) -> np.ndarray:
    # Image upscaling logic here
    return upscaled_image

server = LocalServer()

server.add_route(
    "image-upscale",
    view_func=upscale_image,
    pipeline=PipelineType.IMAGE_TO_IMAGE,
    methods=["POST"]
)

server.run(host="0.0.0.0", port=5001, debug=True)
```

## Contributing

We welcome contributions to Ailetic! Whether it's adding new features, fixing bugs, or improving documentation, your help is appreciated. Please check our contribution guidelines for more information on how to get involved.


## License

This project is licensed under the GNU General Public License v3.0. For more details, see the [LICENSE](LICENSE) file included in this repository.

---

This approach keeps your README clean and straightforward, while still making it clear under what license the project is released. It also provides a direct link to the LICENSE file in your repository, where users can read the full license text.