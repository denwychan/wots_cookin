import numpy as np
from gensim.models import Word2Vec
import pandas as pd
from numpy.linalg import norm

def get_ingredients_vector(model,ingredients):
    """
    Vectorises a list of ingredients and returns an array of average vectors
    Optional parameters:
    - vector_size = 50 as default
    """
    countFound = 0
    vector_list = []
    # Vectorises each ingredient in a list of ingredients
    for word in ingredients:
        if word in model.wv.__dict__['index_to_key']:
            vector = model.wv[word]
            vector_list.append(vector)
            countFound+=1
    if countFound > 0:
        # Calculates a list of average vectors
        average_vector = np.true_divide(sum(vector_list), countFound)
    else:
        # Returns default array of zeros based on the number of vectors if
        # ingredients are not inside of corpus
        average_vector = np.zeros(model.__dict__['vector_size'],)
    return average_vector


def get_similarity_score(ingredients_vector, recipes_vector_list):
    """
    Takes a list of ingredients and returns a numpy array of similar scores
    relative to the recipes' bag of ingredients based on the cosine
    similarity
    """
    # Cosine similarity score list
    cos_sim = []
    # Calculate the cosine similarity of the ingredients compared to each
    # vectorized recipe stored in the model
    for i in range(0,len(recipes_vector_list)):
        if sum(recipes_vector_list[i]) == 0.0:
            # Ignore recipes where there is no similarity
            cos_sim.append(0)
        else:
            cos_sim.append(
                np.dot(ingredients_vector,recipes_vector_list[i])
                /(norm(ingredients_vector)
                    *norm(recipes_vector_list[i])))
    # Returns the cosine similarity score as an numpy array
    sim_score_list = np.array(cos_sim)
    return sim_score_list

def get_similar_recipes(ingredients_vector, recipes_vector_list, df, nrow=100):
    """
    Takes a list of ingredients, a pandas dataframe, and the number of rows
    and returns the recipes with the highest similarity score
    Optional parameter:
    nrows = number of matches returned. Defaults to 100
    """
    # Get the cosine similarity score
    cos_sim = get_similarity_score(ingredients_vector, recipes_vector_list)
    # Get the index for the most similar matches
    index = (-cos_sim).argsort()[:nrow]
    results = []
    # Returns the results in a dataframe
    for i in index:
        results.append(df.iloc[i,:])
    return pd.DataFrame(results)
