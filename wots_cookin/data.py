import pandas as pd
import string
from nltk.tokenize import word_tokenize

def load_data(nrows = None):
    """Method to get data from the recipes csv
    Define 'nrows = integer' for the number of rows returns
    Returns a pandas dataframe with empty or NA values automatically removed
    """
    # Load the raw csv file
    file = "../raw_data/recipes.csv"
    df = pd.read_csv(file, nrows=nrows)
    df_len = df.shape[0]
    # Drop any NAs
    df.dropna(inplace = True)
    # Calculating the length of 'Cleaned_Ingredients' columns to identify any empty ingredients column and then dropping them
    print(f'{df_len - df.shape[0]} rows containing NAs dropped...')
    df_len = df.shape[0]
    df['clean_len'] = [len(i) for i in df["Cleaned_Ingredients"]]
    df.drop(df[df['clean_len']<5].index, axis = 0, inplace= True)
    print(f'{df_len - df.shape[0]} rows containing empty ingredients dropped...')
    # Drop unnecessary columns
    df.drop(columns =['Unnamed: 0', 'clean_len'], inplace = True)
    df.reset_index(drop=True, inplace = True)
    print('Data loaded.')
    return df


def load_full_stopwords():
    """Load the custom stopwords and return a list
    """
    full_stopwords = list(pd.read_csv("../notebooks/full_stopwords.csv")['0'])
    print(f'Returning list of {len(full_stopwords)} stopwords')
    return full_stopwords

def remove_formatting(ingredient_list):
    """
    Function to remove punctuation, numbers and weird formatting
    Takes string and returns string
    """
    punctuation = string.punctuation
    # break string into list of individual items
    ingredient_list = ingredient_list.split("', \'")
    # iterate through each item in list to remove punctuation and non alpha characters
    for i in range(len(ingredient_list)):
        for punc in punctuation:
            ingredient_list[i] = ingredient_list[i].replace(punc, '')
        ingredient_list[i] = ''.join(char for char in ingredient_list[i] if char.isalpha() or char == ' ')
        ingredient_list[i] = ingredient_list[i].strip()
        ingredient_list[i] = ingredient_list[i].replace('  ', ' ')
    return ' '. join(ingredient_list)

def remove_stopwords(ingredient_list):
    """
    Function to remove regular and custom stopwords
    Takes a panda series and returns a list
    """
    # Loading full stopwords list from regular and custom stopwords
    full_stopwords = load_full_stopwords()

    # Removing the stopwords to get bag of ingredients
    print('Removing stopwords...')
    for i in range(0, len(ingredient_list)):
        ingredient_list[i] = ingredient_list[i].lower()
        word_tokens = word_tokenize(ingredient_list[i])
        ingredient_list[i] = [w for w in word_tokens if not w in full_stopwords]
    print("Order's up!")
    return ingredient_list


def load_clean_data(additional = False, nrows = None):
    """
    Function to load data with formatting and stopwords
    Takes optional parameter with number of rows and returns a pandas dataframe
    """
    df = load_data(nrows)
    print('Cleaning formatting...')
    df['Bag_Of_Ingredients'] = df['Cleaned_Ingredients'].map(remove_formatting)
    df['Bag_Of_Ingredients'] = remove_stopwords(df['Bag_Of_Ingredients'])
    if additional == True:
        df = additional_formatting(df)
    print('Returning dataframe with Bag_Of_Ingredients')
    return df

def additional_formatting(df):
    """
    Perform additional formatting to make compatible with basic search function
    NB: this will need to be streamlined into other functions later subject to
    final search model
    """

    def clean_list(ingredient_list):
        """
        Function to convert list in string format to list
        """
        ingredient_list = ingredient_list[2:-2]
        ingredient_list = ingredient_list.split("', '")
        return ingredient_list

    #convert cleaned ingredients string to a list
    df['Cleaned_Ingredients'] = df['Cleaned_Ingredients'].map(clean_list)

    #remove recipes with less than 10 ingredients
    df['length'] = df['Cleaned_Ingredients'].map(lambda x: len(x))
    df = df[df['length']>=10]
    df.reset_index(inplace=True)

    return df
