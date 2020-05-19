import MeCab

class GetNoun:

  def __init__(self, text):
    self.mecab = MeCab.Tagger("-Ochasen")
    self.mecab.parse("")
    self.sentence = text

  # MeCabを使って形態素解析
  def ma_parse(self, sentence):
    node = self.mecab.parseToNode(sentence)
    while node:
      if node.feature.startswith("名詞"):
        yield node.surface
      node = node.next

  #文字列取得
  def get_words(self):
    words =  [word for word in self.ma_parse(self.sentence)]
    return words


