import requests
import json

class LanguageAnalysis:
    def __init__(self, url, api_key):
        self.__url = url                    # APIのURL
        self.__api_key = api_key            # APIのキー

    # 言語解析APIを用いてテキストから固有表現抽出
    def named_entity_recognition(self, sentence):
        url = f"{self.__url}?APIKEY={self.__api_key}"
        params = {
            "sentence":sentence
        }
        r = requests.post(url, json=params)
        if r.status_code == requests.codes.ok: #pylint: disable=no-member
            json_data = r.json()
            ne_list = json_data['ne_list']
            return ne_list
        else:
            raise Exception(r.text)
