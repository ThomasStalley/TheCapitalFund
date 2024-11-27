from thecapitalfund.model import api


def get_transactions_as_tuples() -> list[tuple]:
    """Get a list of transactions, each element as a tuple containing all transaction details."""
    transactions = api.api_get_request(data_slug="transactions", data_key="TRANSACTIONS")
    transaction_tuples = [
        (
            transaction["TRANSACTION_ID"],
            transaction["MEMBER_ID"],
            transaction["DATE"],
            transaction["FUND_AMOUNT"],
            transaction["CURRENCY_AMOUNT"],
        )
        for transaction in transactions
    ]
    return transaction_tuples


def get_transactions_grouped_by_user() -> dict:
    """Create and return dict containing all transaction data, grouped by member_id."""
    transactions = api.api_get_request(data_slug="transactions", data_key="TRANSACTIONS")

    transaction_by_user = {}
    for transaction in transactions:
        member_id = transaction.get("MEMBER_ID")
        c_amount = transaction.get("CURRENCY_AMOUNT")
        if transaction_by_user.get(member_id):
            transaction_by_user.get(member_id).append(c_amount)
        else:
            transaction_by_user[member_id] = [c_amount]
    return transaction_by_user


def get_member_transaction_timeline(chosen_member_id) -> dict:
    """Create and return transaction timeline for chosen member; with k,v being date,amount."""
    all_transactions = get_transactions_as_tuples()

    transactions_by_chosen_user = {}
    for transaction in all_transactions:
        transaction_id, member_id, date, fund_amount, currency_amount = transaction
        if member_id != chosen_member_id:
            continue
        # Check if user has transactions in user_transactions:
        if member_id not in transactions_by_chosen_user.keys():
            transactions_by_chosen_user[member_id] = {date: fund_amount}
        else:
            transaction_on_this_date = transactions_by_chosen_user[member_id].get(date)
            if transaction_on_this_date:
                incoming = fund_amount
                transactions_by_chosen_user[member_id][date] = round(transaction_on_this_date + incoming, 5)
            else:
                transactions_by_chosen_user[member_id][date] = fund_amount
    return transactions_by_chosen_user[chosen_member_id]
