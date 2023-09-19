from typing import List
from tensorflow import keras
import pandas as pd
import numpy as np
import pickle

def format_predictions(prediction_vectors: np.ndarray, classes_path: str, faa_identifiers: List[str], calibration_thresholds: dict = None) -> pd.DataFrame:
	classes = pickle.load(open(classes_path, 'rb'))
	
	## only return predictions above threshold if calbration_thresholds are provided
	## if no calibration thresholds provided, prediciton is the highest probability
	if calibration_thresholds == None:
		all_proteins = []
		for i in range(len(prediction_vectors)):
			c = classes.classes_[prediction_vectors[i].argmax()]
			score = list(prediction_vectors[i])[prediction_vectors[i].argmax()]
			protein = faa_identifiers[i]
			all_proteins.append((protein, c, score))

	else:
		threshold_vector = []
		# do not include unknown function for thresholding
		for cat in classes.classes_[0:-1]:
			threshold_vector.append(calibration_thresholds[cat])

		all_proteins = []
		for i in range(len(prediction_vectors)):
			thresholded = prediction_vectors[i][0:-1] > threshold_vector
			k = np.where(thresholded)[0]
			if len(k) < 1:
				c = 'unknown'
				score = list(prediction_vectors[i])[-1]
				protein = faa_identifiers[i]
				all_proteins.append((protein, c, score))
			else:
				for j in k:
					c = classes.classes_[j]
					score = list(prediction_vectors[i])[j]
					protein = faa_identifiers[i]
					all_proteins.append((protein, c, score))
	return pd.DataFrame(all_proteins, columns=['protein_id', 'class_phrog', 'phrog_model_score'])

def format_model_predict(prediction_vectors: np.ndarray, classes_path: str, faa_identifiers: List[str]) -> pd.DataFrame:
	classes = pickle.load(open(classes_path, 'rb'))
	return pd.DataFrame(prediction_vectors, columns=classes.classes_, index=faa_identifiers)

def model_predict(model_path: str, embeddings: np.ndarray):
	model = keras.models.load_model(model_path)
	return model.predict(embeddings, verbose=0)
