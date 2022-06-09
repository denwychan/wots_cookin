from gensim.models import Word2Vec
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd


class Trainer():
    """
    Intiatiate the Trainer class so there is model template
    """
    def __init__(self):
        self.words = None
        self.recipes_vector_list = None
        self.vector_size = 0
        self.min_count = 0

    def set_corpus(self, bag_of_ingredients):
        """
        Trains the Word2Vec model using a bag_of_ingredients for the corpus
        Optional parameters:
        - vector_size = 50 as default
        - min_count = minimum count before an ingredient is considered
        part of corpus. 5 as defalt
        """
        self.model = Word2Vec(bag_of_ingredients
                              ,vector_size=self.vector_size
                              ,min_count=self.min_count)
        #Get the words inside the model
        self.words = self.model.wv.__dict__["index_to_key"]
        print("Recipes corpus set")
        return self

    def get_ingredients_vector(self,ingredients):
        """
        Vectorises a list of ingredients and returns an array of average vectors
        Optional parameters:
        - vector_size = 50 as default
        """
        countFound = 0
        vector_list = []
        # Vectorises each ingredient in a list of ingredients
        for word in ingredients:
            if word in self.words:
                vector = self.model.wv[word]
                vector_list.append(vector)
                countFound+=1
        if countFound > 0:
            # Calculates a list of average vectors
            average_vector = np.true_divide(sum(vector_list), countFound)
        else:
            # Returns default array of zeros based on the number of vectors if
            # ingredients are not inside of corpus
            average_vector = np.zeros(self.vector_size,)
        return average_vector

    #Given a list of recipes, get a list of each matrix:
    def get_recipes_vectors(self, bag_of_ingredients):
        """
        Takes a list of ingredients and vectorises them
        """
        recipes_vector_list = []
        for i in bag_of_ingredients:
            recipes_vector_list.append(self.get_ingredients_vector(i))
        self.recipes_vector_list = recipes_vector_list
        print(f"{len(self.recipes_vector_list)} recipes vectorized")
        return self

    def get_similarity_score(self, ingredients):
        """
        Takes a list of ingredients and returns a numpy array of similar scores
        relative to the recipes' bag of ingredients based on the cosine
        similarity
        """
        # Cosine similarity score list
        cos_sim = []
        # Calculate the cosine similarity of the ingredients compared to each
        # vectorized recipe stored in the model
        for i in range(0,len(self.recipes_vector_list)):
            if sum(self.recipes_vector_list[i]) == 0.0:
                # Ignore recipes where there is no similarity
                cos_sim.append(0)
            else:
                cos_sim.append(
                    np.dot(
                        self.get_ingredients_vector(ingredients)
                        ,self.recipes_vector_list[i])
                    /(norm(
                        self.get_ingredients_vector(ingredients)
                        )
                      *norm(self.recipes_vector_list[i])))
        # Returns the cosine similarity score as an numpy array
        sim_score_list = np.array(cos_sim)
        return sim_score_list

    def get_similar_recipes(self,ingredients, df, nrow=100):
        """
        Takes a list of ingredients, a pandas dataframe, and the number of rows and
        returns the recipes with the highest similarity score
        Optional parameter:
        nrows = number of matches returned. Defaults to 100
        """
        # Get the similarity score
        cos_sim = self.get_similarity_score(ingredients)
        # Get the index for the most similar matches
        index = (-cos_sim).argsort()[:nrow]
        results = []
        # Returns the results in a dataframe
        for i in index:
            results.append(df.iloc[i,:])
        return pd.DataFrame(results)

    def train_model(self,bag_of_ingredients, vector_size=50, min_count=5):
        """
        Trains the Word2Vec model using a bag_of_ingredients for the corpus
        Optional parameters:
        - vector_size = 50 as default
        - min_count = minimum count before an ingredient is considered
        part of corpus. 5 as defalt
        """
        self.vector_size = vector_size
        self.min_count = min_count
        self.set_corpus(bag_of_ingredients)
        self.get_recipes_vectors(bag_of_ingredients)
        print("Model trained!")
        return self
