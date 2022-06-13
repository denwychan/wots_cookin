from google.cloud import speech_v1 as speech
import pandas as pd

def speech_to_text(config, audio):
    """function to convert audio to text and execute print_sentences function"""
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        # The transcript of first alternative is returned
        return result.alternatives[0].transcript

#downloading list of ingredients with count and splitting by popularity for model optimizing
df = pd.read_csv('ref_data/ingredients_list.csv')
top_list = list(df.iloc[0:1000, 1])
mid_list = list(df.iloc[1000:2000, 1])
bottom_list = list(df.iloc[2000:, 1])

#speech configeration settings, boosted for ingredient words
config = speech.RecognitionConfig(language_code = "en-GB",
            sample_rate_hertz = 48000,
            model = 'default',
            speech_contexts = [{
                "phrases": top_list,
                "boost": 12
                }, {
                "phrases": mid_list,
                "boost": 10
                }, {
                "phrases": bottom_list,
                "boost": 8
                }]
            )
