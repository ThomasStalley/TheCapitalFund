from thecapitalfund.model import api


def get_news_data() -> dict:
    news_data = api.api_get_request(data_slug="news", data_key="NEWS")
    return news_data


def get_fangs_data() -> dict:
    fangs_data = api.api_get_request(data_slug="fangs", data_key="FANGS")
    return fangs_data
