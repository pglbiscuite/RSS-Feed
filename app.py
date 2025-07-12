import feedparser
from flask import Flask, render_template, request
# from pyspark.sql.connect.functions import array_insert

app = Flask(__name__)

RSS_FEEDS = {
    'COLORS': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC2Qw1dzXDBAZPwS7zm37g8g',
    # 'Hacker News': 'https://news.ycombinator.com/rss',
    # 'Wall Street Journal': 'https://feeds.a.dj.com/rss/RSSMarketsMain.xml',
    # 'CNBC': 'https://search.cnbc.com/rs/search/combinedcms/view.xml?partnerId=wrss01&id=15839069'
}


@app.route('/')
def index():
    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [
            (source, entry)
            for entry in parsed_feed.entries
            if '/shorts/' not in entry.link
        ]
        articles.extend(entries)

    articles = sorted(articles, key=lambda x: x[1].published_parsed, reverse=True)

    page = request.args.get('page', 1, type=int)
    per_page = 10
    total_articles = len(articles)
    start = (page-1) * per_page
    end = start + per_page
    paginated_articles = articles[start:end]

    for source, entry in paginated_articles:
        if source == "COLORS" and hasattr(entry, "yt_videoid"):
            entry.thumbnail_url = f"https://img.youtube.com/vi/{entry.yt_videoid}/hqdefault.jpg"

    return render_template('index.html', articles=paginated_articles, page=page,
                           total_pages = total_articles // per_page + 1)


@app.route('/search')
def search():
    query = request.args.get('q')

    articles = []
    for source, feed in RSS_FEEDS.items():
        parsed_feed = feedparser.parse(feed)
        entries = [
            (source, entry)
            for entry in parsed_feed.entries
            if '/shorts/' not in entry.link
        ]
        articles.extend(entries)

    results = [article for article in articles if query.lower() in article[1].title.lower()]

    for source, entry in results:
        if source == "COLORS" and hasattr(entry, "yt_videoid"):
            entry.thumbnail_url = f"https://img.youtube.com/vi/{entry.yt_videoid}/hqdefault.jpg"

    return render_template('search_results.html', articles=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
