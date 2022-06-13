import streamlit as st

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

    #print title, ingredients list and instructions on streamlit
    st.header(title)
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

    ignore_ingredients = ['salt', 'oil', 'sugar']
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
