# docomo Developer support の API を利用した音声認識

## プロジェクト作成

```powershell
> poetry new recorder --name app
> cd .\recorder\
```

## pyproject.toml の編集（Pythonバージョン）

```text
[tool.poetry.dependencies]
python = "^3.6"
```

## プロジェクト設定

```powershell
> pyenv update
> pyenv install 3.6.8
> pyenv local 3.6.8
> pyenv rehash
> python -V
Python 3.6.8
```

## バージョン更新

```powershell
> python -m pip install --upgrade pip
> python -m pip install --upgrade setuptools
```

## ライブラリの追加

```powershell
> poetry add pylint
> poetry add pyaudio
> poetry add numpy==1.19.3
> poetry add python-dotenv
> poetry add requests
> poetry add ginza
```

## ライブラリの一括追加

```powershell
> poetry install
```

## .env の設定

* [docomo Developer support 音声認識](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=speech_recognition&p_name=api_usage_scenario)

* [docomo Developer support 音声合成](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=text_to_speech&p_name=api_usage_scenario)

* [docomo Developer support 言語解析](https://dev.smt.docomo.ne.jp/?p=docs.api.page&api_name=language_analysis&p_name=api_usage_scenario)

## プログラムの実行

```powershell
> poetry run python main.py
```
