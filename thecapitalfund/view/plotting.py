import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --------------------------------------------------------------------------------------------------------- Performance
PERFORMANCE_PALETTE = ["#000000", "#BC0909", "#C1550D", "#DBAD07"]


def get_total_figure(data) -> go.Figure:
    """Create plot to show fund price over time, or account balance over time when logged in."""
    total_fig = px.line()
    total_fig.add_scatter(x=data["DateTime"], y=data["ACF"], name="", line=dict(color=PERFORMANCE_PALETTE[0]))
    _format_performance_figure(total_fig)
    return total_fig


def get_assets_figure(data) -> go.Figure:
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
        go.Scatter(x=days, y=data["VAN"], name=van_name, line=dict(color=PERFORMANCE_PALETTE[1])), row=1, col=1
    )
    assets_fig.add_trace(
        go.Scatter(x=days, y=data["BTC"], name=btc_name, line=dict(color=PERFORMANCE_PALETTE[2])), row=2, col=1
    )
    assets_fig.add_trace(
        go.Scatter(x=days, y=data["ETH"], name=eth_name, line=dict(color=PERFORMANCE_PALETTE[3])), row=3, col=1
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


def _update_y_axis(y_axis):
    """Formatting all y-axes within a figure."""
    y_axis.tickprefix = "£"
    y_axis.update(matches=None)
    y_axis.showticklabels = True


def _update_axes(axes):
    """Creating a black border around each figure."""
    axes.update(showline=True, linewidth=1, linecolor="black", mirror=True)


# ------------------------------------------------------------------------------------------------------------ Analysis
ANALYSIS_PALETTE = ["#BC0909", "#662400", "#000000", "#3b0042", "#360117", "#400000", "#820505"]


def get_holdings_fig(holdings_data):
    holdings_df = pd.DataFrame(holdings_data)
    holdings_df = holdings_df[holdings_df["PERCENTAGE"] >= 0.1]
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


def get_sectors_fig(sectors_data):
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


def get_countries_fig(countries_data):
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
