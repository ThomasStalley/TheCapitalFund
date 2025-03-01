from thecapitalfund.model import api


def get_news_data() -> dict:
    news_data = api.api_get_request(data_slug="news", data_key="NEWS")
    return news_data


def get_sentiments_data() -> dict:
    fangs_data = api.api_get_request(data_slug="sentiments", data_key="SENTIMENTS")
    return fangs_data
 