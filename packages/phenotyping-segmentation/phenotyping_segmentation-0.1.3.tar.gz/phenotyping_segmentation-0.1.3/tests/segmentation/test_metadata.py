from phenotyping_segmentation.segmentation.metadata import write_metadata
from phenotyping_segmentation.pre_processing.crop_image_roi import crop_save_image_plant
from tests.fixtures.data import input_dir, scans_csv
import pytest
import pandas as pd


@pytest.fixture
def scans_df(scans_csv):
    scans_df = pd.read_csv(scans_csv)
    return scans_df


def test_write_metadata(input_dir, scans_df):
    crop_paths = crop_save_image_plant(scans_df)
    assert len(crop_paths) == 7

    metadata_file = write_metadata(crop_paths, input_dir)
    metadata = pd.read_csv(metadata_file)
    assert metadata.shape == (504, 3)
    assert (
        metadata["image_path"][0]
        == "x:/users/linwang/phenotyping-segmentation/tests/data/crop/Day8_2024-11-15/C-1/1.jpg"
    )
