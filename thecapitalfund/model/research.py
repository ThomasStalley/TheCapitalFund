from thecapitalfund.model import api


def get_rdays_data() -> dict:
    rdays_data = api.api_get_request(data_slug="research/rdays", data_key="RDAYS")
    return rdays_data


def get_metrics_data() -> dict:
    metrics_data = api.api_get_request(data_slug="research/metrics", data_key="METRICS")
    return metrics_data
