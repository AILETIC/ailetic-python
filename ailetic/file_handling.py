import io
import base64
from PIL import Image
import numpy as np
from pydub import AudioSegment

def ndarray_to_base64(img_array, format='PNG'):
    """
    Converts a NumPy ndarray to a base64-encoded string.
    
    Args:
        img_array (np.ndarray): The image array to convert.
        format (str): The format to save the image in.
    
    Returns:
        str: Base64-encoded image.
    """
    pil_img = Image.fromarray(img_array.astype('uint8'))
    buffer = io.BytesIO()
    pil_img.save(buffer, format=format)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")

def ndarray_to_base64_mp3(audio_data, sampling_rate=44100):
    """
    Converts a NumPy ndarray containing audio data to a base64-encoded MP3.
    
    Args:
        audio_data (np.ndarray): Audio data array.
        sampling_rate (int): Audio sampling rate.
    
    Returns:
        str: Base64-encoded MP3 audio.
    """
    audio_data = (audio_data * np.iinfo(np.int16).max).astype(np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=sampling_rate, sample_width=2, channels=1)
    buffer = io.BytesIO()
    audio_segment.export(buffer, format="mp3")
    return base64.b64encode(buffer.getvalue()).decode('utf-8')
