import base64
import streamlit as st
import pandas as pd
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from pydub import AudioSegment
from google.cloud import storage
from google_api import speech_to_text, config
from google.cloud import speech_v1 as speech
from search import shortlist_recipes

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
    ['Vegetarian', 'Vegan', 'Gluten Free', 'Nut Free','No Shellfish',
     'No eggs', 'Dairy free', 'No Soy' ]
     )

#minimum number of ingredients selection
min_number_ingredients = st.sidebar.selectbox('Minimum number of ingredients', [1,2,3,4,5,6,7,8,9,10])

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
            uploaded_file = '../audio_files/test.flac'
            with open(uploaded_file,'wb') as f:
                f.write(decoded)

            #convert File to flac and save it again
            flac = AudioSegment.from_file(uploaded_file)
            getaudio = flac.export(uploaded_file, format="flac")

            #convert audio to text with google API
            with open(uploaded_file, "rb") as audio_file:
                content = audio_file.read()
            audio = speech.RecognitionAudio(content=content)
            output = speech_to_text(config, audio)

            st.write(f'Recording: {output}')

            #loading clean dataframe of recipes
            df = pd.read_pickle("../raw_data/enriched_recipes.pkl")
            df.drop(columns = ['index'], inplace = True)

            #filtering recipe list for dietary requirements
            if len(dietary_requirements) > 0:
                df = df[df[dietary_requirements].max(axis=1) == 0]

            #filter recipe list for minimum number of ingredients
            if min_number_ingredients > 0:
                df['Ingredients_Length'] = df['Cleaned_Ingredients'].map(lambda x: len(x))
                df = df[df['Ingredients_Length']>=min_number_ingredients]

            #using search function to find no.1 matching recipe
            top_recipes = shortlist_recipes(df, output, df.index)
            no_1 = top_recipes[0][0]
            title = df.loc[no_1, 'Title']
            ingredients = df.loc[no_1, 'Cleaned_Ingredients']
            instructions = df.loc[no_1, 'Instructions']

            #printing no.1 recipe (title, ingredients and instructions)
            st.write(f'{title}')
            st.write(f'Ingredients: {ingredients}')
            st.write('Instructions')
            st.write(f'{instructions}')
