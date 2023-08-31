#!/bin/bash

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate plm_vpf_embed
python scripts/embed_faa.py -faa "$1" -out "$2"
conda deactivate

conda activate plm_vpf_predict
python scripts/predict_function.py -faa "$1" -out "$2" --output_predictions --prediction_heatmap --output_embeddings --efam_calibration_threshold
conda deactivate