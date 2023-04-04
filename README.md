# viral_protein_function_plm
Viral protein family functional prediction using protein language models

Notes:<br />
-- must be run with osx-64 packages for the embedding procedure. (Relevant if using an ARM64 Apple Silicon chip)<br />
-- bio-transformers package has a numpy conflict with tensorflow so the faa_prediction.sh script utilizes two separate conda environments.<br />


Setup:
1. Create conda environmnet for embedding
	a. CONDA_SUBDIR=osx-64 conda env create -f plm_vpf_embed.yml

2. Create conda environment for predition
	a. conda env create -f plm_vpf_predict.yml

Test installation:
1. Run test.sh
2. output to test_out/ should match the contents of test/test_out_compare/

Quick predictions:<br \>
-- using the faa_prediction.sh script the embedding and classifier can be run from the command line with the first argument provided being a protein fasta file (e.g. example.faa) and the second argument provided being the name of an output directory (e.g. example_out)<br />

`sh faa_prediction.sh example.faa example_out`
