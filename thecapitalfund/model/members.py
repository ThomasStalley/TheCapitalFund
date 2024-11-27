from datetime import datetime, timedelta

import pandas as pd

from thecapitalfund.model import api, prices, transactions


def get_single_member_data(member_id: str) -> dict:
    """Create a return a dict of up-to-date holder's data."""
    single_member = api.api_get_request(data_slug=f"member/{member_id}", data_key=member_id)
    return single_member


def get_member_timeline(chosen_member: dict) -> list[float]:
    """Get a list representing amount of the fund owned by member for all days the fund has been open."""
    start_date = datetime(2023, 1, 1).date()
    days = pd.DataFrame(prices.get_asset_data())
    most_recent_api_date = days["DateTime"].to_list()[-1]
    end_date = datetime.strptime(most_recent_api_date, "%Y-%m-%d").date()
    chosen_member_transactions = transactions.get_member_transaction_timeline(chosen_member)
    # use previous transactions to create a timeline of the account balance:
    balance_by_date_dict = {}
    account_balance = 0
    current_date = start_date
    while current_date <= end_date:
        day = current_date.strftime("%d-%m-%y")
        if day in chosen_member_transactions.keys():
            account_balance += chosen_member_transactions[day]
            account_balance = round(account_balance, 5)
        balance_by_date_dict[day] = account_balance
        current_date += timedelta(days=1)
    timeline = list(balance_by_date_dict.values())
    return timeline
