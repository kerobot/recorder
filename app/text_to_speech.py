import requests
import wave
import pyaudio
import contextlib
from io import BytesIO

class TextToSpeech:
    def __init__(self, url, api_key):
        self.__device_index = 0             # 再生デバイスのインデックス（既定は0番目）
        self.__chunk = 1024                 # フレームバッファサイズ（音源から1回読み込むときのデータサイズ）
        self.__url = url                    # APIのURL
        self.__api_key = api_key            # APIのキー

    # 音声合成APIを用いてテキストからWAVEバイナリを取得
    def text_to_wave_bynary(self, text):
        url = f"{self.__url}?APIKEY={self.__api_key}"
        params = {
            "text":text,
            "speaker":"hikari",
            "emotion":"happiness",
            "emotion_level":"1",
            "pitch":"100",
            "speed":"100",
            "volume":"100",
            "format":"wav"
        }
        r = requests.post(url, data=params)
        if r.status_code == requests.codes.ok: #pylint: disable=no-member
            data = r.content
            return data
        else:
            raise Exception(r.text)

    # WAVEバイナリからbytes-like objectへ変換してpyaudioで再生
    def play_wave_bynary(self, wave_bynary):
        with BytesIO(wave_bynary) as bs:
            with contextlib.closing(wave.open(bs, 'rb')) as wf:
                p = pyaudio.PyAudio()
                stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
                data = wf.readframes(self.__chunk)
                while data != b'':
                    stream.write(data)
                    data = wf.readframes(self.__chunk)
                stream.close()
                p.terminate()

    # WAVEバイナリをWAVEファイルとして保存
    def save_wave_file(self, wave_bynary, output_path):
        with open(output_path,"wb") as fout:
            fout.write(wave_bynary)
