from flask import Flask
from flask import request as req
import requests as r
from bs4 import BeautifulSoup
import json
app = Flask(__name__)


@app.route("/", methods=["GET"])
def start():
    links = []
    content = []
    html = [r.get("https://www.inklingsnews.com/category/news/").content,
    r.get("https://www.inklingsnews.com/category/b/").content,
    r.get("https://www.inklingsnews.com/category/e/").content]
    for h in range(len(html)):
        soup = BeautifulSoup(html[h], features="html.parser")
        snips = soup.findAll('h2', attrs={'class', 'catprofile categoryheadline'})
        for i in range(len(snips)):
            for a in snips[i].find_all('a', href=True):
                links.append(a['href'])

    for l in range(len(links)):
        html = r.get(links[l]).content
        soup = BeautifulSoup(html, features="html.parser")
        try:
            snip = soup.find('div', attrs={'class', 'pf-content'}).get_text(strip=True).encode('ascii', 'ignore').decode("utf-8")
            content.append(snip)
        except:
            pass
    if req.method == 'GET':
        res = app.response_class(
        response=json.dumps(content),
        status=200,
        mimetype='application/json'
    )
    return res


if __name__ == '__main__':
    app.run()
