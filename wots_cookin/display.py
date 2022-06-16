import streamlit as st
from PIL import Image
import numpy as np
from zipfile import ZipFile
from wots_cookin.data import remove_plurals
from wots_cookin.utils import get_path

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
        images_zip = '/ref_data/Food Images.zip'
        file = get_path(images_zip)
        zip = ZipFile(file, 'r')
        if recipe_image == "#NAME?":
            print("No Image")
        else:
            ifile = zip.open(f"Food Images/{recipe_image}.jpg")
            im = Image.open(ifile)
            img = np.array(im)
            st.image(img)

        #Display the ingredients and instructions
        st.subheader('Ingredients:')

        for ingredient in ingredients_list:
            check_missing_ingredients(ingredient, ingredients)

        st.subheader('Instructions:')
        st.write(instructions)

# Ingredients in this list will not be flagged as missing in the frontend
# UI
ignore_ingredients = ['salt', 'oil', 'sugar', 'water', 'black pepper',
                          'butter', 'optional']

# Ingredients which start with one of the words from the below list will
# not be flagged as missing in the frontend UI
ignore_words = ['*', 'an', 'adjusted', 'divided', 'accompaniments:',
                'Accompaniment:', 'or']

def check_missing_ingredients(ingredient, ingredients):
    '''
    Function that checks if ingredient is missing from speech transcript
    '''

    #cleaning cleaned ingredient, changing to lower case and singularised version
    sing_ingredient = ' '.join(remove_plurals(ingredient.lower().split()))

    # cleaned ingredients that start with one of the ignore words will not be
    # flagged
    first_word = ingredient.split()[0].lower()
    if first_word in ignore_words:
        return st.write(ingredient)

    #loop through ignore ingredients, if in ingredients do not flag
    for ignore_ingredient in ignore_ingredients:
        if ignore_ingredient in ingredient.lower():
            return st.write(ingredient)

    #loop through words in transcript, if they match word in
    # singularised clean ingredient list do not flag
    match = False
    for word in ingredients:
        if word in sing_ingredient:
            match = True
    if match == True:
        st.write(ingredient)
    else:
        ingredient = f'{ingredient} 🛑 missing'
        return st.write(ingredient)
