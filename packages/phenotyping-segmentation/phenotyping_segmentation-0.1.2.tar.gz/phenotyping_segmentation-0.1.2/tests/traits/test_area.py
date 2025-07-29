from phenotyping_segmentation.traits.area import get_area_pixel
from tests.fixtures.data import seg_1
import cv2
import pytest
import numpy as np


@pytest.fixture
def img_0():
    return np.array([0, 0, 0, 0])


def test_get_area_pixel(seg_1):
    img = cv2.imread(seg_1)
    area = get_area_pixel(img)
    assert area == 10632


def test_get_area_pixel_0(img_0):
    area = get_area_pixel(img_0)
    assert area == 0
