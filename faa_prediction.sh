#!/bin/bash

CONDA_BASE=$(conda info --base)
source $CONDA_BASE/etc/profile.d/conda.sh

conda activate plm_vpf_embed
python scripts/embed_faa.py -faa GCA_003344105.1_ASM334410v1_protein.faa -out out
conda deactivate

conda activate plm_vpf_predict
python scripts/predict_function.py -faa GCA_003344105.1_ASM334410v1_protein.faa -out out --output_predictions --prediction_heatmap --output_embeddings
conda deactivate