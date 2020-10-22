import sys
import traceback
import datetime
import contextlib
from os.path import join, dirname
from app.settings import Settings
from app.record_from_voice import RecordFromVoice
from app.voice_to_text import VoiceToText
from app.text_to_speech import TextToSpeech
from app.language_analysis import LanguageAnalysis

RETURN_SUCCESS = 0
RETURN_FAILURE = -1

def main():
    try:
        settings = Settings(join(dirname(__file__), '.env'))

        # 音声を録音してバイナリデータ化
        print("音声を録音してバイナリデータ化します。")
        word_string = b''
        with contextlib.closing(RecordFromVoice()) as record_from_voice:
            # 録音デバイスから音声を読み取る
            word_frames = record_from_voice.record_to_word_frames(start_func, end_func)
            # WAVEファイルとして保存
            output_path = f"./input_voice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')}.wav"
            record_from_voice.word_frames_to_wave_file(word_frames, output_path)
            # バイナリ文字列のデータとして取得
            word_string = record_from_voice.word_frames_to_word_string(word_frames)
        print("音声を録音してバイナリデータ化しました。")

        # 録音したデータをもとにテキスト化
        print("録音したデータをテキスト化します。")
        voice_to_text = VoiceToText(settings.voice_to_text_url, settings.apikey)
        # バイナリ文字列のデータをテキスト化
        (text, results) = voice_to_text.word_string_to_text(word_string)
        print(f"解析したテキスト : {text}")
        print(f"解析した結果（形態素解析含む） : {results}")
        print("録音したデータをテキスト化しました。")

        # テキストをもとに音声データ化
        print("テキストを音声化します。")
        text_to_speech = TextToSpeech(settings.text_to_speech_url, settings.apikey)
        # テキストをWAVEフォーマットのバイナリデータ化
        wave_bynary = text_to_speech.text_to_wave_bynary(text)
        # バイナリデータをWAVEファイルとして保存
        output_path = f"./output_voice_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S%f')}.wav"
        text_to_speech.save_wave_file(wave_bynary, output_path)
        # バイナリデータをWAVEとして再生
        text_to_speech.play_wave_bynary(wave_bynary)
        print("テキストを音声化しました。")

        # テキストをもとに固有表現抽出
        print("テキストから固有表現抽出します。")
        language_analysis = LanguageAnalysis(settings.language_analysis_url, settings.apikey)
        # テキストを言語解析して固有表現を抽出
        ne_list = language_analysis.named_entity_recognition(text)
        print(f"固有表現抽出の結果 : {ne_list}")
        print("テキストから固有表現抽出しました。")

        return RETURN_SUCCESS
    except:
        traceback.print_exc()
        return RETURN_FAILURE

def start_func():
    print("録音開始（最大10秒）")

def end_func():
    print("録音終了")

if __name__ == "__main__":
    sys.exit(main())
