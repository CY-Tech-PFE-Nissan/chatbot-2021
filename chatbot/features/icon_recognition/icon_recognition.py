import io
from pathlib import Path

import torch
import torchvision.transforms as transforms
from PIL import Image

from .models.cnn import CNN

model_folder = Path(__file__).resolve().parent / "models"


def transform_images(img_bytes):
    """
    Transforms images from bytes to tensors
    ---------
    Input
    img_bytes: bytes
    -------
    Output
    my_transforms: torchvision.transforms
    """
    my_transforms = transforms.Compose(
        [transforms.Resize((64, 64)), transforms.ToTensor()]
    )

    image = Image.open(io.BytesIO(img_bytes)).convert("L")
    return my_transforms(image).unsqueeze(0)


def get_prediction(img_bytes):
    """
    Predicts a label based on an image (as bytes)
    ---------
    Input
    img_bytes: bytes (image)
    -------
    Output
    out: str (label)
    """
    # Every possible class name
    class_names = [
        "Engine Oil Pressure",
        "Low Tire Pressure",
        "Seat Belt",
        "Slip Indicator",
    ]

    # Loading model
    model = CNN(n_classes=4)
    model.load_state_dict(torch.load(model_folder / "cnn.pth"))
    model = model.to("cpu")
    model.eval()

    # Processing and predicting image
    tensor = transform_images(img_bytes=img_bytes)
    output = model.forward(tensor)
    _, pred = torch.max(output, 1)
    index = pred.squeeze(0).numpy()

    # Translating prediction
    out = class_names[index]
    return out
