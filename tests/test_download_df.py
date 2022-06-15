import numpy as np
import pandas as pd
from wots_cookin.utils import get_path

def test_df_shape():
    """check the shape of the downloaded dataframe"""

    download_path = "/wots_cookin/ref_data/enriched_recipes.pkl"
    file = get_path(download_path)
    df = pd.read_pickle(file)

    assert df.shape == (13487, 17)

def test_df_columns():
    """check the dataframe has the right columns"""

    required_columns = ['Title', 'Ingredients', 'Instructions', 'Image_Name',
       'Cleaned_Ingredients', 'Bag_Of_Ingredients', 'Ingredients_Length',
       'Dairy free', 'No eggs', 'Nut free', 'No shellfish', 'Gluten free',
       'No soy', 'Vegetarian', 'Vegan', 'Vector_List']

    download_path = "/wots_cookin/ref_data/enriched_recipes.pkl"
    file = get_path(download_path)
    df = pd.read_pickle(file)

    columns = df.columns

    for column_name in required_columns:
        assert column_name in columns

def test_df_dtypes():
    """check the data types of key columns"""

    download_path = "/wots_cookin/ref_data/enriched_recipes.pkl"
    file = get_path(download_path)
    df = pd.read_pickle(file)

    #iterate through each row in dataframe to check dtypes of objects
    for row in range(len(df)):

        #check Cleaned_Ingredients is a list and list components are strings
        ci = df.loc[row, 'Cleaned_Ingredients']
        assert type(ci) == list
        for ingredient in ci:
            assert type(ingredient) == str

        #check Bag_Of_Ingredients is a list and list components are strings
        boi = df.loc[row, 'Bag_Of_Ingredients']
        assert type(boi) == list
        for word in boi:
            assert type(word) == str

        #check Vector_List is a list and list components are strings
        vectors = df.loc[row, 'Vector_List']
        assert type(vectors) == np.ndarray
        for vector in vectors:
            assert type(vector) == np.float32 or type(vector) == np.float64

# def test_stopwords_removed():
#     """check that all stopwords have been removed from Bag_Of_Ingredients"""

#     download_path = "/wots_cookin/ref_data/enriched_recipes.pkl"
#     file = get_path(download_path)
#     df = pd.read_pickle(file)

#     boi_series = df.Bag_Of_Ingredients

#     stopwords_path = "/wots_cookin/ref_data/full_stopwords.csv"
#     file = get_path(stopwords_path)
#     full_stopwords = list(pd.read_csv(file)['0'])
#     full_stopwords = remove_plurals(full_stopwords)

#     for boi in boi_series:
#         for word in boi:
#             assert word not in full_stopwords

def test_dietary_tagging():
    """check that dietary tags have been applied and binary values (0 / 1)"""

    download_path = "/wots_cookin/ref_data/enriched_recipes.pkl"
    file = get_path(download_path)
    df = pd.read_pickle(file)

    dietary_tags = ['Dairy free', 'No eggs', 'Nut free', 'No shellfish',
                        'Gluten free', 'No soy', 'Vegetarian', 'Vegan']

    for tag in dietary_tags:
        series_objects = df[tag].value_counts().index
        assert len(series_objects) == 2
        assert 0 in series_objects
        assert 1 in series_objects
