import gensim
import numpy as np
import pandas as pd
from numpy import dot
from numpy.linalg import norm

class Doc2VecTrainer():
    """
    Intiatiate the Trainer class so there is model template
    """
    def __init__(self):
        self.recipes_vector_list = None
        self.vector_size = 0
        self.min_count = 0
        self.epochs = 0

    def set_corpus(self, bag_of_ingredients):
        """
        Trains the Doc2Vec model using a bag_of_ingredients for the corpus
        Optional parameters:
        - vector_size = 50 as default
        - min_count = minimum count before an ingredient is considered
        part of corpus. 5 as defalt
        - epochs = 10 as default
        """
        self.model = gensim.models.doc2vec.Doc2Vec(bag_of_ingredients
                              ,vector_size=self.vector_size
                              ,min_count=self.min_count,epochs=self.epochs)
        print("Recipes corpus set")
        return self

    #Given a list of ingredients, get the representative vector:
    def get_ingredients_vector(self, ingredients):
        """
        Takes a list of ingredients and vectorises them
        """
        infered_vector = self.model.infer_vector(ingredients)
        return infered_vector

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
        for i in range(0,len(self.model.dv)):
            #if sum(self.model.dv[i]) == 0.0:
                # Ignore recipes where there is no similarity
                #cos_sim.append(0)
            if 1==1:
                cos_sim.append(
                    np.dot(
                        self.get_ingredients_vector(ingredients)
                        ,self.model.dv[i])
                    /(norm(
                        self.get_ingredients_vector(ingredients)
                        )
                      *norm(self.model.dv[i])))
        # Returns the cosine similarity score as an numpy array
        sim_score_list = np.array(cos_sim)
        return sim_score_list

    def get_similar_recipes(self,ingredients, df, nrow=100):
        """
        Takes a list of ingredients, a pandas dataframe, and the number of rows
        and returns the recipes with the highest similarity score
        Optional parameter:
        nrows = number of matches returned. Defaults to 100
        """
        # Get the cosine similarity score
        cos_sim = self.get_similarity_score(ingredients)
        # Get the index for the most similar matches
        index = (-cos_sim).argsort()[:nrow]
        results = []
        # Returns the results in a dataframe
        for i in index:
            results.append(df.iloc[i,:])
        return pd.DataFrame(results)

    def train_model(self,bag_of_ingredients, vector_size=50, min_count=5,epochs=10):
        """
        Trains the Word2Vec model using a bag_of_ingredients for the corpus
        Optional parameters:
        - vector_size = 50 as default
        - min_count = minimum count before an ingredient is considered
        part of corpus. 5 as defalt
        """
        self.vector_size = vector_size
        self.min_count = min_count
        self.epochs = epochs
        self.set_corpus(bag_of_ingredients)
        print("Model trained!")
        return self
