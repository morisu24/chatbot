
import sys
import re
import libmstdn
import get_news
import morphological_analysis
import get_summary


#Mastodonホスト
#注意："https://"を記述せず,ホスト名のみ記述すること
MASTODON_HOST = "memphis.ibe.kagoshima-u.ac.jp"

#MastodonAPIアクセストークン
#Mastodonのサイトでアプリの登録を行い，取得したアクセストークンを記述すること.
ACCESS_TOKEN = "2847a7d24f17b304fc252506077aad2f69454f15d1ccdea541334f39497e7535"


def remove_html_tags(content):
  """
  文字列内のHTMLタグを削除

  Args:
    content(str):HTMLを削除する文字列

  Returns:
    str:HTMLを削除された文字列
  """
  return re.sub("<[^>]*>", "", content).strip()

def is_to_me(status, my_id):
  """
  自分へのリプライかどうかを判定

  Args:
    status(dict):トゥート情報を格納したdict
    my_id(int):自分のアカウントID

  Returns:
    bool:Trueであれば自分へのリプライ
  """

  for mention in status["mentions"]:
    if mention["id"] == my_id:
      return True
  return False

def generate_reply(status, my_name):
  """
  リプライを生成

  Args:
    status(dict):
    トゥート情報を格納したdict

  Returns:
    str:生成されたリプライ
  """
  #tweet内容の取り出し
  received_text = remove_html_tags(status["content"])
  received_text = "".join(received_text.split()[1:])
  #tweet内容の形態素解析
  mor_ana = morphological_analysis.GetNoun(received_text)
  #print(mor_ana.get_words())
  received_text = "".join(mor_ana.get_words())
  if received_text == "":
    return "対象のニュースはありません．"
  toot_form = status["account"]["username"]

  #retweetするニュースを取得
  toot = get_news.GetNews(received_text)
  toot.search_news()
  #ニュースの要約
  summ = get_summary.GetSummary(toot.readable_article)
  summ.get_summary()
  return "[要約]" + str(summ.summary) + "\n\n" + "【" + toot.news_title[0] + "】" + toot.news_url[0]


  """
  if "こんにちは" in received_text:
    return toot_form + "さん，こんにちは！"
  elif "こんばんは" in received_text:
    return toot_form + "さん，こんにちは！"
  elif "はじめまして" in received_text:
    return toot_form + "さん，はじめまして！私は" + my_name + "です！"
  else:
    return "ごめんなさい,よくわかりません．"
  """
def main():
  api = libmstdn.MastodonAPI(
      mastodon_host=MASTODON_HOST,
      access_token=ACCESS_TOKEN)

  account_info = api.verify_account()
  my_id = account_info["id"]
  my_name = account_info["username"]
  print("Started bot, name: {}, id: {}".format(my_name, my_id))

  stream = api.get_user_stream()
  for status in stream:
    if is_to_me(status, my_id):
      received_text = remove_html_tags(status["content"])
      toot_id = status["id"]
      toot_from = status["account"]["username"]
      print("received from {}: {}".format(toot_from, received_text))

      reply_text = "@{} {}".format(
          toot_from, generate_reply(status, my_name))
      api.toot(reply_text, toot_id)
      print("post to {}: {}".format(toot_from, reply_text))

  return 0

if __name__ == "__main__":
  sys.exit(main())
