# Viral Protein Function prediction using Protein Language Model (VPF-PLM)
Viral protein high-level function prediction. Categories are defined by the PHROGs database (https://phrogs.lmge.uca.fr/).

To access the classifier with no-code, use our Google Colab notebook- https://colab.research.google.com/drive/1ZjxgOtWU335fkEXRVyTq5FCWhbVyQEQM?usp=sharing

We have tested the installation on multiple Mac, Windows, and Linux systems. If you are having a problem with installation please leave an issue and we will do our best to address it. 

Installation:  
1. Download codebase
2. Environment setup requires conda and there are two environments that need to be setup. This process takes some time.  
        a. Create conda environmnet for embedding (for Mac users with M-series machine, environment must be created with osx-64 environment on x86_64 architecture due to dependency requirement)   
        b. Create conda environment for prediction

        conda env create -f plm_vpf_embed.yml  
        conda env create -f plm_vpf_predict.yml  

Test installation:
1. Run test bash script

        bash test.sh
2. compare output (test_out/) to the contents of test/test_out_compare/  

Make predictions:  
using the faa_prediction.sh script the embedding and classifier can be run from the command line with the first argument provided being a protein fasta file (e.g. example.faa) and the second argument provided being the name of an output directory (e.g. example_out)

        bash faa_prediction.sh example.faa example_out

Notes:  
-- must be run with osx-64 packages for the embedding procedure. (Relevant if using an ARM64 Apple Silicon chip)  
-- bio-transformers package has a numpy conflict with tensorflow so the faa_prediction.sh script utilizes two separate conda environments.  

Citation:  
Flamholz, Z.N., Biller, S.J. & Kelly, L. Large language models improve annotation of prokaryotic viral proteins. Nat Microbiol (2024). https://doi.org/10.1038/s41564-023-01584-8

[![DOI](https://zenodo.org/badge/619829420.svg)](https://zenodo.org/doi/10.5281/zenodo.10182746)




