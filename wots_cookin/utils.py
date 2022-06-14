import numpy as np
from gensim.models import Word2Vec
import pandas as pd
import os

#Define the Word2Vec model to be used
def word2vec_(bag_of_ingredients,vector_size=50,min_count=5):
    return Word2Vec(sentences=bag_of_ingredients,vector_size=vector_size, min_count=min_count)

#Get the words inside the model
def get_model_words(model):
        return model.wv.__dict__["index_to_key"]

#Given the model above, get the average "matrix" for a list of words (recipe):
def getRecipeEmbedding(sentence,bag_of_ingredients):
    countFound = 0
    embeddingList = []
    model = word2vec_(bag_of_ingredients)
    for wordx in sentence:
        if wordx in get_model_words(model):
            vector1 = model.wv[wordx]
            embeddingList.append(vector1)
            countFound+=1
    return np.true_divide(sum(embeddingList), countFound)

#Given a list of recipes, get a list of each matrix:
def recipes_list(bag_of_ingredients):
    recipes_embed_list = []
    for i in bag_of_ingredients:
        if getRecipeEmbedding(i).size == 1:
            recipes_embed_list.append(np.zeros(50,))
        else:
            recipes_embed_list.append(getRecipeEmbedding(i))
    return recipes_embed_list

from numpy import dot
from numpy.linalg import norm

#Given a list of ingredients, get a matrix with the cosine similarity with a list of recipes:
def similar_recipe(ingredients,bag_of_ingredients):
    cos_sim = []
    recipes_embed_list = recipes_list(bag_of_ingredients)
    for i in range(0,len(recipes_embed_list)):
        if sum(recipes_embed_list[i]) == 0.0:
            cos_sim.append(0)
        else:
            cos_sim.append(np.dot(getRecipeEmbedding(ingredients),recipes_embed_list[i])/(norm(getRecipeEmbedding(ingredients))*norm(recipes_embed_list[i])))
    dis_array = np.array(cos_sim)
    return dis_array

#Given a matrix of cosine similarity between ingredients and recipes, search the title of the most similar recipe in a recipes dataframe:
def getListofRecipes(recipes_df,ingredients,bag_of_ingredients,n):
    cos_sim = similar_recipe(ingredients,bag_of_ingredients)
    n_index = (-cos_sim).argsort()[:n]
    titles = []
    for i in n_index:
        titles.append(recipes_df.iloc[i,0:2])
    return titles

def get_path(file_path, abs_path = os.path.abspath(__file__)):
    abs_path = abs_path.split('/')
    new_path = ''
    check = 0

    for dir in abs_path[1:]:
        if dir == 'wots_cookin':
            check = 1
        if check == 0:
            new_path += f'/{dir}'

    new_path += file_path
    return new_path
