import requests
import json

class VoiceToText:
    UNKNOWN_ERROR = 'X'
    CODES = {'-1': '認証に失敗しました。',
             '-2': '必須パラメータがありません。',
             '-3': '音声データがありません。',
             '-4': '音声認識サーバー側でエラーが発生しました。',
             '-5': '無効なEngineModeが指定されました。',
             '1': '利用回数制限を超えています。',
             '2': '利用秒数制限を超えています。',
             'o': 'サーバーエラー: 認識結果全体の信頼度が信頼度閾値を下回ったため認識に失敗しました。',
             'b': 'サーバーエラー: 音声認識サーバが混んでいるため認識に失敗しました。',
             'c': 'サーバーエラー: 認識処理中断要求がなされたために認識に失敗しました。',
             UNKNOWN_ERROR: 'サーバーエラー: 不明なエラーが発生しました。'}

    def __init__(self, url, api_key):
        self.__url = url                    # APIのURL
        self.__api_key = api_key            # APIのキー

    # WAVEファイル（PCM(MSB)16khz/16bit）からテキストへ変換
    def wave_file_to_text(self, filepath):
        url = f"{self.__url}?APIKEY={self.__api_key}"
        param = {"a":open(filepath, 'rb'), "v":"on"}
        return self.__to_text(url, param)

    # バイナリ文字列のデータ（PCM(MSB)16khz/16bit）からテキストへ変換
    def word_string_to_text(self, word_string):
        url = f"{self.__url}?APIKEY={self.__api_key}"
        param = {"a":word_string, "v":"on"}
        return self.__to_text(url, param)

    # 音声認識APIを用いて音声からテキストを取得
    def __to_text(self, url, param):
        r = requests.post(url, files=param)
        if r.status_code == requests.codes.ok: #pylint: disable=no-member
            json_data = r.json()
            code = json_data['code']
            if code != '':
                raise Exception(self.CODES.get(code, self.UNKNOWN_ERROR))
            text = json_data['text']
            results = json_data['results']
            return (text, results)
        else:
            raise Exception(r.text)
