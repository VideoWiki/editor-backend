
# Create your views here.

from sklearn.feature_extraction.text import CountVectorizer
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import re
from django.http import JsonResponse
from rest_framework.views import APIView


model = SentenceTransformer('distilbert-base-nli-mean-tokens')


class KeywordExtraction(APIView):
	def post(self, request):
		if request.method == 'POST':
			sentences = request.data['sentences']
			srcLang = request.data['srcLang']
			max_keywords = 10
			response_dict = {}

			for key, text in sentences.items():
				new_text = re.sub(r'[^\w\s]', '', text).lower()

				# Candidate Keywords/Keyphrases

				n_gram_range = (1, 1)
				stop_words = "english"

				# Extract candidate words/phrases

				count = CountVectorizer(ngram_range=n_gram_range,
										stop_words=stop_words).fit([new_text])
				candidates = count.get_feature_names()

				# Embeddings

				doc_embedding = model.encode([text])
				candidate_embeddings = model.encode(candidates)

				# Cosine Similarity

				top_n = max_keywords
				distances = cosine_similarity(doc_embedding, candidate_embeddings)
				keywords = [candidates[index] for index in distances.argsort()[0][-top_n:]]
				response_dict[key] = keywords

			return JsonResponse(response_dict)