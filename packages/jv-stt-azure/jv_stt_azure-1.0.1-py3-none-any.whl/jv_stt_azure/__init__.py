from jvcore import SpeechToText, Communicator
from .azure_stt import AzureSpeechToText

def getStt() -> SpeechToText:
    return AzureSpeechToText()

def test(comm: Communicator):
    stt = getStt()
    while True:
        utterance = stt.get_utterance(5)
        print(utterance)