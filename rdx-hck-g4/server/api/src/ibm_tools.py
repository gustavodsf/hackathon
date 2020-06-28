from ibm_watson import TextToSpeechV1
import json

class IbmTools(object):

    def from_text_to_speech(self, txt):
        text_to_speech = TextToSpeechV1(
            iam_apikey='Vm2QNF3Iu-HBKoxBykJqRFF-ul5OVVuKzAUaQYe4UtMk',
            url='https://stream.watsonplatform.net/text-to-speech/api'
        )

        with open('speech.wav', 'wb') as audio_file:
            audio_file.write(
                text_to_speech.synthesize(
                    txt,
                    voice='pt-BR_IsabelaVoice',
                    accept='audio/wav'        
                ).get_result().content)