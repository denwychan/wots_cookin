import numpy as np
from nltk.stem.porter import PorterStemmer

def shortlist_recipes(df, speech_transcript, index_refs):
    """function that returns shortlist of index references"""

    score_ls = []
    stemmer = PorterStemmer()

    #converting transcript to list and stemming
    speech_transcript = speech_transcript.split(' ')
    speech_transcript = [stemmer.stem(word) for word in speech_transcript]

    # iterate through each recipe to get match score
    for recipe in index_refs:

            # extract bag of words for each recipe and stem
            boi = df.loc[recipe, 'Bag_Of_Ingredients']
            boi = [stemmer.stem(word) for word in boi]

            # calculate number of matching BoI
            positive_boi = [word for word in speech_transcript if word in boi]
            score = len(positive_boi)

            # calculate score relative to total ingredients required
            score = score / len(df.loc[recipe, 'Cleaned_Ingredients'])
            score_ls.append(score)

    # select top 5 matching indices
    output = np.array([index_refs, score_ls]).T
    output = output[output[:,1].argsort()]
    output = np.flip(output[-5:,:1])

    return output
