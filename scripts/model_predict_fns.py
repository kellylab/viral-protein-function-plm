from typing import List
from tensorflow import keras
import pandas as pd
import numpy as np
import pickle

def get_faa_identifier(path: str) -> List[str]:
	idents = []
	with(open(path)) as file:
		for line in file:
			line = line.rstrip()
			if line.startswith('>'):
				idents.append(line)
	
	return idents

def format_predictions(prediction_vectors: np.ndarray, classes_path: str, faa_path: str) -> pd.DataFrame:
	classes = pickle.load(open(classes_path, 'rb'))
	faa_identifiers = get_faa_identifier(path=faa_path)
	
	all_proteins = []
	for i in range(len(prediction_vectors)):
		c = classes.classes_[prediction_vectors[i].argmax()]
		score = list(prediction_vectors[i])[prediction_vectors[i].argmax()]
		protein = faa_identifiers[i]
		all_proteins.append((protein, c, score))

	return pd.DataFrame(all_proteins, columns=['protein_id', 'class_phrog', 'phog_model_score'])

def format_model_predict(prediction_vectors: np.ndarray, classes_path: str, faa_path: str) -> pd.DataFrame:
	classes = pickle.load(open(classes_path, 'rb'))
	faa_identifiers = get_faa_identifier(path=faa_path)
	
	return pd.DataFrame(prediction_vectors, columns=classes.classes_, index=faa_identifiers)

def model_predict(model_path: str, embeddings: np.ndarray):
	model = keras.models.load_model(model_path)
	
	return model.predict(embeddings, verbose=0)
