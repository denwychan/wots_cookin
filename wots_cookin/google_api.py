from google.cloud import speech_v1 as speech

def speech_to_text(config, audio):
    """function to convert audio to text and execute print_sentences function"""
    client = speech.SpeechClient()
    response = client.recognize(config=config, audio=audio)
    for result in response.results:
        # The first alternative is the most likely one for this portion.
        return result.alternatives[0].transcript

config = speech.RecognitionConfig(language_code = "en-GB",
            sample_rate_hertz = 48000,
            model = 'default',
            speech_contexts = [{
                "phrases": ["list to be added with most popular ingredients"],
                "boost": 10
                }, {
                "phrases": ["list to be added with mid popular ingredients"],
                "boost": 6
                }, {
                "phrases": ["list to be added with lowest popular ingredients"],
                "boost": 3
                }]
            )
