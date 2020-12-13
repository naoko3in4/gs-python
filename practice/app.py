import json
import random
import ssl
from urllib.request import urlopen
from random import shuffle
from flask import Flask, render_template
from bs4 import BeautifulSoup

app = Flask(__name__)

print("hello")

ssl._create_default_https_context = ssl._create_unverified_context


@app.route("/")
def index():
    """初期画面を表示します."""
    return render_template("index.html")


@app.route("/api/recommend_article")
def api_recommend_article():
    """はてブのホットエントリーから記事を入手して、ランダムに1件返却します."""
    # # **** ここを実装します（基礎課題） ****
    # # 1. はてブのホットエントリーページのHTMLを取得する
    with urlopen("http://feeds.feedburner.com/hatena/b/hotentry") as res:
        html = res.read().decode("utf-8")
    # # # 2. BeautifulSoupでHTMLを読み込む
    soup = BeautifulSoup(html, "html.parser")
    # # # 3. 記事一覧を取得する, 4. ランダムに1件取得する
    items = soup.select("item")
    random.shuffle(items)
    # shuffle(items)
    item = items[0]
    print(item)
    # # 5. 以下の形式で返却する.
    # {
    #     "content": "記事のタイトル",
    #     "link": "記事のURL"
    # }
    return json.dumps({
        "content": item.find("title").string,
        # "link": item.find("link").string
        "link": item.get("rdf:about")
    })


@app.route("/api/biz_article")
def api_tech_article():
    print("hello biz_article")
    """
        **** ここを実装します（発展課題） ****
        ・自分の好きなサイトをWebスクレイピングして情報をフロントに返却します
        ・お天気APIなども良いかも
        ・関数名は適宜変更してください
    """
    # ビジネスジャーナルの記事をランダムに出す
    with urlopen("http://biz-journal.jp/index.xml") as res:
        html = res.read().decode("utf-8")

    soup = BeautifulSoup(html, "html.parser")
    items = soup.select("item")
    shuffle(items)
    item = items[0]
    print(item)

    return json.dumps({
        "content": item.find("title").string,
        # "description": item.find("description").string,
        "link": item.find("guid").string
    })


if __name__ == "__main__":
    app.run(debug=True, port=5004)
