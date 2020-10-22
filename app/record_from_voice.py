import pyaudio
import numpy as np
import wave
import contextlib

class RecordFromVoice:
    FORMAT = pyaudio.paInt16            # 16bits
    CHANNELS = 1                        # モノラル
    RATE = 48000                        # サンプリングレート（入力48khz）
    CONV_RATE = 3                       # サンプリングレートのダウンサンプリング率（1/3の場合は3）

    def __init__(self):
        self.__device_index = 0         # 録音デバイスのインデックス（既定は0番目）
        self.__chunk = 1024             # フレームバッファサイズ（音源から1回読み込むときのデータサイズ）
        self.__max_record_seconds = 10  # 最大録音時間（秒）
        self.__silence_seconds = 1      # 無音検知時間（秒）
        self.__threshold_start = 0.01   # 録音開始の閾値
        self.__threshold_stop = 0.01    # 録音終了の閾値
        # pyaudio インスタンスの作成
        self.__pa = pyaudio.PyAudio()

    def close(self):
        # pyaudio インスタンスの破棄
        self.__pa.terminate()

    # 録音ストリームから音声を読み取る（48khzから1/3の16kHzへ間引く）
    # マイクが16khzに対応していないため、48khzで読み取って、
    # docomo Developer support の音声認識で必要な16kHzへ
    def __read_stream(self, stream):
        # 録音ストリームから音声の読み取り
        samples = stream.read(self.__chunk)
        # 符号あり16ビット整数の一次元配列に変換して1/3（48khz/16bit → 16kHz/16bit）にダウンサンプリングする
        word_array = np.frombuffer(samples, dtype="int16")[::self.CONV_RATE]
        return word_array

    # 録音を行いオーディオフレームを取得する
    def record_to_word_frames(self, start_func=None, end_func=None):
        with contextlib.closing(self.__pa.open(format=self.FORMAT,
                                channels=self.CHANNELS,
                                rate=self.RATE,
                                input=True,
                                input_device_index = self.__device_index,
                                frames_per_buffer=self.__chunk)) as stream:
            word_frames = []
            prev_array = []
            # 録音ストリームの開始
            stream.start_stream()
            while True:
                # 録音ストリームから音声を読み取る
                word_array = self.__read_stream(stream)
                # 16bitの最大値を32768で割り-1～1までに正規化したうえで、閾値を超えていれば録音開始
                if abs(word_array.max() / 32768) > self.__threshold_start:
                    # 録音開始コールバック呼び出し
                    if start_func is not None:
                        start_func()
                    # 開始時の音声をフレームに結合
                    word_frames.extend(word_array)
                    # 1回目をスキップしてサンプリングレート ÷ フレームバッファサイズ × 最大録音時間 繰り返す
                    # 48khzであれば毎秒48000回の標本化となるが、1回の処理でフレームバッファサイズ(1024)を読み取るため、
                    # 1秒間の処理回数はサンプリングレート ÷ フレームバッファサイズ = 約47回
                    # この1秒間の処理回数に、最大録音時間を掛けたものがループ回数となる。
                    stop_count = 0
                    for _ in range(1, int(self.RATE / self.__chunk * self.__max_record_seconds)):
                        # 録音ストリームから音声を読み取る
                        word_array = self.__read_stream(stream)
                        # 読み取った音声をフレームに結合
                        word_frames.extend(word_array)
                        # 16bitの最大値を32768で割り-1～1までに正規化したうえで、閾値を下回っていれば停止と判断
                        if abs(word_array.max() / 32768) < self.__threshold_stop:
                            stop_count += 1
                        else:
                            stop_count = 0
                        # 停止カウンタが無音検知時間を超えたら録音停止
                        # 1秒間の処理回数に、無音検知時間を掛けたものが停止カウンタ上限となる。
                        if stop_count > int(self.RATE / self.__chunk * self.__silence_seconds): 
                            break
                    # 開始前の音声があれば先頭に結合
                    if len(prev_array) != 0:
                        word_frames[0:0] = prev_array
                    # 録音停止コールバック呼び出し
                    if end_func is not None:
                        end_func()
                    break
                # 開始前の音声を保持
                prev_array = word_array
            # 録音ストリームの停止
            stream.stop_stream()
            return word_frames

    # オーディオフレームをWAVEファイルとして出力する
    def word_frames_to_wave_file(self, word_frames, output_path):
        with contextlib.closing(wave.open(output_path, 'wb')) as wf:
            # チャンネル数を設定
            wf.setnchannels(self.CHANNELS)
            # サンプルサイズを設定
            wf.setsampwidth(self.__pa.get_sample_size(self.FORMAT))
            # サンプリングレートを設定（48khz / 3 = 16kHz）
            wf.setframerate(self.RATE / self.CONV_RATE) 
            # オーディオフレームの書き込み
            wf.writeframes(b''.join(word_frames))

    # オーディオフレームの16bit配列を8bitずつ入れ替えてバイナリ文字列とする
    def word_frames_to_word_string(self, word_frames):
        word_array = []
        # 16bit配列の要素を取得
        for word in word_frames:
            # 8bitの配列に変換
            byte_array = np.frombuffer(word, dtype="int8")
            # 8bitずつ入れ替え
            byte_tupple = (byte_array[1], byte_array[0])
            # 16bitに戻して結合
            word_array.append(b''.join(byte_tupple))
        # バイナリ文字列にする
        return b''.join(word_array)
