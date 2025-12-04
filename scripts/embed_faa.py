import argparse
import os
import pickle
import numpy as np
#from protbert_bfd_embed_utils import protbert_bfd_embed
from embed_protbert_bfd import protbert_bfd_embed

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-faa", help="path to protein fasta", required=True)
	parser.add_argument("-out", help="path to directory for script outputs", default='output')
	parser.add_argument("--num_gpus", help="number of GPUs to utilize for embedding, default 0",
					type=int, default=0)
	parser.add_argument("--max_length", help="maximum length of protein to embed, default 5,096 amino acids",
                    type=int, default=5096)
	parser.add_argument("--batch_size", help="batch size for BioTransformers compute_embeddings method",
                    type=int, default=1)
	args = parser.parse_args()

	## set variables
	faa_path = args.faa
	faa_file_name = faa_path.split('.faa')[0].split('/')[-1]
	### check to see faa exists

	## need to make output directory if it does not exist
	out_path = os.getcwd() + '/' + args.out
	if not os.path.isdir(out_path):
		os.mkdir(out_path)

	MAX_LENGTH = args.max_length
	NUM_GPU = args.num_gpus
	BATCH_SIZE = args.batch_size

	embedding = protbert_bfd_embed(faa_path=faa_path, max_length=MAX_LENGTH, num_gpus=NUM_GPU, batch_size=BATCH_SIZE)
	pickle.dump(embedding, open('{0}/{1}_embeddings_dict.pkl' ''.format(out_path, faa_file_name), "wb"))

if __name__ == '__main__':
	main()
