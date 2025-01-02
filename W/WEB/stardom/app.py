from flask import Flask, render_template
import feedparser

app = Flask(__name__)

@app.route('/')
def home():
    rss_feed = feedparser.parse('https://www.tmz.com/rss.xml')
    articles = []
    for entry in rss_feed.entries:
        media_url = None
        if 'media_content' in entry and entry.media_content:
            media_url = entry.media_content[0]['url']
        elif 'media_thumbnail' in entry and entry.media_thumbnail:
            media_url = entry.media_thumbnail[0]['url']
        elif 'links' in entry:
            for link in entry.links:
                if 'image' in link.type:
                    media_url = link.href
                    break

        # Print media URL for debugging
        print(f"Title: {entry.title}")
        print(f"Media URL: {media_url}")

        article = {
            'title': entry.title,
            'link': entry.link,
            'summary': entry.summary,
            'media_url': media_url,
        }
        articles.append(article)
    return render_template('index.html', articles=articles)

if __name__ == '__main__':
    app.run(debug=True)
