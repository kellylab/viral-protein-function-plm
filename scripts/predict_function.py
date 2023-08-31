import argparse
import os
import pickle
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from model_predict_fns import model_predict, format_model_predict, format_predictions

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-faa", help="path to protein fasta", required=True)
	parser.add_argument("-out", help="path to directory for script outputs", default='output')
	parser.add_argument("--efam_calibration_threshold", help="use model decision thresholds from calibration on EFAM data", action='store_true')
	parser.add_argument("--output_embeddings", help="ouput the protein embeddings vectors as a pickle object", action='store_false')
	parser.add_argument("--output_predictions", help="ouput the protein functional predictions as a csv", action='store_true')
	parser.add_argument("--prediction_heatmap", help="output protein prediction heatmap", action='store_true')
	args = parser.parse_args()
	print(args)

	## set variables
	faa_path = args.faa
	faa_file_name = faa_path.split('.faa')[0].split('/')[-1]
	### check to see faa exists
	out_path = os.getcwd() + '/' + args.out

	MODEL = 'model/model_unknown_80_07092023/'
	CLASSES = 'model/model_unknown_80_07092023_lb.pkl'

	MODEL_PATH = os.getcwd() + '/' + MODEL
	CLASSES_PATH = os.getcwd() + '/' + CLASSES

	## PHROG model calibrated with EFAM as described in paper manuscript
	efam_calibration_thresholds = {
	'DNA, RNA and nucleotide metabolism': 0.24689098,
	'connector': 0.7350025,
	'head and packaging': 0.40578952,
	'integration and excision': 0.4553879,
	'lysis': 0.5299651,
	'moron, auxiliary metabolic gene and host takeover': 0.6360029,
	'other': 0.49765095,
	'tail': 0.44529513,
	'transcription regulation': 0.29414055,
	}



	embedding = pickle.load(open('{0}/{1}_protbert_bfd.pkl' ''.format(out_path, faa_file_name), "rb"))
	print('making predictions')
	preds = model_predict(model_path=MODEL_PATH, embeddings=embedding)
	if args.output_predictions:
		preds_formatted = format_model_predict(prediction_vectors=preds, classes_path=CLASSES_PATH, faa_path=faa_path)
		preds_formatted.to_csv('{0}/{1}_functional_probabilities.csv' ''.format(out_path, faa_file_name))

	if args.prediction_heatmap:
		ax = sns.heatmap(preds)
		plt.savefig('{0}/prediction_heatmap.png' ''.format(out_path), dpi=300)

	if args.efam_calibration_threshold:
		final_preds_formatted = format_predictions(prediction_vectors=preds, classes_path=CLASSES_PATH, faa_path=faa_path, calibration_thresholds=efam_calibration_thresholds)
	else:
		final_preds_formatted = format_predictions(prediction_vectors=preds, classes_path=CLASSES_PATH, faa_path=faa_path)
	
	final_preds_formatted.to_csv('{0}/{1}_function_predictions.csv' ''.format(out_path, faa_file_name), index=False)

	if args.output_embeddings:
		os.remove('{0}/{1}_protbert_bfd.pkl' ''.format(out_path, faa_file_name))

if __name__ == '__main__':
	main()
