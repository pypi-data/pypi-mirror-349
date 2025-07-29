import os
import json
import torch
import pandas as pd
from pathlib import Path
from phenotyping_segmentation.pre_processing.crop_image_roi import *
from phenotyping_segmentation.segmentation.augmentation import *
from phenotyping_segmentation.segmentation.color import *
from phenotyping_segmentation.segmentation.dataset import *
from phenotyping_segmentation.segmentation.metadata import *
from phenotyping_segmentation.segmentation.model_parameters import *
from phenotyping_segmentation.segmentation.one_hot import *
from phenotyping_segmentation.segmentation.preprocessing import *
from phenotyping_segmentation.post_processing.buffer import *
from phenotyping_segmentation.post_processing.remove_unconnected import *
from phenotyping_segmentation.traits.area import *
from phenotyping_segmentation.traits.convex_hull import *
from phenotyping_segmentation.traits.d95 import *
from phenotyping_segmentation.traits.ellipse import *
from phenotyping_segmentation.traits.get_traits import *
from phenotyping_segmentation.traits.height_width import *
from phenotyping_segmentation.traits.scanline import *
from phenotyping_segmentation.traits.sdxy import *
from phenotyping_segmentation.traits.summary import *
from phenotyping_segmentation.util.subfolder import *


def pipeline_cylinder(input_dir):
    # load scans_csv as dataframe
    scans_csv = Path(input_dir, "scans.csv")
    scans_df = pd.read_csv(scans_csv)

    # load params_json as dict
    params_json = Path(input_dir, "params.json")
    with open(params_json) as f:
        params = json.load(f)
    model_name = params["model_name"]
    nlayer_d95 = int(params["nlayer_d95"])
    calculate_layerTraits = params["calculate_layerTraits"]
    layerNum_layeredTraits = int(params["layerNum_layeredTraits"])
    plantRegion_layeredTraits = params["plantRegion_layeredTraits"]

    # add device
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    output_dir = Path(input_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # crop the original image in scans_df and save cropped images in {output}/crop
    crop_paths = crop_save_image_plant(scans_df)

    # write metadata
    metadata_path = write_metadata(crop_paths, input_dir)

    # load segmentation model and parameters
    (
        best_model,
        select_classes,
        select_class_rgb_values,
        preprocessing_fn,
    ) = setup_model_parameters(input_dir, model_name, DEVICE)
    # setup dataset
    test_dataset, test_dataset_vis = setup_dataset(
        metadata_path, select_class_rgb_values, preprocessing_fn
    )

    # predict cropped images
    seg_raw_plant_root_folders = seg_dataset(
        test_dataset, test_dataset_vis, DEVICE, best_model, select_class_rgb_values
    )

    # remove unconnected area
    seg_raw_subfolders = get_subfolders(seg_raw_plant_root_folders)
    min_size_small = 300
    min_size_large = 3000
    seg_plant_root_folders = seg_raw_plant_root_folders.replace(
        "segmentation_raw", "segmentation"
    )
    for subfolder in seg_raw_subfolders:
        remove_unconnection(
            subfolder,
            subfolder.replace("segmentation_raw", "segmentation"),
            min_size_small,
            min_size_large,
        )

    # get traits
    # get all plant folders
    seg_plant_subfolders = []
    valid_extensions = (".png", ".jpg", ".jpeg", ".tif", ".bmp")
    for dirpath, dirnames, filenames in os.walk(seg_plant_root_folders):
        if (
            any(fname.lower().endswith(valid_extensions) for fname in filenames)
            and not dirnames
        ):
            seg_plant_subfolders.append(dirpath)

    # trait analysis
    summary_df = pd.DataFrame()
    for seg_path in seg_plant_subfolders:
        seg_path = seg_path.replace("\\", "/")
        df = get_traits(
            seg_path,
            nlayer_d95,
            calculate_layerTraits,
            layerNum_layeredTraits,
            plantRegion_layeredTraits,
        )
        traits_fname = (
            "plant_original_traits/"
            + seg_path.split("/segmentation/")[1].replace("/", "_")
            + ".csv"
        )
        save_name = Path(output_dir, traits_fname)
        save_path = os.path.dirname(save_name)
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        df.to_csv(save_name, index=False)

        df = pd.read_csv(save_name)
        traits_df = df
        group_index = "plant"

        # get plant summary
        summary_df = get_statistics_df(traits_df, group_index, summary_df)
        # merge the summary dataframe with scans information
        summary_df["scan_path"] = summary_df["plant"].str.replace(
            "/segmentation/", "/images/"
        )
        merged_df = (
            scans_df.assign(
                key=scans_df["scan_path"].apply(
                    lambda x: next((y for y in summary_df["scan_path"] if y in x), None)
                )
            )
            .merge(summary_df, left_on="key", right_on="scan_path", how="left")
            .drop(columns=["key"])
        )
        merged_df.to_csv(
            Path(output_dir, "plant_summarized_traits.csv"),
            index=False,
        )
