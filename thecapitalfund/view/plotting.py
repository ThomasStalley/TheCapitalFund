import base64
import io

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image, ImageDraw
from plotly.subplots import make_subplots

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


def get_sentiments_fig(sentiments_data: list) -> go.Figure:
    sentiments_df = pd.DataFrame(sentiments_data)
    sentiments_df = pd.DataFrame(sentiments_data)[["DATE", "MSFT", "NVDA", "AAPL", "AMZN", "META", "BTC", "ETH"]].copy()
    sentiments_df["DATE"] = pd.to_datetime(sentiments_df["DATE"])
    # Create evenly spaced x-axis ticks
    first_date = sentiments_df["DATE"].min()
    last_date = sentiments_df["DATE"].max()
    n_ticks = 10
    tickvals = pd.to_datetime(np.linspace(first_date.value, last_date.value, n_ticks)).tolist()
    # create gradient background image.
    gradient_data = _generate_gradient(256, 256, "#008000", "#BC0909", opacity=0.33)
    # Create line plot
    sentiments_fig = px.line()
    assets = ["MSFT", "NVDA", "TSLA", "BTC", "AAPL", "AMZN", "META", "GOOGL", "ETH"]
    for i, asset in enumerate(assets):
        sentiments_fig.add_scatter(
            x=sentiments_df["DATE"],
            y=sentiments_df[asset],
            name=asset,
            line=dict(color=INTEL_PALETTE[i % len(INTEL_PALETTE)]),
            opacity=1.0,
            hovertemplate="%{x|%Y-%m-%d}: %{y:.2f}",
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
        plot_bgcolor="rgba(0,0,0,0)",
        images=[
            dict(
                source=gradient_data,
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="below",
                opacity=1,
            )
        ],
        annotations=[
            dict(
                text="OPTIMISM",
                x=0,
                y=1,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(
                    family="Garamond",
                    size=14,
                    color="rgba(0,128,0,0.2)",
                ),
            ),
            dict(
                text="PESSIMISM",
                x=0,
                y=0,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(
                    family="Garamond",
                    size=14,
                    color="rgba(188,9,9,0.2)",
                ),
            ),
        ],
    )
    return sentiments_fig


def get_fangs_fig(sentiments_data: list) -> go.Figure:
    sentiments_df = pd.DataFrame(sentiments_data)
    fangs_df = sentiments_df[["DATE", "STOCK", "CRYPTO"]].copy()
    fangs_df["DATE"] = pd.to_datetime(fangs_df["DATE"])

    def sentiment_level(val: float) -> str:
        if val >= 0.7:
            return "Extreme Greed"
        elif val >= 0.2:
            return "Greed"
        elif val > -0.2:
            return "Neutral"
        elif val > -0.7:
            return "Fear"
        else:
            return "Extreme Fear"

    fangs_df["STOCK_label"] = fangs_df["STOCK"].apply(sentiment_level)
    fangs_df["CRYPTO_label"] = fangs_df["CRYPTO"].apply(sentiment_level)
    # create evenly spaced x-axis ticks:
    first_date = fangs_df["DATE"].min()
    last_date = fangs_df["DATE"].max()
    n_ticks = 10
    tickvals = pd.to_datetime(np.linspace(first_date.value, last_date.value, n_ticks)).tolist()
    # create gradient background image.
    gradient_data = _generate_gradient(256, 256, "#008000", "#BC0909", opacity=0.33)
    # create the line plot:
    sentiments_fig = px.line()
    colors = [INTEL_PALETTE[-5], INTEL_PALETTE[-1]]
    assets = ["STOCK", "CRYPTO"]
    for i, asset in enumerate(assets):
        sentiments_fig.add_scatter(
            x=sentiments_df["DATE"],
            y=sentiments_df[asset],
            name=asset,
            line=dict(color=colors[i]),
            opacity=1.0,
            hovertemplate="%{x|%Y-%m-%d}: %{y:.2f}",
        )
    sentiments_fig.update_traces(hoverinfo="skip")
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
        plot_bgcolor="rgba(0,0,0,0)",
        images=[
            dict(
                source=gradient_data,
                xref="paper",
                yref="paper",
                x=0,
                y=1,
                sizex=1,
                sizey=1,
                sizing="stretch",
                layer="below",
                opacity=1,
            )
        ],
        annotations=[
            dict(
                text="GREED",
                x=0,
                y=1,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(
                    family="Garamond",
                    size=14,
                    color="rgba(0,128,0,0.2)",
                ),
            ),
            dict(
                text="FEAR",
                x=0,
                y=0,
                xref="paper",
                yref="paper",
                showarrow=False,
                font=dict(
                    family="Garamond",
                    size=14,
                    color="rgba(188,9,9,0.2)",
                ),
            ),
        ],
    )
    return sentiments_fig


def _generate_gradient(width: int, height: int, top_color: str, bottom_color: str, opacity: float) -> str:
    image = Image.new("RGBA", (width, height))
    draw = ImageDraw.Draw(image)

    def hex_to_rgb(hex_color):
        hex_color = hex_color.lstrip("#")
        return tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))

    tc = hex_to_rgb(top_color)
    bc = hex_to_rgb(bottom_color)
    alpha_val = int(opacity * 255)
    for y in range(height):
        ratio = y / height
        r = int(tc[0] * (1 - ratio) + bc[0] * ratio)
        g = int(tc[1] * (1 - ratio) + bc[1] * ratio)
        b = int(tc[2] * (1 - ratio) + bc[2] * ratio)
        draw.line([(0, y), (width, y)], fill=(r, g, b, alpha_val))
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return "data:image/png;base64," + img_str
