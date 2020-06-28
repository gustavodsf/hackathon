import io
import os

# Imports the Google Cloud client library
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pydub import AudioSegment

class GoogleTools(object):

    def from_speech_to_text(self, audio_path):
        self.split_audio_channel()
        text_ch1 = self.from_channel_to_text('teste_ch1.wav')
        text_ch2 = self.from_channel_to_text('teste_ch2.wav')
        return text_ch1 + text_ch2

    def split_audio_channel(self):
        mp3 = AudioSegment.from_mp3("upload.wav")
        samples = mp3.get_array_of_samples()
        mono_channels = []
        for i in range(mp3.channels):
            samples_for_current_channel = samples[i::mp3.channels]
            try:
                mono_data = samples_for_current_channel.tobytes()
            except AttributeError:
                mono_data = samples_for_current_channel.tostring()
            mono_channels.append(mp3._spawn(mono_data, overrides={"channels": 1, "frame_rate": int(mp3.frame_rate * 1)}))

        mono_channels[0].export("teste_ch1.wav", format="wav")
        mono_channels[1].export("teste_ch2.wav", format="wav")

    def from_channel_to_text(self,file_name):
        # Instantiates a client
        client = speech.SpeechClient()

        # The name of the audio file to transcribe

        # Loads the audio into memory
        with io.open(file_name, 'rb') as audio_file:
            content = audio_file.read()
            audio = types.RecognitionAudio(content=content)

        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=8000,
            language_code='pt-BR',	
            speech_contexts=[speech.types.SpeechContext(
                            phrases=['salto santiago','salto osório','regional sul','ons regional','kv barra','compensando sistema','usina itá','trezentos volts','prado prado','cos tibes','volts tensão',
                                    'vinte três','tudo tudo','passo fundo','mauro cos','compensar sistema','schimanski schimanski','marcelo ons','gerador salto','revertida gerador','três kv',
                                    'dois kv','reduzir trezentos','barra passo','quatrocentos volts','compensou sistema','mauro mauro','itá michel','zero três','sul marcelo','marcelo prado',
                                    'itá compensando','pampa sul','itá gerador', 'barra salto','pro mínimo','sistema itá','esteira cinza','sete sete','oitocentos sessenta','sete dezesseis',
                                    'santiago gerador','elevar três', 'santiago reduzir','tensão salto','três trinta','centro regional','franco salto', 'sul arilton','cos marcão','pablo tibes',
                                    'vazão vertida','duas unidades','cinco oito','sete quinze','oito dezenove','prado michel','michel usina','feito cos','torres ons','três cinquenta',
                                    'schimanski tudo','vinte seis','ons centro','comutação máquina','reverter gerador','gerador cag','reduzir tensão','unidades geradoras','tensão mínima',
                                    'tensão barra','elevar geração','ons nordeste','tensão unidades','gerar máquina','pessoal ambiental','chamar pessoal', 'máquina','problema esteira',
                                    'rompimento esteira','osvaldo elias', 'cos', 'salto','santiago','prado','itá','thibes','sete','gerador','osório','tibes','ons','zero','dois','sul','schimanski',
                                    'sistema','mauro','tensão', 'compensando','volts','kv','usina','barra','cag','vertido','metros','geração','geradoras','ug',
                                    'utlc','sgi','minski','cog','ocorrência', 'defluência','quinhentos','shimanski','hidrologia','disjuntor','usinas','autorização',
                                    'manobras','umburanas','diamei','rompimento','vitti', 'comutações','sobrecorrente','ligação','reservatório','cnos','oeste',
                                    'ug1','vasão','fornecimento','liberação','impedindo','programação','jorge', 'lacerda','santoago','preventiva','equipamentos',
                                    'elétricos','instalados','cogeração','bay','reduza','norte', 'hidrelétrica', 'equipe',
                                    'ons','engie','kav', 'carga', 'um', 'dois', 'cav', 'elevar carga', 'usina'],
                                    )],)

        # Detects speech in the audio file
        response = client.recognize(config, audio)

        aux = ""
        for result in response.results:
            aux = aux + result.alternatives[0].transcript
        return aux
