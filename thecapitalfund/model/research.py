from thecapitalfund.model import api


def get_models_data() -> dict:
    models_data = api.api_get_request(data_slug="research/models", data_key="MODELS")
    return models_data


def get_metrics_data() -> dict:
    metrics_data = api.api_get_request(data_slug="research/metrics", data_key="METRICS")
    return metrics_data
