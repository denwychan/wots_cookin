import base64
import streamlit as st
import pandas as pd
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from pydub import AudioSegment
from wots_cookin.google_api import speech_to_text, config
from google.cloud import speech_v1 as speech
from wots_cookin.data import load_full_stopwords, remove_stopwords_from_list, remove_plurals
from wots_cookin.word2vec_trainer import Trainer
from wots_cookin.shortlist import *
from wots_cookin.display import print_details
from PIL import Image

# Load clean dataframe of recipes
df = pd.read_pickle("/ref_data//enriched_recipes.pkl")
df.drop(columns = ['index'], inplace = True)
print(f'Loading dataframe of {df.shape}')

# Load stopword for preprocessing recording transcript
stopwords = load_full_stopwords()

# Load pretrained model
model = Word2Vec.load("/ref_data//word2vec.model")
print(f'{model} model loaded')

# Main function for running app
def main():
    #set the page image and icon
    st.set_page_config(page_title="Wots Cookin", page_icon="🍳")
    image = Image.open('/ref_data//Wots_Cookin1.png')
    st.image(image,width=600)
    # Create audio record button
    record_button  = Button(label="Record", width=100)
    # Custom javascript to run audio recording on clicking 'record' and 'stop'
    record_button.js_on_event("button_click", CustomJS(code="""
    //Get button from the DOM
    var button = document.getElementsByTagName('button')[0];

    if (button.textContent == "Record") {
        const timeMilliSec = 10000 //Fixed 10sec recording ... change here the value
        navigator.mediaDevices.getUserMedia({ audio: true })
        .then(stream => {
            window.mediaRecorder = new MediaRecorder(stream);
            window.mediaRecorder.start();
            const audioChunks = [];
            window.mediaRecorder.addEventListener("dataavailable", event => {
                audioChunks.push(event.data);
            });
            window.mediaRecorder.addEventListener("stop", () => {
                //convert audioBuffer to wav
                const audioBlob = new Blob(audioChunks, {type:'audio/wav'});
                //create base64 reader
                var reader = new FileReader();
                reader.readAsDataURL(audioBlob);
                reader.onloadend = function() {
                    //read base64
                    var base64data = reader.result;
                    //send data to streamlit
                    document.dispatchEvent(new CustomEvent("GET_AUDIO_BASE64", {detail: base64data}));
                }
            });
            //Automatic stop after a set timeframe
            //setTimeout(() => {
            //window.mediaRecorder.stop();
            //}, timeMilliSec);

        });
        button.textContent = "Stop";
    } else {
        mediaRecorder.stop();
        button.textContent = "Record";
    }
    """))
    # Convert audio transcript from javacript to python
    result = streamlit_bokeh_events(
        record_button,
        events="GET_AUDIO_BASE64",
        key="listen",
        refresh_on_update=False,
        override_height=75,
        debounce_time=0)

    # Create multiselect dietary side-bar checklist
    dietary_requirements = st.sidebar.multiselect(
        'What are your dietary requirements?',
        ['Vegetarian', 'Vegan', 'Gluten free', 'Nut free','No shellfish',
        'No eggs', 'Dairy free', 'No soy' ]
        )

    # Create single select box for choosing minimum number of ingredients
    min_num_ingredients = st.sidebar.selectbox(
        'Minimum number of ingredients', [1,2,3,4,5,6,7,8,9,10])

    # Convert recording to file and send to Google speech-to-text API for
    # transcript processing
    if result:
        if "GET_AUDIO_BASE64" in result:
            st.write("Audio recording completed")
            b64_str_metadata = result.get("GET_AUDIO_BASE64")
            metadata_string = "data:audio/wav;base64,"
            if len(b64_str_metadata)>len(metadata_string):
                # Remove metadata (data:audio/wav;base64,)
                if b64_str_metadata.startswith(metadata_string):
                    b64_str = b64_str_metadata[len(metadata_string):]
                else:
                    b64_str = b64_str_metadata

                decoded = base64.b64decode(b64_str)
                # Save file to audio_files folder locally
                uploaded_file = 'ref_data/test.flac'
                with open(uploaded_file,'wb') as f:
                    f.write(decoded)
                # Convert file to flac and save it again
                flac = AudioSegment.from_file(uploaded_file)
                getaudio = flac.export(uploaded_file, format="flac")
                # Convert audio to text with google speech-to-text API
                with open(uploaded_file, "rb") as audio_file:
                    content = audio_file.read()
                audio = speech.RecognitionAudio(content=content)
                transcript = speech_to_text(config, audio)
                st.write(f'Recording: {transcript}')

                # Filter dietary requirements
                shortlist_df = filter_diet_req(dietary_requirements, df)
                print(f'Returning dataframe of {df.shape} after dietary\
                    requirements filtering')

                #filter recipe list for minimum number of ingredients
                shortlist_df = filter_min_ingredients(min_num_ingredients
                                                      , shortlist_df)
                print(f'Returning dataframe of {df.shape} after minimum number\
                    of ingredients filtering')

                # Preprocess transcript into ingredients list and singularise
                ingredients = transcript.split()
                ingredients = remove_stopwords_from_list(ingredients, stopwords)
                ingredients = remove_plurals(ingredients)
                print(f'Searching {ingredients}...')

                # Vectorise the ingredients list form the transcript
                ing_vector = get_ingredients_vector(model, ingredients)
                print('Ingredients vectorised')

                # Get shortlist recipes from model
                shortlist_df = get_similar_recipes(ing_vector
                                                   , shortlist_df['Vector_List']
                                                   , shortlist_df)
                print(f'Returning dataframe of {shortlist_df.shape}')

                # Create slider to allow the user to select the number of
                # results displayed in the summary table
                results_count = st.slider('Select number of results', 1, 10, 5)

                # Shortlist the top results based on the match score
                top_recipes_df = shortlist_recipes(shortlist_df, ingredients
                                                , shortlist_len=results_count)
                print(f'Returning top results of {top_recipes_df.shape}')

                # Display top results html table
                output_df = top_recipes_df[['Title'
                                         , 'Match'
                                         , 'Ingredients_Available']]
                output_df.rename(columns={"Ingredients_Available": "Ingredients Available"},inplace=True)
                style = output_df.style.hide_index()
                st.write(style.to_html(), unsafe_allow_html=True)


                # Print full version of individual recipes with
                # missing ingredients flagged
                st.title('Recipe Details:')
                print_details(top_recipes_df, ingredients)

if __name__ == '__main__':
    main()
