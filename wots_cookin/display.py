import streamlit as st
from PIL import Image
import numpy as np
from zipfile import ZipFile
from wots_cookin.data import remove_plurals

def print_details(df, ingredients):
    '''
    Function which prints on streamlit a recipes title, list of ingredients and
    instructions
    '''
    for i in df.index:
        #extract recipe details from database
        title = df['Title'][i]
        ingredients_list = df['Cleaned_Ingredients'][i]
        instructions = df['Instructions'][i]
        recipe_image = df['Image_Name'][i]

        #print title
        st.header(title)

        #Display the picture for that recipe
        # zip = ZipFile('raw_data/Food Images.zip', 'r')
        # ifile = zip.open(f"Food Images/{recipe_image}.jpg")
        # im = Image.open(ifile)
        # img = np.array(im)
        # st.image(img)


        #Display the ingredients and instructions
        st.subheader('Ingredients:')

        for ingredient in ingredients_list:
            check_missing_ingredients(ingredient, ingredients)

        st.subheader('Instructions:')
        st.write(instructions)


def check_missing_ingredients(ingredient, ingredients):
    '''
    Function that checks if ingredient is missing from speech transcript
    '''

    # Ingredients in this list will not be flagged as missing in the frontend
    # UI
    ignore_ingredients = ['salt', 'oil', 'sugar', 'water']
    ingredient = ingredient.lower()
    sing_ingredient = ' '.join(remove_plurals(ingredient.split()))
    match = False

    for ignore_ingredient in ignore_ingredients:
        if ignore_ingredient in ingredient:
            match = True
        else:
            for word in ingredients:
                if word in sing_ingredient:
                    match = True

    if match == True:
        st.write(ingredient)
    else:
        ingredient = f'{ingredient} 🛑 missing'
        return st.write(ingredient)
