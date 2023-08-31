# Viral protein function using Protein Language Model
Viral protein high-level function prediction. Categories are defined by the PHROGs database (https://phrogs.lmge.uca.fr/)

To access the classifier with no-code, use our Google Colab notebook- https://colab.research.google.com/drive/1ZjxgOtWU335fkEXRVyTq5FCWhbVyQEQM?usp=sharing

We have tested the installation on multiple Mac and Windows systems. If you are having a problem with installation please leave an issue and we will do our best to address it. 

Installation (must be run with conda):
1. Download codebase
2. Create conda environmnet for embedding (must be with osx-64 environment on x86_64 architechture due to dependency requirement)
	a. conda env create -f plm_vpf_embed.yml

3. Create conda environment for predition
	a. conda env create -f plm_vpf_predict.yml

Test installation:
1. Run test.sh
2. compare output (test_out/) to the contents of test/test_out_compare/

Notes:<br />
-- must be run with osx-64 packages for the embedding procedure. (Relevant if using an ARM64 Apple Silicon chip)<br />
-- bio-transformers package has a numpy conflict with tensorflow so the faa_prediction.sh script utilizes two separate conda environments.<br />

Quick predictions:<br />
-- using the faa_prediction.sh script the embedding and classifier can be run from the command line with the first argument provided being a protein fasta file (e.g. example.faa) and the second argument provided being the name of an output directory (e.g. example_out)<br />

`sh faa_prediction.sh example.faa example_out`
