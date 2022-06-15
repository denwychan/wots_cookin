from gensim.models import Word2Vec
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd
from wots_cookin.data import load_clean_data
from wots_cookin.utils import get_path

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
        save_path = "/ref_data/word2vec.model"
        file = get_path(save_path)
        self.model.save(file)
        print("Model saved!")
        return self

def model_topickle(vector_size=50
                ,min_count=5):
    # Train Word2Vec model to enrich recipes bank
    df = load_clean_data()
    boi = df['Bag_Of_Ingredients']

    # Train model
    model = Trainer()
    model.train_model(boi, vector_size, min_count)
    df['Vector_List'] = model.recipes_vector_list
    save_path = "/ref_data/enriched_recipes.pkl"
    file = get_path(save_path)
    df.to_pickle(file)
    print('Recipes with vectors created!')
    return df

if __name__ == "__main__":
    model_topickle()
