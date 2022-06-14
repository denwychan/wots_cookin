import base64
import streamlit as st
import pandas as pd
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from pydub import AudioSegment
from wots_cookin.google_api import speech_to_text, config
from google.cloud import speech_v1 as speech
from wots_cookin.data import load_full_stopwords, remove_stopwords_from_list
from wots_cookin.word2vec_trainer import Trainer
from wots_cookin.shortlist import *
from wots_cookin.display import print_details

#audio record button
record_button  = Button(label="Record", width=100)

#java script to run audio recording

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

# Load clean dataframe of recipes
df = pd.read_pickle("raw_data/enriched_recipes.pkl")
df.drop(columns = ['index'], inplace = True)
print(df.shape)
print(df.head(1))
print(df.tail(1))

# Load stopword for preprocessing recording transcript
stopwords = load_full_stopwords()

# Load pretrained model
model = Word2Vec.load("ref_data/word2vec.model")
print(model)
print(model.wv.__dict__.keys())
print(model.wv.__dict__['index_to_key'][:10])

#code to extract audio results from JS to python
result = streamlit_bokeh_events(
    record_button,
    events="GET_AUDIO_BASE64",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

#dietary side-bar checklist
dietary_requirements = st.sidebar.multiselect(
    'What are your dietary requirements?',
    ['Vegetarian', 'Vegan', 'Gluten free', 'Nut free','No shellfish',
     'No eggs', 'Dairy free', 'No soy' ]
     )

#minimum number of ingredients selection
min_number_ingredients = st.sidebar.selectbox(
    'Minimum number of ingredients', [1,2,3,4,5,6,7,8,9,10])

if result:
    if "GET_AUDIO_BASE64" in result:
        st.write("Audio recording completed")
        b64_str_metadata = result.get("GET_AUDIO_BASE64")
        metadata_string = "data:audio/wav;base64,"
        if len(b64_str_metadata)>len(metadata_string):
            #get rid of metadata (data:audio/wav;base64,)

            if b64_str_metadata.startswith(metadata_string):
                b64_str = b64_str_metadata[len(metadata_string):]
            else:
                b64_str = b64_str_metadata

            decoded = base64.b64decode(b64_str)

            #save it server side
            uploaded_file = 'audio_files/test.flac'
            with open(uploaded_file,'wb') as f:
                f.write(decoded)

            #convert File to flac and save it again
            flac = AudioSegment.from_file(uploaded_file)
            getaudio = flac.export(uploaded_file, format="flac")

            #convert audio to text with google API
            with open(uploaded_file, "rb") as audio_file:
                content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
            transcript = speech_to_text(config, audio)

            st.write(f'Recording: {transcript}')
            print(transcript)

            #Filter dietary requirements
            if len(dietary_requirements) > 0:
                df = df[df[dietary_requirements].max(axis=1) == 0]
                print('Error?')
                print(df.head(5))

            #filter recipe list for minimum number of ingredients
            if min_number_ingredients > 0:
                df['Ingredients_Length'] = df['Cleaned_Ingredients'].map(lambda x: len(x))
                df = df[df['Ingredients_Length']>=min_number_ingredients]
                print('Error?')
                print(df.head(5))

            # Preprocess transcript into ingredients list
            ingredients = transcript.split()
            ingredients = remove_stopwords_from_list(ingredients, stopwords)
            print(ingredients)

            # Vectorise the ingredients list form the transcript
            ing_vector = get_ingredients_vector(model, ingredients)
            print(ing_vector)

            # Get shortlist recipes from model
            print(df.head(5))
            shortlist = get_similar_recipes(ing_vector, df['Vector_List'], df)
            print(shortlist.shape)

            #using search function to find no.1 matching recipe
            top_recipes = shortlist_recipes(df, transcript, df.index)

            #print list of recipes including ingredients (flagging missing ingredients)
            #and instructions
            st.title('Recipe Shortlist Details:')
            for recipe in top_recipes:
                print_details(df, transcript, recipe)

