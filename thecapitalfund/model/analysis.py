from thecapitalfund.model import api


def get_holdings_data() -> dict:
    holdings_data = api.api_get_request(data_slug="holdings", data_key="HOLDINGS")
    return holdings_data


def get_countries_data() -> dict:
    countries_data = api.api_get_request(data_slug="countries", data_key="COUNTRIES")
    return countries_data


def get_sectors_data() -> dict:
    sectors_data = api.api_get_request(data_slug="sectors", data_key="SECTORS")
    return sectors_data
