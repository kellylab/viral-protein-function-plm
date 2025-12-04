#!/bin/bash

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate plm_vpf_predict_cpu
python scripts/embed_faa.py -faa test/test.faa -out test_out

python scripts/predict_function.py -faa test/test.faa -out test_out --output_predictions --prediction_heatmap --output_embeddings --efam_calibration_threshold
conda deactivate