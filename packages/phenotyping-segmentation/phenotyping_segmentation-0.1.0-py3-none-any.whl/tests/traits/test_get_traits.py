from phenotyping_segmentation.traits.get_traits import get_traits
from tests.fixtures.data import output_dir
import pytest
import os
import numpy as np


@pytest.fixture
def seg_path_1():
    return "tests/data/segmentation/Day8_2024-11-15/C-1"


@pytest.fixture
def seg_path():
    return "tests/data/segmentation"


def test_get_traits(seg_path_1):
    traits_df = get_traits(seg_path_1, True, 50, 3, True)
    traits_df = traits_df.reset_index(drop=True)
    assert traits_df.shape == (72, 103)
    assert traits_df["area"][0] == 3544
    np.testing.assert_almost_equal(traits_df["chull_area"][0], 9235.5, decimal=2)
    np.testing.assert_almost_equal(traits_df["y_centroid"][9], 371.86, decimal=2)
    np.testing.assert_almost_equal(traits_df["root_y_mean"][11], 373.77, decimal=2)
    np.testing.assert_almost_equal(traits_df["angle_top"][20], 13.5, decimal=2)
    np.testing.assert_almost_equal(traits_df["layer_1_angle_avg"][25], 4.65, decimal=2)
    np.testing.assert_almost_equal(traits_df["layer_3_area"][29], 863, decimal=2)
    np.testing.assert_almost_equal(traits_df["angle_whole_height"][32], 0.02, decimal=2)


def test_get_traits_all(seg_path, output_dir):
    layerNum_layeredTraits = 3
    plantRegion_layeredTraits = True
    nlayer_d95 = 50
    calculate_layerTraits = True

    seg_plant_subfolders = []
    valid_extensions = (".png", ".jpg", ".jpeg", ".tif", ".bmp")
    for dirpath, dirnames, filenames in os.walk(seg_path):
        if (
            any(fname.lower().endswith(valid_extensions) for fname in filenames)
            and not dirnames
        ):
            seg_plant_subfolders.append(dirpath)

    for seg_path in seg_plant_subfolders:
        df = get_traits(
            os.path.join(seg_path),
            nlayer_d95,
            calculate_layerTraits,
            layerNum_layeredTraits,
            plantRegion_layeredTraits,
        )
        traits_fname = (
            "plant_original_traits"
            + seg_path.split("segmentation")[1].replace("/", "_")
            + ".csv"
        )
        save_name = os.path.join(output_dir, traits_fname)
        save_path = os.path.dirname(save_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        df.to_csv(save_name, index=False)
    assert df.shape == (72, 103)
