from gensim.models import Word2Vec
import numpy as np
from numpy import dot
from numpy.linalg import norm
import pandas as pd


class Trainer():
    #Define the class Trainer by the bag_of_ingredients and available_ingredients
    def __init__(self,X,y):
        self.words = None
        self.bag_of_ingredients = X
        self.available_ingredients = y
        self.recipes_embed_list = None


    #Define the Word2Vec model used
    def set_model(self):
        self.model = Word2Vec(self.bag_of_ingredients,vector_size=50,min_count=5)

    #Get the words inside the model
    def get_model_words(self):
        self.words = self.model.wv.__dict__["index_to_key"]

    #Given the model above, get the average "matrix" for a list of words/sentence:
    def getRecipeEmbedding(self,sentence):
        countFound = 0
        embeddingList = []
        for wordx in sentence:
            if wordx in self.words:
                vector1 = self.model.wv[wordx]
                embeddingList.append(vector1)
                countFound+=1
        return np.true_divide(sum(embeddingList), countFound)

    #Given a list of recipes, get a list of each matrix:
    def recipes_list(self):
        recipes_embed_list = []
        for i in self.bag_of_ingredients:
            if self.getRecipeEmbedding(i).size == 1:
                recipes_embed_list.append(np.zeros(50,))
            else:
                recipes_embed_list.append(self.getRecipeEmbedding(i))
        self.recipes_embed_list = recipes_embed_list

    #Given a list of ingredients, get a matrix with the cosine similarity with a list of recipes:
    def similar_recipe(self):
        cos_sim = []
        for i in range(0,len(self.recipes_embed_list)):
            if sum(self.recipes_embed_list[i]) == 0.0:
                cos_sim.append(0)
            else:
                cos_sim.append(np.dot(self.getRecipeEmbedding(self.available_ingredients),self.recipes_embed_list[i])/(norm(self.getRecipeEmbedding(self.available_ingredients))*norm(self.recipes_embed_list[i])))
        dis_array = np.array(cos_sim)
        return dis_array

    #Given a matrix of cosine similaritys between ingredients and recipes, returns a dataframe with the title and ingredients of the most similar recipe in a recipes dataframe:
    def getListofRecipes(self,recipes_df,n):
        cos_sim = self.similar_recipe()
        n_index = (-cos_sim).argsort()[:n]
        titles = []
        for i in n_index:
            titles.append(recipes_df.iloc[i,1:3])
        return pd.DataFrame(titles)
