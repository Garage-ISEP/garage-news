import os
import time
from newscatcherapi import NewsCatcherApiClient
from dotenv import load_dotenv


load_dotenv()

NEWS_CATCHER_API = os.getenv("NEWS_CATCHER")


def get_latest_tech_news(lab: str):
    themes = {
        "IA": "artificial intelligence",
        "Blockchain": "blockchain",
        "Coder": "programming and coding",
        "Meta": "virtual reality",
        "Maker": "electronics and robotics",
        "Cyber": "cyber security",
        "All": ["blockchain", "artificial intelligence", "programming and coding",
                "virtual reality", "cyber security", "electronics and robotics"]
    }

    news_articles = []

    # Get your API key from https://newscatcherapi.com/
    newscatcher = NewsCatcherApiClient(x_api_key=NEWS_CATCHER_API)

    if lab == "All":
        # If "All" is selected, loop through all themes
        for theme in themes["All"]:
            # Query the latest news about the theme
            result = newscatcher.get_search(q=theme, lang="en", page_size=1)
            # Choose the latest news
            latest_news = result['articles'][0]
            print(latest_news)
            news_articles.append(latest_news)
            time.sleep(1.5)
    else:
        # If specific lab is selected, fetch the news for that lab
        theme = themes[lab]
        result = newscatcher.get_search(q=theme, lang="en", page_size=1)
        latest_news = result['articles'][0]
        print(latest_news)
        news_articles.append(latest_news)

    return news_articles
