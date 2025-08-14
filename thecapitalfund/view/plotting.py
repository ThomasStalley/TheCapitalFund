import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta

# --------------------------------------------------------------------------------------------------------- Performance
PERFORMANCE_PALETTE = ["#000000", "#BC0909", "#C1550D", "#DBAD07"]


def get_total_figure(data: pd.DataFrame) -> go.Figure:
    """Create plot to show fund price over time, or account balance over time when logged in."""
    total_fig = px.line()
    total_fig.add_scatter(x=data["DateTime"], y=data["ACF"], name="", line=dict(color=PERFORMANCE_PALETTE[0]))
    _format_performance_figure(total_fig)
    return total_fig


def get_assets_figure(data: pd.DataFrame) -> go.Figure:
    """Create plot to show fund asset prices over time."""
    days = data["DateTime"]
    # calculate percentage that each asset contributes to fund price:
    tcf_price_today = data["ACF"][-1]
    van_name = f"VAN [{round(100 * (data['VAN'][-1] * 8 / tcf_price_today), 2)}%]"
    btc_name = f"BTC [{round(100 * (data['BTC'][-1] * 0.0014349 / tcf_price_today), 2)}%]"
    eth_name = f"ETH [{round(100 * (data['ETH'][-1] * 0.0199347 / tcf_price_today), 2)}%]"
    # create and format assets graph:
    assets_fig = make_subplots(rows=3, cols=1, vertical_spacing=0.11)
    assets_fig.add_trace(
        go.Scatter(x=days, y=data["VAN"], name=van_name, line=dict(color=PERFORMANCE_PALETTE[1])),
        row=1,
        col=1,
    )
    assets_fig.add_trace(
        go.Scatter(x=days, y=data["BTC"], name=btc_name, line=dict(color=PERFORMANCE_PALETTE[2])),
        row=2,
        col=1,
    )
    assets_fig.add_trace(
        go.Scatter(x=days, y=data["ETH"], name=eth_name, line=dict(color=PERFORMANCE_PALETTE[3])),
        row=3,
        col=1,
    )
    assets_fig.for_each_yaxis(lambda axis: _update_y_axis(axis))
    assets_fig.for_each_yaxis(lambda axis: _update_axes(axis))
    assets_fig.for_each_xaxis(lambda axis: _update_axes(axis))
    _format_performance_figure(assets_fig)
    return assets_fig


def _format_performance_figure(figure: go.Figure):
    """Update figure layout to achieve desired formatting."""
    figure.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Serif", size=15, color="Black"),
        xaxis_title="",
        yaxis_title="",
        yaxis_tickprefix="£",
        xaxis_showline=True,
        xaxis_linewidth=1,
        xaxis_linecolor="black",
        xaxis_mirror=True,
        yaxis_showline=True,
        yaxis_linewidth=1,
        yaxis_linecolor="black",
        yaxis_mirror=True,
        legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.2),
        hovermode="closest",
        hoverlabel=dict(bgcolor="#BC0909", font_size=16, font_family="Serif", font_color="white"),
    )
    # update hover label template for each trace:
    for ele in figure.data:
        ele.hoverinfo = "none"
        ele.hovertemplate = "%{x|%d %b %Y}: £%{y:.2f}"
        ele.hoverlabel = dict(bgcolor=ele.line.color)


def _update_y_axis(y_axis: go.layout.YAxis):
    """Formatting all y-axes within a figure."""
    y_axis.tickprefix = "£"
    y_axis.update(matches=None)
    y_axis.showticklabels = True


def _update_axes(axes):
    """Creating a black border around each figure."""
    axes.update(showline=True, linewidth=1, linecolor="black", mirror=True)


# ------------------------------------------------------------------------------------------------------------ Analysis
ANALYSIS_PALETTE = ["#BC0909", "#662400", "#000000", "#3b0042", "#360117", "#400000", "#820505"]


def get_holdings_fig(holdings_data: list) -> go.Figure:
    """Create treemap plot to show tcf's asset distribution."""
    holdings_df = pd.DataFrame(holdings_data)
    holdings_df = holdings_df[holdings_df["PERCENTAGE"] >= 0.1].copy()
    holdings_fig = px.treemap(
        holdings_df,
        path=["TICKER"],
        values="PERCENTAGE",
        color_discrete_sequence=ANALYSIS_PALETTE,
        custom_data=["TICKER"],
    )
    holdings_fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:.2f}%",
        hoverinfo="skip",
    )
    holdings_fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Times New Roman", size=14),
        hovermode=False,
    )
    return holdings_fig


def get_sectors_fig(sectors_data: list) -> go.Figure:
    """Create treemap plot to show tcf's sector distribution."""
    sectors_df = pd.DataFrame(sectors_data)
    sectors_fig = px.treemap(
        sectors_df,
        path=["SECTOR"],
        values="PERCENTAGE",
        color_discrete_sequence=ANALYSIS_PALETTE,
        custom_data=["SECTOR"],
    )
    sectors_fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:.2f}%",
        hoverinfo="skip",
    )
    sectors_fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Times New Roman", size=14),
        hovermode=False,
    )
    return sectors_fig


def get_countries_fig(countries_data: list) -> go.Figure:
    """Create treemap plot to show tcf's geographical distribution."""
    countries_df = pd.DataFrame(countries_data)
    countries_fig = px.treemap(
        countries_df,
        path=["COUNTRY"],
        values="PERCENTAGE",
        color_discrete_sequence=ANALYSIS_PALETTE,
        custom_data=["COUNTRY"],
    )
    countries_fig.update_traces(
        texttemplate="<b>%{label}</b><br>%{value:.2f}%",
        hoverinfo="skip",
    )
    countries_fig.update_layout(
        paper_bgcolor="white",
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Times New Roman", size=14),
        hovermode=False,
    )
    return countries_fig


# --------------------------------------------------------------------------------------------------------------- Intel
INTEL_PALETTE = px.colors.sequential.YlOrRd


def _sentiment_level(value: float) -> str:
    if value >= 0.7:
        return "Extreme Optimism"
    elif value >= 0.2:
        return "Optimism"
    elif value > -0.2:
        return "Neutral"
    elif value > -0.7:
        return "Pessimism"
    else:
        return "Extreme Pessimism"


def _fang_level(value: float) -> str:
    if value >= 0.7:
        return "Extreme Greed"
    elif value >= 0.2:
        return "Greed"
    elif value > -0.2:
        return "Neutral"
    elif value > -0.7:
        return "Fear"
    else:
        return "Extreme Fear"


def get_sentiments_fig(sentiments_data: list) -> go.Figure:
    columns = ["DATE", "BTC", "AAPL", "NVDA", "MSFT", "AMZN", "ETH", "META"]
    sentiments_df = pd.DataFrame(sentiments_data)[columns].copy()
    sentiments_df["DATE"] = pd.to_datetime(sentiments_df["DATE"])

    # ✅ Show last 60 days instead of fixed date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    sentiments_df = sentiments_df[(sentiments_df["DATE"] >= start_date) & (sentiments_df["DATE"] <= end_date)]

    assets = columns[1:]

    # create evenly spaced x axis ticks:
    first_date = sentiments_df["DATE"].min()
    last_date = sentiments_df["DATE"].max()
    n_ticks = 10
    tickvals = pd.to_datetime(np.linspace(first_date.value, last_date.value, n_ticks)).tolist()

    # create line plot with sentiment labels for each asset:
    sentiments_fig = px.line()
    for i, asset in enumerate(assets):
        sentiments_fig.add_scatter(
            x=sentiments_df["DATE"],
            y=sentiments_df[asset],
            name=asset,
            text=sentiments_df[asset].apply(_sentiment_level),
            textposition="top center",
            hovertemplate="%{x|%Y-%m-%d}: %{y:.2f} (%{text})",
            line=dict(color=INTEL_PALETTE[(i % len(INTEL_PALETTE)) + 2]),
        )

    sentiments_fig.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Serif", size=15, color="Black"),
        xaxis_title="",
        yaxis_title="",
        xaxis_showline=True,
        xaxis_linewidth=1,
        xaxis_linecolor="black",
        xaxis_mirror=True,
        yaxis_showline=True,
        yaxis_linewidth=1,
        yaxis_linecolor="black",
        yaxis_mirror=True,
        hovermode="closest",
        hoverlabel=dict(font_size=16, font_family="Serif", font_color="white"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            xanchor="center",
            x=0.5,
            y=-0.3,
        ),
        xaxis=dict(
            tickmode="array",
            tickvals=tickvals,
            ticktext=[d.strftime("%d %b") for d in tickvals],
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            range=[-1, 1],
            showticklabels=False,
            ticks="",
            zeroline=False,
            showgrid=False,
        ),
    )
    return sentiments_fig

def get_fangs_fig(sentiments_data: list) -> go.Figure:
    sentiments_df = pd.DataFrame(sentiments_data)
    fangs_df = sentiments_df[["DATE", "STOCK", "CRYPTO"]].copy()
    fangs_df["DATE"] = pd.to_datetime(fangs_df["DATE"])
    end_date = datetime.now()
    start_date = end_date - timedelta(days=60)
    fangs_df = fangs_df[(fangs_df["DATE"] >= start_date) & (fangs_df["DATE"] <= end_date)]
    # assign fear and greed labels:
    fangs_df["STOCK_label"] = fangs_df["STOCK"].apply(_fang_level)
    fangs_df["CRYPTO_label"] = fangs_df["CRYPTO"].apply(_fang_level)
    # create evenly spaced x axis ticks:
    first_date = fangs_df["DATE"].min()
    last_date = fangs_df["DATE"].max()
    n_ticks = 10
    tickvals = pd.to_datetime(np.linspace(first_date.value, last_date.value, n_ticks)).tolist()
    # create the line plot:
    fangs_fig = px.line()
    colors = [INTEL_PALETTE[-5], INTEL_PALETTE[-1]]
    assets = [("STOCK", "STOCK_label"), ("CRYPTO", "CRYPTO_label")]
    for i, (asset, label_col) in enumerate(assets):
        fangs_fig.add_scatter(
            x=fangs_df["DATE"],
            y=fangs_df[asset],
            name=asset,
            text=fangs_df[label_col],
            textposition="top center",
            hovertemplate="%{x|%Y-%m-%d}: %{y:.2f} (%{text})",
            line=dict(color=colors[i]),
        )
    fangs_fig.update_layout(
        template="plotly_white",
        margin=dict(l=0, r=0, t=0, b=0),
        font=dict(family="Serif", size=15, color="Black"),
        xaxis_title="",
        yaxis_title="",
        xaxis_showline=True,
        xaxis_linewidth=1,
        xaxis_linecolor="black",
        xaxis_mirror=True,
        yaxis_showline=True,
        yaxis_linewidth=1,
        yaxis_linecolor="black",
        yaxis_mirror=True,
        hovermode="closest",
        hoverlabel=dict(font_size=16, font_family="Serif", font_color="white"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            xanchor="center",
            x=0.5,
            y=-0.3,
        ),
        xaxis=dict(
            tickmode="array",
            tickvals=tickvals,
            ticktext=[d.strftime("%d %b") for d in tickvals],
            showgrid=False,
            zeroline=False,
        ),
        yaxis=dict(
            range=[-1, 1],
            showticklabels=False,
            ticks="",
            zeroline=False,
            showgrid=False,
        ),
    )
    return fangs_fig


# ------------------------------------------------------------------------------------------------------------ Research
INTEL_PALETTE = px.colors.sequential.YlOrRd


def get_rdays_figure(rdays_data):
    rdays_df = pd.DataFrame(rdays_data)
    rdays_fig = go.Figure()
    rdays_fig.add_trace(
        go.Scatter(
            x=rdays_df["DATE"],
            y=rdays_df["DAILY"],
            mode="lines",
            name="Daily Investment",
            line=dict(color=INTEL_PALETTE[-5]),
        )
    )
    rdays_fig.add_trace(
        go.Scatter(
            x=rdays_df["DATE"],
            y=rdays_df["WEEKLY"],
            mode="lines",
            name="Weekly Investment",
            line=dict(color=INTEL_PALETTE[-3]),
        )
    )
    rdays_fig.add_trace(
        go.Scatter(
            x=rdays_df["DATE"],
            y=rdays_df["MONTHLY"],
            mode="lines",
            name="Monthly Investment",
            line=dict(color=INTEL_PALETTE[-2]),
        )
    )
    rdays_fig.add_trace(
        go.Scatter(
            x=rdays_df["DATE"],
            y=rdays_df["QUARTERLY"],
            mode="lines",
            name="Quarterly Investment",
            line=dict(color=INTEL_PALETTE[-1]),
        )
    )
    rdays_fig.update_layout(
        template="plotly_white",
        margin=dict(l=10, r=10, t=10, b=10),
        font=dict(family="Serif", size=15, color="Black"),
        xaxis_title="",
        yaxis_title="",
        yaxis_tickprefix="£",
        xaxis_showline=True,
        xaxis_linewidth=1,
        xaxis_linecolor="black",
        xaxis_mirror=True,
        yaxis_showline=True,
        yaxis_linewidth=1,
        yaxis_linecolor="black",
        yaxis_mirror=True,
        legend=dict(orientation="h", yanchor="bottom", xanchor="center", x=0.5, y=-0.2),
        hovermode="closest",
        hoverlabel=dict(bgcolor="#BC0909", font_size=16, font_family="Serif", font_color="white"),
    )
    for ele in rdays_fig.data:
        ele.hoverinfo = "none"
        ele.hovertemplate = "%{x|%d %b %Y}: £%{y:.2f}"
        ele.hoverlabel = dict(bgcolor=ele.line.color)
    return rdays_fig
