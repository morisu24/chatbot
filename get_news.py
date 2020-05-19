
import feedparser
import json
import pprint
import urllib.request
from readability.readability import Document
#from boilerpipe3.extract import Extractor
import re
from selenium import webdriver
from bs4 import BeautifulSoup
import sys, io




class GetNews:
	#news_url #検索結果url_クラス変数
	def __init__(self, search_str):
		# RSSのスクレイピング
		
		self._search_str = search_str

	def format_text(text):
		text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
		text=re.sub('RT', "", text)
		text=re.sub('お気に入り', "", text)
		text=re.sub('まとめ', "", text)
		text=re.sub(r'[!-~]', "", text)#半角記号,数字,英字
		text=re.sub(r'[︰-＠]', "", text)#全角記号
		text=re.sub('\n', " ", text)#改行文字
		return text


	def search_news(self):
		# URLエンコーディング
		s_quote = urllib.parse.quote(self._search_str)
		#Googleニュース
		url = "https://news.google.com/news/rss/search/section/q/" + s_quote + "/" + s_quote + "?ned=jp&amp;hl=ja&amp;gl=JP"
		#url = "http://www.google.co.jp/search?hl=jp&gl=JP&num=10&q=" + s_quote

		d = feedparser.parse(url)
		news = list()

		for i, entry in enumerate(d.entries, 1):

		    p = entry.published_parsed
		    sortkey = "%04d%02d%02d%02d%02d%02d" % (p.tm_year, p.tm_mon, p.tm_mday, p.tm_hour, p.tm_min, p.tm_sec)

		    tmp = {
		        "no": i,
		        "title": entry.title,
		        "link": entry.link,
		        "published": entry.published,
		        "sortkey": sortkey
		    }

		    news.append(tmp)

		self.news_title = [d.get('title') for d in news]
		self.news_url = [d.get('link') for d in news]

		#HTML テキストを取得 
		url_ = self.news_url[0]
		#ver.1
		
		html = urllib.request.urlopen(url_).read()
		_readable_article = Document(html).summary()
		self.readable_title = Document(html).short_title()
		cleanr = re.compile('<.*?>')
		self.readable_article = re.sub(cleanr, '', _readable_article)
		print(self.readable_article)
		
		#ver.2
		"""
		extractor = Extractor(extractor='ArticleExtractor', url=url)
		self.readable_article = extractor.getText()
		print(extractor.getText())
		"""
		#ver.3
		"""
		# UTF8にエンコード
		sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

		# ブラウザを操作するオブジェクトの生成
		driver = webdriver.Chrome()
		# 指定したURLへの移動
		driver.get(url_)
		# ページのHTMLを取得
		html = driver.page_source
		# ブラウザの終了
		driver.close()

		# 取得したHTMLからBeautifulSoupオブフェクトを生成
		# scriptやstyle及びその他タグの除去
		soup = BeautifulSoup(html, "lxml")
		for s in soup(['script', 'style']):
		    s.decompose()

		readable_article = ' '.join(soup.stripped_strings)
		"""
		
		#print(readable_article)
		#print(readable_title)
