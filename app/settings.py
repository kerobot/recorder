import os
import urllib.request
from dotenv import load_dotenv

class Settings:
    def __init__(self, envpath):
        # .env ファイルを明示的に指定して環境変数として読み込む
        self.__dotenv_path = envpath
        load_dotenv(self.__dotenv_path)
        # 環境変数から設定値を取得
        self.__apikey = os.environ.get("APIKEY")
        self.__voice_to_text_url = os.environ.get("VOICE_TO_TEXT_URL")
        self.__text_to_speech_url = os.environ.get("TEXT_TO_SPEECH_URL")
        self.__language_analysis_url = os.environ.get("LANGUAGE_ANALYSIS_URL")

    # docomo Developer support APIキー
    @property
    def apikey(self):
        return self.__apikey

    # 音声認識【Powered by アドバンスト・メディア】URL
    @property
    def voice_to_text_url(self):
        return self.__voice_to_text_url

    # 音声合成【Powered by HOYA】URL
    @property
    def text_to_speech_url(self):
        return self.__text_to_speech_url

    # 言語解析【Powered by goo】URL
    @property
    def language_analysis_url(self):
        return self.__language_analysis_url
