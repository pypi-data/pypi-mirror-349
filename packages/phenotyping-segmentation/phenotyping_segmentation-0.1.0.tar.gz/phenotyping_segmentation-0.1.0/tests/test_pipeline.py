from phenotyping_segmentation.pipeline import pipeline_cylinder
from tests.fixtures.data import input_dir, output_dir
import os
import pandas as pd
import numpy as np
from pathlib import Path


def test_pipeline_cylinder(input_dir):
    pipeline_cylinder(input_dir)
    output_dir = Path(input_dir, "output")
    assert os.path.exists(Path(input_dir, "crop"))
    assert os.path.exists(Path(input_dir, "segmentation"))
    assert os.path.exists(Path(output_dir, "plant_original_traits"))
    assert os.path.exists(Path(output_dir, "plant_summarized_traits.csv"))

    # Check if the "crop" folder contains exactly 72 files
    crop_folder = Path(input_dir, "crop", "Day8_2024-11-15", "C-1")
    valid_extensions = (".png", ".jpg", ".jpeg", ".tif", ".bmp")
    frames = [
        file
        for file in os.listdir(crop_folder)
        if (not file.startswith(".")) and file.lower().endswith(valid_extensions)
    ]
    assert len(frames) == 72, f"Expected 72 files in 'crop', found {len(frames)}"

    # check summary traits
    summary_df = pd.read_csv(Path(output_dir, "plant_summarized_traits.csv"))
    assert summary_df.shape == (7, 932)
    np.testing.assert_almost_equal(summary_df["sdxy_mean"][1], 0.14, decimal=2)
