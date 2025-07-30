import azure.cognitiveservices.speech as speechsdk
from jvcore import TextToSpeech, getConfig

class AzureTextToSpeech(TextToSpeech):
    def __init__(self) -> None:
        self._config = getConfig().get('tts.azure')
        
    def sayAndWait(self, text) -> None:
        speech_config = speechsdk.SpeechConfig(subscription=self._config['accessKey'], region=self._config['region'])
        audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
        speech_config.speech_synthesis_voice_name=self._config['voiceName']
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
