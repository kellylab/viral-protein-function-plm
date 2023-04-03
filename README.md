# viral_protein_function_plm
Viral protein family functional prediction using protein language models

Notes:
-- Must be run with osx-64 packages for the embedding procedure. (Relevant if using an ARM64 Apple Silicon chip)\n
--bio-transformers package has a numpy conflict with tensorflow so the faa_prediction.sh script utilizes two separate conda environments.\n


Setup:
1. Create conda environmnet for embedding
	a. CONDA_SUBDIR=osx-64 conda env create -f plm_vpf_embed.yml

2. Create conda environment for predition
	a. conda create env create -f plm_vpf_predict.yml

3. Run scripts/faa_prediction.sh
