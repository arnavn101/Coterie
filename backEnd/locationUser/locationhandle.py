import googlemaps
from datetime import datetime

from hackathon_project_backend.settings import GOOGLE_API_KEY
import fasttext
import fasttext.util
import numpy as np


class HandleCoordinates:
    def __init__(self, google_api_key=GOOGLE_API_KEY):
        self.maps_client = googlemaps.Client(key=google_api_key)

    def get_location_category(self, latitude_loc, longitude_loc):
        place_id = self.maps_client.find_place((latitude_loc, longitude_loc),
                                               input_type='textquery')['candidates'][0]['place_id']
        return self.maps_client.place(place_id)['result']['types']


class FindSimilarityWords:
    def __init__(self):
        # fasttext.util.download_model('en', if_exists='ignore')
        self.this_model = fasttext.load_model('cc.en.300.bin')

    def cos_sim(self, a, b):
        """Takes 2 vectors a, b and returns the cosine similarity according
        to the definition of the dot product
        (https://masongallo.github.io/machine/learning,/python/2016/07/29/cosine-similarity.html)
        """
        dot_product = np.dot(a, b)
        norm_a = np.linalg.norm(a)
        norm_b = np.linalg.norm(b)
        return dot_product / (norm_a * norm_b)

    def compare_word(self, w, words_vectors):
        """
        Compares new word with those in the words vectors dictionary
        """
        vec = self.this_model.get_sentence_vector(w)
        return {w1: self.cos_sim(vec, vec1) for w1, vec1 in words_vectors.items()}

    # input_word_list would be google places results
    # input_word_list would be the users' interests
    def found_most_similar(self, input_user_interests: list, input_word_list: list, threshold_similarity=0.4):
        words_vectors = {w: self.this_model.get_sentence_vector(w) for w in input_word_list}
        dict_word_similarity = [self.compare_word(ind_word, words_vectors) for ind_word in input_user_interests]
        list_to_append = [input_user_interests[it] for it in range(len(dict_word_similarity)) if
                          dict_word_similarity[it][max(dict_word_similarity[it], key=dict_word_similarity[it].get)]
                          >= threshold_similarity]
        return dict_word_similarity
