from flask import Flask, render_template
import feedparser

app = Flask(__name__)

@app.route('/')
def home():
    rss_feed = feedparser.parse('https://www.tmz.com/rss.xml')
    articles = []
    for entry in rss_feed.entries:
        article = {
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'media_content': entry.get('media_content', []),
            'media_thumbnail': entry.get('media_thumbnail', []),
        }
        articles.append(article)
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)