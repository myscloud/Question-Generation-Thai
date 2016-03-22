import numpy as np
from sklearn import linear_model
from sklearn.cross_validation import KFold

def train_model(training_data, training_score):
	regr = linear_model.LinearRegression()
	regr.fit(training_data, training_score)
	return regr

def predict(model, testing_data):
	results = model.predict(testing_data)
	return results

def test_kfold(source_data, scores, n_folds):
	kf = KFold(len(source_data), n_folds=n_folds)
	all_testing_results = np.array([])
	all_original_results = np.array([])

	for training_index, testing_index in kf:
		training_data = source_data[training_index]
		training_scores = scores[training_index]
		testing_data = source_data[testing_index]
		testing_scores = scores[testing_index]
		all_original_results = np.append(all_original_results, testing_scores)

		model = train_model(training_data, training_scores)
		testing_results = predict(model, testing_data)
		all_testing_results = np.append(all_testing_results, testing_results)

	sq_err = np.mean((all_testing_results - all_original_results) ** 2)
	return sq_err