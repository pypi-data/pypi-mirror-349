import azure.cognitiveservices.speech as speechsdk
from jvcore import SpeechToText, getConfig

class AzureSpeechToText(SpeechToText):
    def __init__(self):
        self._config = getConfig().get('stt.azure')
    
    def get_utterance(self, max_seconds) -> str:
        speech_config = speechsdk.SpeechConfig(subscription=self._config['accessKey'], region=self._config['region'])
        speech_config.speech_recognition_language=self._config['language']

        idn = self._config['_inputDeviceName']
        audio_config = speechsdk.audio.AudioConfig(
            device_name=idn if idn else None, 
            use_default_microphone=False if idn else True)
        speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

        print('?')
        speech_recognition_result = speech_recognizer.recognize_once_async().get()
        print('^')
        
        if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
            return speech_recognition_result.text    
        else:
            print('error on stt: ' + speechsdk.ResultReason(speech_recognition_result.reason).name)
            print(speech_recognition_result)
            return None
        
        
