<h1 align="center">
    <span class="title-main">WildWaterSplatting</span><br>
    <span class="title-small">Occluder-Masking Underwater Gaussian Splatting</span>
</h1>

<br>

<p align="center">
  <img alt="WaterSplatting Reconstruction" src="./wws_splitscreen.gif" />
</p>

<p align="justify">
    This repository introduces WildWaterSplatting, a Gaussian Splatting method that combines underwater lighting dynamics modelling and occluder masking with an auxiliary model. WildWaterSplatting is built on top of WaterSplatting with the addition of a U-Net masking model from the method Gaussians in the Wild. Through this combination, WildWaterSplatting shows improved reconstruction of highly dynamic scenes containing large quantities of moving marine animals and marine snow.
</p>

<br>

## Installation

This method is built on WaterSplatting; therefore, all setup instructions are the same. This repository is a fork of the original WaterSplatting repository:

https://github.com/water-splatting/water-splatting

### Create environment
```bash
conda create --name wild_water_splatting -y python=3.8
conda activate wild_water_splatting
python -m pip install --upgrade pip
```

### Install WaterSplatting

```bash
# Install PyTorch
pip uninstall torch torchvision functorch tinycudann
pip install torch==2.1.2+cu118 torchvision==0.16.2+cu118 --extra-index-url https://download.pytorch.org/whl/cu118

# Install cuda-toolkit with conda
conda install -c "nvidia/label/cuda-11.8.0" cuda-toolkit

# Install tiny-cuda-nn
pip install ninja git+https://github.com/NVlabs/tiny-cuda-nn/#subdirectory=bindings/torch

# Install nerfstudio
pip install nerfstudio==1.1.4
ns-install-cli

# WaterSplatting
git clone git@github.com:water-splatting/water-splatting.git
cd water-splatting
git submodule init
git submodule update --recursive
pip install --no-use-pep517 -e .
```

## Data Preprocessing
To keep consistency across different models, we recomputed the camera intrinsic/extrinsic parameters and performed distortion corrections using [COLMAP](https://github.com/colmap/colmap)'s `image_undistorter` on [SeaThru-NeRF](https://sea-thru-nerf.github.io/) dataset:
```bash
colmap image_undistorter \
  --image_path /your_path_to_dataset/SeathruNeRF_dataset/IUI3-RedSea/images_wb \
  --input_path /your_path_to_dataset/SeathruNeRF_dataset/IUI3-RedSea/colmap/sparse/0 \
  --output_path /your_path_to_dataset/undistorted_seathrunerf_dataset/IUI3-RedSea \
  --output_type COLMAP
```

## Training
To start the training on the undistorted SeaThru-NeRF dataset, run the following commands:
```bash
cd /your_path_to_repo/water-splatting
ns-train water-splatting --vis viewer+wandb colmap --downscale-factor 1 --colmap-path sparse --data /your_path_to_dataset/undistorted_seathrunerf_dataset/IUI3-RedSea --images-path images
```

Or, to start the training on the original [SeaThru-NeRF](https://sea-thru-nerf.github.io/) dataset, run the following commands:
```bash
cd /your_path_to_repo/water-splatting
ns-train water-splatting --vis viewer+wandb colmap --downscale-factor 1 --colmap-path sparse/0 --data /your_path_to_dataset/SeathruNeRF_dataset/IUI3-RedSea --images-path Images_wb
```
Please note that: The training and testing splits reported in our paper are different from the default splits in nerfstudio, and are consistent with the splits used in the SeaThru-NeRF paper.

## Evaluation

```bash
cd /your_path_to_repo/water-splatting
ns-eval --load-config outputs/unnamed/water-splatting/your_timestamp/config.yml --render-output-path renders/eval
```

## Interactive viewer
To start the viewer and explore the trained models, run one of the following:
```bash
ns-viewer --load-config outputs/unnamed/water-splatting/your_timestamp/config.yml
```

## Rendering videos
To render a video on a trajectory (e.g., generated from the interactive viewer), run:
```bash
ns-render camera-path --load-config outputs/unnamed/water-splatting/your_timestamp/config.yml --camera-path-filename /your_path_to_dataset/SeathruNeRF_dataset/IUI3-RedSea/camera_paths/your_trajectory.json --output-path renders/IUI3-RedSea/water_splatting.mp4
```

Please note that the default output quality is lossy.

## Rendering dataset
To render testing set for a checkpoint, run:
```bash
ns-render dataset --load-config outputs/unnamed/water-splatting/your_timestamp/config.yml --data /your_path_to_dataset/SeathruNeRF_dataset/IUI3-RedSea
```
Please note that the default output quality is lossy.
</p>
</section>

## Acknowledgements
This work was supported by the Czech Science Foundation (GACR) EXPRO (grant no. 23-07973X), and by the Ministry of Education, Youth and Sports of the Czech Republic through the e-INFRA CZ (ID:90254).
Jonas Kulhanek acknowledges travel support from the European Union’s Horizon 2020 research and innovation programme under ELISE (grant no. 951847).

## Citation
If you find our code or paper useful, please cite:
```bibtex
@article{li2025watersplatting,
  title={{W}ater{S}platting: Fast Underwater {3D} Scene Reconstruction using Gaussian Splatting},
  author={Li, Huapeng and Song, Wenxuan and Xu, Tianao and Elsig, Alexandre and Kulhanek, Jonas},
  journal={3DV},
  year={2025}
}
```
