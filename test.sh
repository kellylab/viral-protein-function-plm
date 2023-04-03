#!/bin/bash

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate plm_vpf_embed
python scripts/embed_faa.py -faa test/test.faa -out test_out
conda deactivate

conda activate plm_vpf_predict
python scripts/predict_function.py -faa test/test.faa -out test_out --output_predictions --prediction_heatmap --output_embeddings
conda deactivate