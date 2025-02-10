from datetime import datetime, timedelta

import dash
import pandas as pd
from dash import Input, Output, State, no_update

from thecapitalfund.controller import login, models
from thecapitalfund.model import members, prices, transactions
from thecapitalfund.view import plotting

prices_data = pd.DataFrame(prices.get_asset_data())


def _get_account_value(user: dict, as_string: bool = True):
    """Get monetary value of the account."""
    fund_owned = user.get("FUND_AMOUNT")
    fund_price_today = prices_data["ACF"].to_list()[-1]
    account_value_today = fund_owned * fund_price_today
    if as_string:
        account_value_today = f"£{account_value_today:.2f}"
    return account_value_today


def _get_account_gain_loss(user: dict) -> str:
    """Get percentage gain/loss of the account (deposited money vs account value)."""
    user_name = user.get("MEMBER_ID")
    grouped_transactions = transactions.get_transactions_grouped_by_user()
    total_value_invested = sum(grouped_transactions.get(user_name))
    account_value_today = _get_account_value(user, as_string=False)
    gain_loss = 100 * ((account_value_today - total_value_invested) / total_value_invested)
    gain_loss_text = f"+{gain_loss:.2f}%" if gain_loss > 0 else f"{gain_loss:.2f}%"
    return gain_loss_text


def _get_member_chart_data(user, chart_data):
    """Show account value vs time, with date range slimmed down to when account value is positive."""
    member_timeline = _get_member_timeline(user.get("MEMBER_ID"))
    # begin x-axis four days prior to member's first deposit:
    begin_timeline_index = 0
    if any(member_balance != 0 for member_balance in member_timeline):
        begin_timeline_index = next(i for i, x in enumerate(member_timeline) if x > 0) - 4
    # update chart data (x=dates, y=balance):
    chart_data["ACF"] = member_timeline[begin_timeline_index:] * chart_data["ACF"][begin_timeline_index:]
    chart_data["DateTime"] = chart_data["DateTime"][begin_timeline_index:]
    return chart_data


def _get_member_timeline(chosen_member: dict) -> list[float]:
    """Get a list representing amount of the fund owned by member for all days the fund has been open."""
    start_date = datetime(2023, 1, 1).date()
    most_recent_api_date = prices_data["DateTime"].to_list()[-1]
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


@dash.callback(
    Output("PerformanceContent", "style"),
    Output("AssetContent", "style"),
    Output("AnalysisContent", "style"),
    Output("AboutContent", "style"),
    Input("NavBarTabs", "active_tab"),
)
def nav_bar_interaction(active_tab):
    """Change main content in response to nav bar tab click."""
    hidden = {"display": "none"}
    visible = {"display": "block"}
    active_tab = active_tab or "performance"
    # delta screen is visible only when performance tab
    contents = ["performance", "asset", "analysis", "about"]
    return [visible if active_tab == content else hidden for content in contents]


@dash.callback(
    Output("ModalLogin", "is_open"),
    Output("NavBarTabs", "active_tab"),
    Input("NavBarTabs", "active_tab"),
    State("ModalLogin", "is_open"),
)
def log_in_button_interaction(active_tab, is_open):
    """When log in button clicked, open modal login and switch tab to performace."""
    if active_tab == "login":
        return not is_open, "performance"
    return no_update, no_update


@dash.callback(
    Output("TotalPlot", "figure"),
    Output("home_session", "data"),
    Output("FooterLoginButton", "n_clicks"),
    Output("FooterHomeButton", "n_clicks"),
    Output("UserIdInput", "value"),
    Output("UserPasswordInput", "value"),
    Output("ModalHeaderText", "children"),
    Output("HeaderTwoValueText", "children"),
    Output("HeaderThrValueText", "children"),
    Output("HeaderTwoValueText", "style"),
    Output("HeaderThrValueText", "style"),
    Output("OpenModalLogin", "label"),
    Output("OpenModalLogin", "label_style"),
    Input("home_session", "data"),
    State("UserIdInput", "value"),
    State("UserPasswordInput", "value"),
    Input("FooterLoginButton", "n_clicks"),
    Input("FooterHomeButton", "n_clicks"),
    Input("ModalHeaderText", "children"),
    Input("HeaderTwoValueText", "children"),
    Input("HeaderThrValueText", "children"),
    Input("HeaderTwoValueText", "style"),
    Input("HeaderThrValueText", "style"),
    Input("OpenModalLogin", "label"),
    Input("OpenModalLogin", "label_style"),
)
def log_in_attempt(
    session,
    name,
    password,
    login_click,
    home_click,
    modal_header_one,
    modal_header_two,
    modal_header_thr,
    modal_header_two_style,
    modal_header_thr_style,
    log_in_button_text,
    log_in_button_style,
):
    """Various updates following an attempted login."""
    logged_in_login_button_style = {
        "color": "#008000",
        "background-color": "#FFF",
        "border": "1px solid #008000",
        "border-radius": "0.2rem",
    }
    logged_out_login_button_style = {
        "color": "#000",
        "background-color": "#FFF",
        "border": "1px solid #00000030",
    }
    visible_header_style = {
        "font-size": "18px",
        "font-family": "eb garamond",
        "margin": "5px 0",
    }
    invisible_header_style = {
        "display": "none",
    }
    chart_data = prices_data.copy()
    app_state = models.AppState(
        session=session or {},
        login_click=login_click,
        home_click=home_click,
        name=name,
        password=password,
        modal_header_one_text=modal_header_one,
        modal_header_two_text=modal_header_two,
        modal_header_thr_text=modal_header_thr,
        modal_header_two_style=modal_header_two_style,
        modal_header_thr_style=modal_header_thr_style,
        log_in_button_text=log_in_button_text,
        log_in_button_style=log_in_button_style,
    )
    # login button clicked:
    if login_click:
        # check if login is successful:
        if successful_login := login.try_login(name, password):
            user = members.get_single_member_data(name)
            chart_data = _get_member_chart_data(user=user, chart_data=chart_data)
            app_state.session = user
            app_state.login_click = 0
            app_state.home_click = 0
            app_state.modal_header_one_text = user.get("NAME")
            app_state.modal_header_two_text = _get_account_value(user=user)
            app_state.modal_header_thr_text = _get_account_gain_loss(user=user)
            app_state.modal_header_two_style = visible_header_style
            app_state.modal_header_thr_style = visible_header_style
            app_state.log_in_button_text = name
            app_state.log_in_button_style = logged_in_login_button_style
        # reset state for failed login:
        if not successful_login:
            app_state.session = {}
            app_state.login_click = 0
            app_state.home_click = 0
            app_state.name = ""
            app_state.password = ""
            app_state.modal_header_one_text = "Log In"
            app_state.modal_header_two_text = "Nope!"
            app_state.modal_header_thr_text = ""
            app_state.modal_header_two_style = visible_header_style
            app_state.modal_header_thr_style = invisible_header_style
            app_state.log_in_button_text = "Log In"
            app_state.log_in_button_style = logged_out_login_button_style
    # reset state for home button click:
    if home_click:
        app_state.session = {}
        app_state.name = ""
        app_state.password = ""
        app_state.login_click = 0
        app_state.home_click = 0
        app_state.modal_header_one_text = "Log In"
        app_state.modal_header_two_text = ""
        app_state.modal_header_thr_text = ""
        app_state.modal_header_two_style = invisible_header_style
        app_state.modal_header_thr_style = invisible_header_style
        app_state.log_in_button_text = "Log In"
        app_state.log_in_button_style = logged_out_login_button_style
    # dump model features to be used in app layout:
    updated_app_features = list(app_state.model_dump().values())
    updated_app_features.insert(0, plotting.get_total_figure(chart_data))
    return updated_app_features
