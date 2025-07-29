from phenotyping_segmentation.traits.height_width import (
    get_height,
    get_height_dist,
    get_centroid,
)
from tests.fixtures.data import seg_1
import pytest
import cv2
import numpy as np


@pytest.fixture
def img(seg_1):
    return cv2.imread(seg_1, cv2.IMREAD_GRAYSCALE)


@pytest.fixture
def img_nan():
    return np.array([[np.nan, np.nan], [np.nan, np.nan]])


@pytest.fixture
def img_0():
    return np.array([[0, 0], [0, 0]])


@pytest.fixture
def img_array():
    return np.array([[0, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 0]])


def test_get_height(img):
    height, top, bottom = get_height(img)
    assert height == 368
    assert top == 175
    assert bottom == 543


def test_get_height_nan(img_nan):
    height, top, bottom = get_height(img_nan)
    assert height == 0
    assert np.isnan(top)
    assert np.isnan(bottom)


def test_get_height_0(img_0):
    height, top, bottom = get_height(img_0)
    assert height == 0
    assert np.isnan(top)
    assert np.isnan(bottom)


def test_get_height_0_array(img_array):
    height, top, bottom = get_height(img_array)
    assert height == 0
    assert top == 1
    assert bottom == 1


def test_get_height_dist(img):
    (
        root_y_min,
        root_y_max,
        root_y_std,
        root_y_mean,
        root_y_median,
        root_y_p5,
        root_y_p25,
        root_y_p75,
        root_y_p95,
        root_y_mean_norm,
        root_y_median_norm,
        root_y_p5_norm,
        root_y_p25_norm,
        root_y_p75_norm,
        root_y_p95_norm,
    ) = get_height_dist(img)
    np.testing.assert_almost_equal(root_y_min, 175, decimal=2)
    np.testing.assert_almost_equal(root_y_max, 543, decimal=2)
    np.testing.assert_almost_equal(root_y_std, 95.06, decimal=2)
    np.testing.assert_almost_equal(root_y_mean, 377.97, decimal=2)
    np.testing.assert_almost_equal(root_y_median, 385.5, decimal=2)
    np.testing.assert_almost_equal(root_y_p5, 207, decimal=2)
    np.testing.assert_almost_equal(root_y_p25, 307, decimal=2)
    np.testing.assert_almost_equal(root_y_p75, 458.25, decimal=2)
    np.testing.assert_almost_equal(root_y_p95, 517, decimal=2)
    np.testing.assert_almost_equal(root_y_mean_norm, 0.55, decimal=2)
    np.testing.assert_almost_equal(root_y_median_norm, 0.57, decimal=2)
    np.testing.assert_almost_equal(root_y_p5_norm, 0.09, decimal=2)
    np.testing.assert_almost_equal(root_y_p25_norm, 0.36, decimal=2)
    np.testing.assert_almost_equal(root_y_p75_norm, 0.77, decimal=2)
    np.testing.assert_almost_equal(root_y_p95_norm, 0.93, decimal=2)


def test_get_centroid(img):
    x_centroid, y_centroid = get_centroid(img)
    np.testing.assert_almost_equal(x_centroid, 544.79, decimal=2)
    np.testing.assert_almost_equal(y_centroid, 377.97, decimal=2)
