import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import scipy
import unicodedata

"""
This file provides some helper functions to fill in the
missing pieces of a pipeline
"""

def featureSynth(output):
	"""
	Given an MLDB pipeline that ends with a list of lists, this
	function synthesizes the remaining steps.
	"""

	#first a helper method
	def getDataTypes(data):
		"""
		Given a list of lists infers the type for each colum
		"""
		num_features = len(data[0])
		num_data = len(data)
		thresh = num_data/np.log(num_data)
		
		feature_sets = []
		feature_float_count = {}
		for i in range(0, num_features):
			feature_sets.append(set())
			feature_float_count[i] = 0

		for d in data:
			for i,v in enumerate(d):
				feature_sets[i].add(v)
				try:
					float(v)
					feature_float_count[i] = feature_float_count[i] + 1
				except ValueError:
					pass

		result = []
		for i in range(0, num_features):
			if feature_float_count[i] > thresh:
				result.append("num")
			elif len(feature_sets[i]) > thresh:
				result.append("string")
			else:
				result.append("cat")

		return result

	types = getDataTypes(output)
	feature_list = []

	for i,t in enumerate(types):
		if t == "string":
			vectorizer = TfidfVectorizer(min_df=1,stop_words='english', max_features=50000)
			text = [unicodedata.normalize('NFKD', unicode(d[i],errors='replace')).encode('ascii','ignore') for d in output]
			X = vectorizer.fit_transform(text)
			feature_list.append(X)
		elif t == "cat":
			vectorizer = CountVectorizer(min_df=1)
			text = [unicodedata.normalize('NFKD', unicode(d[i],errors='replace')).encode('ascii','ignore') for d in output]
			X = vectorizer.fit_transform(text)
			feature_list.append(X)
		else:
			vector = []
			for d in output:
				try:
					vector.append(float(d[i]))
				except ValueError:
					vector.append(0)
			
			feature_list.append(scipy.sparse.csr_matrix(vector).T)

	features = scipy.sparse.hstack(feature_list).tocsr()
	return features