from datetime import datetime

from thecapitalfund.model import api


def get_asset_data() -> dict:
    """Create and return a dict of up-to-date asset data."""
    days = api.api_get_request(data_slug="days", data_key="DAYS")
    day_data_dict = {"Timeline": [1] * len(days)}
    for day in days:
        for key, value in day.items():
            if key == "DATE":
                key = key.replace("DATE", "DateTime")
                value = datetime.strptime(value, "%Y%m%d").strftime("%Y-%m-%d")
            if key not in day_data_dict:
                day_data_dict[key] = []
            day_data_dict[key].append(value)
    return day_data_dict


def get_price(asset: str) -> float:
    """Get today's price of chosen asset."""
    data_dict = get_asset_data()
    price = round(data_dict.get(asset)[-1], 2)
    return price


def day_percent_change(asset: str) -> str:
    """Get percentage change in asset price between today and one day prior."""
    data_dict = get_asset_data()
    asset_prices = data_dict.get(asset)
    day_percent_change_tcf = 100 * ((asset_prices[-1] - asset_prices[-2]) / asset_prices[-2])
    day_percent_change_tcf = round(day_percent_change_tcf, 2)
    day_percent_change_tcf = f"+{day_percent_change_tcf}" if day_percent_change_tcf > 0 else day_percent_change_tcf
    return day_percent_change_tcf


def week_percent_change(asset: str) -> str:
    """Get percentage change in asset price between today and seven days prior."""
    data_dict = get_asset_data()
    asset_prices = data_dict.get(asset)
    week_percent_change_tcf = 100 * ((asset_prices[-1] - asset_prices[-8]) / asset_prices[-8])
    week_percent_change_tcf = round(week_percent_change_tcf, 2)
    if week_percent_change_tcf > 0:
        week_percent_change_tcf = f"+{week_percent_change_tcf}"
    return week_percent_change_tcf


def all_time_percent_change(asset: str) -> str:
    """Get percentage change in asset price between today and first day of fund."""
    data_dict = get_asset_data()
    asset_prices = data_dict.get(asset)
    all_time_percent_change_tcf = 100 * ((asset_prices[-1] - asset_prices[0]) / asset_prices[0])
    all_time_percent_change_tcf = round(all_time_percent_change_tcf, 2)
    if all_time_percent_change_tcf > 0:
        all_time_percent_change_tcf = f"+{all_time_percent_change_tcf}"
    return all_time_percent_change_tcf


def today() -> dict:
    """Construct dictionary of data to use in holdings table."""
    today = {
        "tcf_price": get_price("ACF"),
        "van_price": get_price("VAN"),
        "btc_price": get_price("BTC"),
        "eth_price": get_price("ETH"),
        "day_percent_change_tcf": day_percent_change("ACF"),
        "week_percent_change_tcf": week_percent_change("ACF"),
        "all_time_percent_change_tcf": all_time_percent_change("ACF"),
        "day_percent_change_van": day_percent_change("VAN"),
        "week_percent_change_van": week_percent_change("VAN"),
        "all_time_percent_change_van": all_time_percent_change("VAN"),
        "day_percent_change_btc": day_percent_change("BTC"),
        "week_percent_change_btc": week_percent_change("BTC"),
        "all_time_percent_change_btc": all_time_percent_change("BTC"),
        "day_percent_change_eth": day_percent_change("ETH"),
        "week_percent_change_eth": week_percent_change("ETH"),
        "all_time_percent_change_eth": all_time_percent_change("ETH"),
    }
    return today
