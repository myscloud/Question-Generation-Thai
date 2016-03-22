from sklearn.feature_extraction import DictVectorizer
import preprocess.orchid_corpus as orchid_corpus
import numpy as np

import ranking.linear_regression as regr

orchid = orchid_corpus.orchid_corpus()

class question_ranker():
	def __init__(self, model=None, question_set=None):
		self.vectorizer = None
		if model != None:
			pass
		elif question_set != None:
			self.model = self.train_question(question_set)

	def preprocess_data(self, question_set, has_score=False):
		# get all parameters, score
		article = []
		last_idx = -1
		for question in question_set:
			if question.sentence_no != last_idx:
				article.extend([word for word, pos in question.sentence.pos])
				last_idx = question.sentence_no

		data_info = []
		data_scores = []
		for question in question_set:
			data_info.append(question.get_all_features(article))
			if has_score:
				data_scores.append(question.get_average_eval())
		
		# vectorize
		if self.vectorizer == None:
			self.vectorizer = DictVectorizer(sparse=False)
			data_vector = self.vectorizer.fit_transform(data_info)
		else:
			data_vector = self.vectorizer.transform(data_info)

		return data_vector, np.array(data_scores)


	def train_question(self, question_set):
		data_vector, data_scores = self.preprocess_data(question_set, has_score=True)
		# test_kfold(data_vector, data_scores, 5)
		model = regr.train_model(data_vector, data_scores)
		return model

	def test_kfolds(self, question_set):
		data_vector, data_scores = self.preprocess_data(question_set, has_score=True)
		print(regr.test_kfold(data_vector, data_scores, 5))

	def rank_question(self, question_set):
		data_vector, _ = self.preprocess_data(question_set)
		predicted_scores = regr.predict(self.model, data_vector)

		score_list = [(question_set[i], predicted_scores[i]) for i in range(len(question_set))]
		ranked_scores = sorted(score_list, key=lambda x: x[1], reverse=True)
		ranked_question = [question for question, score in ranked_scores]
		return ranked_question, ranked_scores
