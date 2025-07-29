import pytest
import cv2
import json
import torch
import numpy as np


@pytest.fixture
def original_images():
    """Path to a folder with the original images."""
    return "tests/data/Day8_2024-11-15"


@pytest.fixture
def original_image_1():
    """Path to a folder with the original images."""
    return "tests/data/images/Day8_2024-11-15/C-1/1.jpg"


@pytest.fixture
def crop_image_1():
    """Path to a folder with the original images."""
    return "tests/data/crop/1.jpg"


@pytest.fixture
def crop_label_1():
    """Path to a folder with a label."""
    return "tests/data/label/18_D_R8_19.png"


@pytest.fixture
def seg_1():
    """Path to a folder with a label."""
    return "tests/data/segmentation/Day8_2024-11-15/C-1/1.png"


@pytest.fixture
def seg_seperate_branch():
    """Path to a folder with a label."""
    return "tests/data/segmentation/Day8_2024-11-15/C-10/23.png"


@pytest.fixture
def seg_good():
    """Path to a folder with a label."""
    return "tests/data/segmentation/Day8_2024-11-15/E-3/38.png"


@pytest.fixture
def input_dir():
    """Input directory."""
    return "tests/data"


@pytest.fixture
def output_dir():
    """Output directory."""
    return "tests/data/output"


@pytest.fixture
def params_json():
    """Parameters json file."""
    return "tests/data/params.json"


@pytest.fixture
def model_name(params_json):
    """Trained model name."""
    with open(params_json) as f:
        params = json.load(f)
    model_name = params["model_name"]
    return params["model_name"]


@pytest.fixture
def DEVICE():
    """Get device."""
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return DEVICE


@pytest.fixture
def scans_csv():
    """Path to the scans.csv file."""
    return "tests/data/scans.csv"


@pytest.fixture
def metadata_path():
    """Path to the metadata."""
    return "tests/data/metadata_tem.csv"


@pytest.fixture
def select_class_rgb_values():
    """Selected RGB values for selected classes."""
    return np.array([[0, 0, 0], [128, 0, 0]])
