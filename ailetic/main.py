from ailetic import LocalServer, PipelineType
import numpy as np
import torch
import torchvision
from PIL import Image

def remove_background(image_array: np.ndarray) -> np.ndarray:
    """
    Removes the background from an image using a pretrained FCN ResNet101 model.
    
    Args:
        image_array (np.ndarray): Input image as a NumPy array.
    
    Returns:
        np.ndarray: Image array with background removed.
    """
    # Convert numpy array to PIL Image
    pil_img = Image.fromarray(image_array)
    
    # Load pretrained segmentation model
    model = torchvision.models.segmentation.fcn_resnet101(pretrained=True)
    model.eval()

    # Define transformations
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToTensor(),
        torchvision.transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        torchvision.transforms.Resize((256, 256))
    ])
    
    # Apply transformations
    image_tensor = transform(pil_img).unsqueeze(0)

    # Inference
    with torch.no_grad():
        output = model(image_tensor)['out'][0].argmax(0).unsqueeze(0)

    # Create mask and resize to original image size
    mask = torch.vstack([output, output, output]).float()
    mask = torch.nn.functional.interpolate(mask.unsqueeze(0), size=image_array.shape[:2], mode='bilinear', align_corners=False)[0]
    mask = mask.cpu().permute(1, 2, 0).numpy() * 255
    mask = mask.astype(np.uint8)

    # Apply mask to original image
    masked_image = np.where(mask > 0, image_array, 255)
    
    return masked_image

def to_grayscale(image_array: np.ndarray) -> np.ndarray:
    """
    Converts an image to grayscale.
    
    Args:
        image_array (np.ndarray): Input image as a NumPy array.
    
    Returns:
        np.ndarray: Grayscale image array.
    """
    return np.mean(image_array, axis=2).astype(np.uint8)

def main():
    server = LocalServer()

    server.add_route(
        "image-to-image",
        view_func=remove_background,
        pipeline=PipelineType.IMAGE_TO_IMAGE,
        methods=["POST"]
    )
    
    server.run(
        host="0.0.0.0",
        port=5001,
        debug=True
    )

if __name__ == "__main__":
    main()
