from flask import Flask, render_template
import feedparser

app = Flask(__name__)

@app.route('/')
def home():
    rss_feed = feedparser.parse('http://feeds.bbci.co.uk/news/world/rss.xml')
    articles = rss_feed.entries
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
