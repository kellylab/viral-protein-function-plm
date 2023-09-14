# Viral protein function prediction using Protein Language Model
Viral protein high-level function prediction. Categories are defined by the PHROGs database (https://phrogs.lmge.uca.fr/). For more information, please see the preprint assocaited with this project- https://www.researchsquare.com/article/rs-2852098/latest.  

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
Zachary Flamholz, Steven Biller, and Libusha Kelly. Large language models improve annotation of viral proteins, 02 May 2023, PREPRINT (Version 1). https://doi.org/10.21203/rs.3.rs-2852098/v1].
