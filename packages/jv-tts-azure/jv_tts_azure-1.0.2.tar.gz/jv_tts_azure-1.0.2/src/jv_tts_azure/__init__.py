from jvcore import TextToSpeech, Communicator
from .azure_tts import AzureTextToSpeech

def getTts() -> TextToSpeech:
    return AzureTextToSpeech()

def test(comm: Communicator):
    tts = getTts()
    while True:
        text = input('>')
        tts.sayAndWait(text)