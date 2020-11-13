import spacy

class NamedEntityRecognition:
    def __init__(self, model_path):
        self.__model_path = model_path      # spyCyモデルパス

    # 言語解析APIを用いてテキストから固有表現抽出
    def text_to_ner(self, text):
        nlp = spacy.load(self.__model_path)
        doc = nlp(text)
        ne_list = []
        for ent in doc.ents:
            result = f"[{ent.text}]:{ent.label_}:{ent.start_char}:{ent.end_char} "
            ne_list.append(result)
        return ne_list
