import streamlit as st
from PIL import Image
import numpy as np
from zipfile import ZipFile

def print_details(df, speech_transcript, index):
    '''
    Function which prints on streamlit a recipes title, list of ingredients and
    instructions
    '''

    index = index[0]

    #extract recipe details from database
    title = df.loc[index, 'Title']
    ingredients = df.loc[index, 'Cleaned_Ingredients']
    instructions = df.loc[index, 'Instructions']
    recipe_image = df.loc[index, 'Image_Name']

    #print title
    st.header(title)

    #Display the picture for that recipe
    zip = ZipFile('raw_data/Food Images.zip', 'r')
    ifile = zip.open(f"Food Images/{recipe_image}.jpg")
    im = Image.open(ifile)
    img = np.array(im)
    st.image(img)

    #Display the ingredients and instructions
    st.subheader('Ingredients:')

    speech_transcript = speech_transcript.lower().split(' ')
    for ingredient in ingredients:
        check_missing_ingredients(ingredient, speech_transcript)

    st.subheader('Instructions:')
    st.write(instructions)


def check_missing_ingredients(ingredient, speech_transcript):
    '''
    Function that checks if ingredient is missing from speech transcript
    '''

    ignore_ingredients = ['salt', 'oil', 'sugar', 'water']
    ingredient = ingredient.lower()
    match = False

    for ignore_ingredient in ignore_ingredients:
        if ignore_ingredient in ingredient:
            match = True
        else:
            for word in speech_transcript:
                if word in ingredient:
                    match = True

    if match == True:
        st.write(ingredient)
    else:
        ingredient = f'{ingredient} 🛑 missing'
        return st.write(ingredient)
