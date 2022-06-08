import base64
import streamlit as st
from bokeh.models.widgets import Button
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events
from pydub import AudioSegment
from google.cloud import storage
from google_api import speech_to_text, config
from google.cloud import speech_v1 as speech

#audio record button
stt_button  = Button(label="Record", width=100)

#java script to run audio recording
stt_button.js_on_event("button_click", CustomJS(code="""
const timeMilliSec = 10000 //Fixed 10sec recording ... change here the value
navigator.mediaDevices.getUserMedia({ audio: true })
  .then(stream => {
    const mediaRecorder = new MediaRecorder(stream);
    mediaRecorder.start();
    const audioChunks = [];
    mediaRecorder.addEventListener("dataavailable", event => {
      audioChunks.push(event.data);
    });
    mediaRecorder.addEventListener("stop", () => {
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
    setTimeout(() => {
      mediaRecorder.stop();
    }, timeMilliSec);
  });
  """))

#code to extract audio results from JS to python
result = streamlit_bokeh_events(
    stt_button,
    events="GET_AUDIO_BASE64",
    key="listen",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

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
