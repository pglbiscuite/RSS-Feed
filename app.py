import feedparser
from flask import Flask, render_template, request
# from pyspark.sql.connect.functions import array_insert

app = Flask(__name__)

RSS_FEEDS = {
    'COLORS': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC2Qw1dzXDBAZPwS7zm37g8g',
    'AI Search': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCIgnGlGkVRhd4qNFcEwLL4A',
    'Sam Witteveen': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC55ODQSvARtgSyc8ThfiepQ',
    'Fireship': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCsBjURrPoezykLs9EqgamOA',
    'MICUTZU OFFICIAL': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCAaqUlKbywt__K4jvlrRdbA',
    'ThePrimeagen': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC8ENHE5xdFSwx71u3fDH5Xw',
    'Tech With Tim': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC4JX40jDee_tINbkjycV4Sg',
    'micul Toma': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCySFpz4yYjG87ZM9rwxgLLw',
    'X Ambassadors': 'https://www.youtube.com/feeds/videos.xml?channel_id=UCBv5tYsc0zm7RCum-umdIBA',
    'Code with Ania Kubów': 'https://www.youtube.com/feeds/videos.xml?channel_id=UC5DNytAJ6_FISueUfzZCVsw',

}

# YouTube RSS Feeds
sources = ["COLORS", "AI Search", "Sam Witteveen", "Fireship", "MICUTZU OFFICIAL", "ThePrimeagen", "Tech With Tim", "micul Toma"
            , "X Ambassadors", "Code with Ania Kubów"]

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
        if source in sources and hasattr(entry, "yt_videoid"):
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
        if source in sources and hasattr(entry, "yt_videoid"):
            entry.thumbnail_url = f"https://img.youtube.com/vi/{entry.yt_videoid}/hqdefault.jpg"

    return render_template('search_results.html', articles=results, query=query)


if __name__ == '__main__':
    app.run(debug=True)
