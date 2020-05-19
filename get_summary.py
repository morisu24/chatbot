from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter, RegexReplaceCharFilter
from janome.tokenizer import Tokenizer as JanomeTokenizer  # sumyのTokenizerと名前が被るため
from janome.tokenfilter import POSKeepFilter, ExtractAttributeFilter
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer

class GetSummary:
	def __init__(self, text):
		self._text = text

	def get_summary(self):
		# 1行1文となっているため、改行コードで分離
		sentences = [t for t in self._text.split('\n')]
		for i in range(1):
		    print(sentences[i])
		
		# 形態素解析器を作る
		analyzer = Analyzer(
		    [UnicodeNormalizeCharFilter(), RegexReplaceCharFilter(r'[(\)「」、。]', ' ')],  # ()「」、。は全てスペースに置き換える
		    JanomeTokenizer(),
		    [POSKeepFilter(['名詞', '形容詞', '副詞', '動詞']), ExtractAttributeFilter('base_form')]  # 名詞・形容詞・副詞・動詞の原型のみ
		)

		# 抽出された単語をスペースで連結
		# 末尾の'。'は、この後使うtinysegmenterで文として分離させるため。
		corpus = [' '.join(analyzer.analyze(s)) + '。' for s in sentences]
		"""
		for i in range(2):
		    print(corpus[i])
		"""
		# 転職 Advent Calendar 2016 - Qiita 14 日 目 なる 少し ポエム 含む。
		# 今年 11 月 SIer Web サービス 会社 転職 する。


		"""
		from sumy.parsers.plaintext import PlaintextParser
		from sumy.nlp.tokenizers import Tokenizer
		from sumy.summarizers.lex_rank import LexRankSummarizer
		"""

		# 連結したcorpusを再度tinysegmenterでトークナイズさせる
		parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

		# LexRankで要約を2文抽出
		summarizer = LexRankSummarizer()
		summarizer.stop_words = [' ']  # スペースも1単語として認識されるため、ストップワードにすることで除外する

		self.summary = summarizer(document=parser.document, sentences_count=2)

		# 元の文を表示
		for sentence in self.summary:
		    print(sentences[corpus.index(sentence.__str__())])
