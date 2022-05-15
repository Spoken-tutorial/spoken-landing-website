from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import requests
stop_words = set(stopwords.words('english'))
lemmatizer = WordNetLemmatizer()

def filter_words():

	filtered_sentence = []
	fosses = requests.get('http://127.0.0.1:8001/api/get_fosslist/')
	for fossdata in fosses.json():
		# foss = []
		for keys in fossdata['keywords']:
			word_tokens = word_tokenize(keys)
			for w in word_tokens:
				if w not in stop_words:		
					lemmi = lemmatizer.lemmatize(w)
					adj   = lemmatizer.lemmatize(w, pos ="a")
					if lemmi != adj:
						filtered_sentence.append(adj)
					filtered_sentence.append(lemmi)
				else:
					filtered_sentence.append(w)
	return filtered_sentence

def tfidf():
	string = filter_words()
	# create object
	tfidf = TfidfVectorizer()
	# get tf-df values
	result = tfidf.fit_transform(string)
	# get idf values
	print('\nidf values:')
	for ele1, ele2 in zip(tfidf.get_feature_names(), tfidf.idf_):
		print(ele1, ':', ele2)


