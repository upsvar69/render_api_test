import feedparser

# List of RSS feeds to check
RSS_FEEDS = {
    "World": "https://feeds.bbci.co.uk/news/world/rss.xml",
    "Asia": "https://feeds.bbci.co.uk/news/world/asia/rss.xml",
    "Top Stories": "https://feeds.bbci.co.uk/news/rss.xml"
}

KEYWORD = "belt and road"
MAX_RESULTS = 5

print("🔗 BBC Articles on Belt and Road Initiative (via RSS)")
print("🧪 Debug Info")

matched_articles = []

for name, url in RSS_FEEDS.items():
    print(f"🌐 Connecting to {name} feed...")
    feed = feedparser.parse(url)

    if feed.bozo:
        print(f"❌ Failed to parse feed: {name}")
        continue

    print(f"✅ Successfully parsed {len(feed.entries)} entries from {name}")

    for entry in feed.entries:
        if KEYWORD.lower() in entry.title.lower() or KEYWORD.lower() in entry.get("summary", "").lower():
            matched_articles.append({
                "title": entry.title,
                "link": entry.link,
                "published": entry.get("published", "No date")
            })
            if len(matched_articles) >= MAX_RESULTS:
                break
    if len(matched_articles) >= MAX_RESULTS:
        break

# Display results
print("\n🔍 Search Results:\n")
if matched_articles:
    for article in matched_articles:
        print(f"📰 {article['title']}")
        print(f"📅 {article['published']}")
        print(f"🔗 {article['link']}")
        print("-" * 50)
else:
    print("❗ No articles found mentioning 'Belt and Road'.")