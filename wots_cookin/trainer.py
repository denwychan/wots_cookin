from gensim.models import Word2Vec
import numpy as np


#Implement Word2Vec model given a bag of ingredients:
def word2vec_(bag_of_ingredients,vector_size=50,min_count=5):
    return Word2Vec(sentences=bag_of_ingredients,vector_size=vector_size, min_count=min_count)


class Trainer():

    def __init__(self,X,y):
        self.bag_of_ingredients = X
        self.available_ingredients = y


    def set_model(self,X):
        self.model = word2vec_(self.bag_of_ingredients,vector_size=50,min_count=5)

    def get_model_words(self):
        self.words = self.model.wv__dict__["index_to_key"]

    def getRecipeEmbedding(self,sentence):
        countFound = 0
        embeddingList = []
        for wordx in sentence:
            if wordx in self.words:
                vector1 = word2vec.wv[wordx]
                embeddingList.append(vector1)
                countFound+=1
        return np.true_divide(sum(embeddingList), countFound)


    def recipes_list(self,X):
        recipes_embed_list = []
        for i in self.bag_of_ingredients:
            if self.getRecipeEmbedding(i).size == 1:
                recipes_embed_list.append(np.zeros(50,))
            else:
                recipes_embed_list.append(self.getRecipeEmbedding(i))
        return recipes_embed_list
