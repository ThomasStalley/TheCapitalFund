import dash_bootstrap_components as dbc
from dash import dcc, html

from thecapitalfund.model import analysis, intel, prices, research
from thecapitalfund.view import plotting


def format_delta(stock):
    price_increase = stock["today"] > stock["yesterday"]
    arrow = "▲" if price_increase else "▼"
    color = "#008000" if price_increase else "#BC0909"
    span = html.Span(f"{stock['symbol']} {stock['today']} {arrow} ", style={"color": color, "font-family": "dots"})
    return span


def get_layout() -> html.Div:
    # load in required datasets:
    asset_data = prices.get_asset_data()
    holdings_data = analysis.get_holdings_data()
    sectors_data = analysis.get_sectors_data()
    countries_data = analysis.get_countries_data()
    news_data = intel.get_news_data()
    sentiments_data = intel.get_sentiments_data()
    models_data = research.get_models_data()
    metrics_data = research.get_metrics_data()
    today = prices.today()
    # construct tab layouts:
    _performance_tab = dbc.Container(
        id="PerformanceTab",
        fluid=True,
        children=[
            dbc.Row(
                id="PlottingContainer",
                children=[
                    dbc.Row(dbc.Col([html.P("Fund Performance", className="subtitle")], width=10), justify="center"),
                    dbc.Row(
                        dbc.Col(
                            id="TotalPlottingContainer",
                            children=[
                                dcc.Loading(
                                    children=dcc.Graph(
                                        id="TotalPlot",
                                        figure=plotting.get_total_figure(asset_data),
                                        config={"displayModeBar": False},
                                        style={"height": "500px"},
                                    ),
                                    type="circle",
                                    color="#000000",
                                ),
                            ],
                        ),
                    ),
                    dbc.Row(dbc.Col([html.P("Asset Performance", className="subtitle")], width=10), justify="center"),
                    dbc.Row(
                        dbc.Col(
                            id="AssetsPlottingContainer",
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="AssetsPlot",
                                        figure=plotting.get_assets_figure(asset_data),
                                        config={"displayModeBar": False},
                                        style={"height": "350px"},
                                    )
                                ),
                            ],
                        ),
                    ),
                    dbc.Row(dbc.Col(html.P("spacer", style={"font-size": "2px", "opacity": "0"}))),
                ],
            ),
        ],
    )
    _analysis_tab = dbc.Container(
        id="AnalysisTab",
        children=[
            html.P("The Fund", className="subtitle"),
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Asset", id="asset-header-top", className="header"),
                                        html.Th("Price", id="price-header-top", className="header"),
                                        html.Th("Day", id="daily-header-top", className="header"),
                                        html.Th("Week", id="weekly-heade-topr", className="header"),
                                        html.Th("All", id="all-time-header-top", className="header"),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td("TCF-GBP"),
                                            html.Td(f"£{today.get('tcf_price')}"),
                                            html.Td(f"{today.get('day_percent_change_tcf')}%"),
                                            html.Td(f"{today.get('week_percent_change_tcf')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_tcf')}%"),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                        className="equal-width-table",
                        striped=True,
                    ),
                    width=10,
                ),
                justify="center",
            ),
            html.P("The Assets", className="subtitle", style={"transform": "translate(0, 20px)"}),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Asset", id="asset-header", className="header"),
                                        html.Th("Units", id="unit-header", className="header"),
                                        html.Th("Percentage", id="percentage-header", className="header"),
                                        html.Th("Price", id="price-header", className="header"),
                                        html.Th("Day", id="daily-header", className="header"),
                                        html.Th("Week", id="weekly-header", className="header"),
                                        html.Th("All", id="all-time-header", className="header"),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td("VAEIAGA"),
                                            html.Td("8.00"),
                                            html.Td(f"{today.get('van_percentage')}%"),
                                            html.Td(f"£{today.get('van_price')}"),
                                            html.Td(f"{today.get('day_percent_change_van')}%"),
                                            html.Td(f"{today.get('week_percent_change_van')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_van')}%"),
                                        ]
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("BTC-GBP"),
                                            html.Td("0.0014349"),
                                            html.Td(f"{today.get('btc_percentage')}%"),
                                            html.Td(f"£{today.get('btc_price')}"),
                                            html.Td(f"{today.get('day_percent_change_btc')}%"),
                                            html.Td(f"{today.get('week_percent_change_btc')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_btc')}%"),
                                        ]
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("ETH-GBP"),
                                            html.Td("0.0199347"),
                                            html.Td(f"{today.get('eth_percentage')}%"),
                                            html.Td(f"£{today.get('eth_price')}"),
                                            html.Td(f"{today.get('day_percent_change_eth')}%"),
                                            html.Td(f"{today.get('week_percent_change_eth')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_eth')}%"),
                                        ]
                                    ),
                                ]
                            ),
                        ],
                        className="equal-width-table",
                        striped=True,
                    ),
                    width=10,
                ),
                justify="center",
            ),
            html.P("Asset Distribution", className="subtitle", style={"transform": "translate(0, 20px)"}),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dcc.Loading(
                                type="circle",
                                color="#000000",
                                children=dcc.Graph(
                                    id="HoldingsFig",
                                    figure=plotting.get_holdings_fig(holdings_data),
                                    config={"displayModeBar": False},
                                    style={"height": "300px"},
                                ),
                            )
                        ],
                        width=10,
                    )
                ],
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            html.P("Sector Distribution", className="subtitle", style={"transform": "translate(0, 20px)"}),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dcc.Loading(
                                type="circle",
                                color="#000000",
                                children=dcc.Graph(
                                    id="SectorsFig",
                                    figure=plotting.get_sectors_fig(sectors_data),
                                    config={"displayModeBar": False},
                                    style={"height": "300px"},
                                ),
                            )
                        ],
                        width=10,
                    )
                ],
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            html.P("Geographic Distribution", className="subtitle", style={"transform": "translate(0, 20px)"}),
            dbc.Row(
                children=[
                    dbc.Col(
                        children=[
                            dcc.Loading(
                                type="circle",
                                color="#000000",
                                children=dcc.Graph(
                                    id="CountriesFig",
                                    figure=plotting.get_countries_fig(countries_data),
                                    config={"displayModeBar": False},
                                    style={"height": "300px"},
                                ),
                            )
                        ],
                        width=10,
                    )
                ],
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
        ],
    )
    _intel_tab = dbc.Container(
        id="IntelTab",
        children=[
            dbc.Row(dbc.Col(html.P("Asset Sentiments", className="subtitle"))),
            dbc.Row(
                dbc.Col(
                    id="Sentimentsontainer",
                    children=[
                        dcc.Graph(
                            id="SentimentsPlotting",
                            figure=plotting.get_sentiments_fig(sentiments_data),
                            config={"displayModeBar": False},
                            style={"height": "300px"},
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            dbc.Row(dbc.Col(html.P("Market Fear And Greed", className="subtitle"))),
            dbc.Row(
                dbc.Col(
                    id="FangPlottingContainer",
                    children=[
                        dcc.Graph(
                            id="FangsPlotting",
                            figure=plotting.get_fangs_fig(sentiments_data),
                            config={"displayModeBar": False},
                            style={"height": "300px"},
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            dbc.Row(dbc.Col(html.P("News Summaries", className="subtitle"))),
            dbc.Row(
                dbc.Col(
                    children=[
                        html.P(
                            "Today's curated news stories - headlines and summaries produced using GPT-4o mini.",
                        ),
                    ],
                )
            ),
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        [
                            html.Tbody(
                                [
                                    html.Tr(
                                        children=[
                                            html.Td(
                                                children=[
                                                    html.B(
                                                        html.A(
                                                            news_row["TITLE"],
                                                            href=news_row["LINK"],
                                                            style={"color": "#BD0404"},
                                                        ),
                                                    ),
                                                    html.Br(),
                                                    news_row["SUMMARY"],
                                                    html.Br(),
                                                    html.Span(
                                                        f"{news_row['ASSET']} accounts for {news_row['ASSET_PERCENTAGE']:.4f}% of The Capital Fund.",
                                                        style={"color": "grey", "font-style": "italic"},
                                                    ),
                                                ],
                                                style={"border-radius": "0.2rem"},
                                            ),
                                        ],
                                    )
                                    for news_row in news_data
                                ]
                            ),
                        ],
                        striped=True,
                    ),
                    width=10,
                ),
                justify="center",
            ),
        ],
    )
    _research_tab = dbc.Container(
        id="ResearchTab",
        children=[
            dbc.Row(dbc.Col(html.P("Research", className="subtitle"))),
            dbc.Row(
                dbc.Col(
                    children=[
                        html.P(
                            "Here we investigate various investment strategies, focusing specifically on when and how frequently to invest, aiming to maximize returns per pound invested."
                        ),
                        html.P(
                            "We establish three simple baseline methods that involve regular deposits — daily, weekly, and monthly — and then calculate the normalized returns for each."
                        ),
                        html.P(
                            "Additionally, we implement five machine learning techniques. For these methods, we invest today if a model predicts that the fund's price will increase tomorrow. "
                            "Models are trained using fund asset prices from 2020 to 2022, with investment simulation and model evaluation using price data from 1st Jan 2023 onward."
                        ),
                        html.P(
                            "Given the project's objective, we aim to maximize precision (correctly predicting price increases) so each deposit precedes an actual price increase."
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            dbc.Row(dbc.Col(html.P("Investing Methods", className="subtitle"))),
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Investment Method", className="header"),
                                        html.Th("Pounds Invested", className="header"),
                                        html.Th("Investments Made", className="header"),
                                        html.Th("Return Per Pound Invested", className="header"),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Th(method["model"], className="normal"),
                                            html.Th(f'£{method["invested"]}', className="normal"),
                                            html.Th(method["n_investments"], className="normal"),
                                            html.Th(f'£{method["rpp"]}', className="normal"),
                                        ]
                                    )
                                    for method in metrics_data
                                ]
                            ),
                        ],
                        className="equal-width-table",
                        striped=True,
                    ),
                    width=10,
                ),
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            dbc.Row(dbc.Col(html.P("Model Metrics", className="subtitle"))),
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Model", className="header"),
                                        html.Th("Precision", className="header"),
                                        html.Th("Recall", className="header"),
                                        html.Th("F1", className="header"),
                                    ]
                                )
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Th(model["model"], className="normal"),
                                            html.Th(model["precision"], className="normal"),
                                            html.Th(model["recall"], className="normal"),
                                            html.Th(model["f1"], className="normal"),
                                        ]
                                    )
                                    for model in models_data
                                ]
                            ),
                        ],
                        className="equal-width-table",
                        striped=True,
                    ),
                    width=10,
                ),
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
        ],
    )
    _about_tab = dbc.Container(
        id="AboutTab",
        children=[
            html.P("The Project", className="subtitle"),
            dbc.Row(
                dbc.Col(
                    children=[
                        html.P(
                            "This is a personal programming project, the goal being to create a production level, investment fund platform."
                        ),
                        html.P("The app is updated daily, with real world financial data, sourced from my own api."),
                        html.P(
                            [
                                "See the source code in github: ",
                                html.A(
                                    "github.com/thomasstalley/thecapitalfund",
                                    href="https://github.com/thomasstalley/thecapitalfund",
                                    target="_blank",
                                    style={"color": "#000000"},
                                ),
                                ".",
                            ]
                        ),
                        html.P(
                            [
                                "Built with dash, by plotly: ",
                                html.A(
                                    "dash.plotly.com",
                                    href="https://dash.plotly.com/",
                                    target="_blank",
                                    style={"color": "#000000"},
                                ),
                                ".",
                            ],
                        ),
                    ],
                    width=10,
                ),
                className="ebg middle",
                justify="center",
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            html.P("Deployment", className="subtitle", style={"transform": "translate(0, 10px)"}),
            dbc.Row(
                dbc.Col(
                    html.Img(
                        src="/assets/cicd.png",
                        style={
                            "width": "89%",
                            "display": "block",
                            "margin": "0 auto",
                        },
                    ),
                    width=12,
                    className="text-center",
                )
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
            html.P("Architecture", className="subtitle", style={"transform": "translate(0, 20px)"}),
            dbc.Row(
                dbc.Col(
                    html.Img(
                        src="/assets/architecture.png",
                        style={
                            "width": "90%",
                            "display": "block",
                            "margin": "0 auto",
                        },
                    ),
                    width=12,
                    className="text-center",
                )
            ),
            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
        ],
    )
    # construct complete app layout:
    layout = html.Div(
        id="AppContainer",
        style={"padding-top": "5px", "padding-bottom": "5px"},
        children=[
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="home_session", storage_type="session"),
            dcc.Store(id="active_tab_store", data={"active_tab": "performance"}),
            html.Div(
                children=[
                    html.P(
                        id="AppTitle",
                        className="temp middle title",
                        children=[
                            "The Capital Fund",
                        ],
                    ),
                    dbc.Row(
                        id="DeltaScreenRow",
                        justify="center",
                        children=dbc.Col(
                            width=9,
                            children=[
                                html.Div(
                                    id="DeltaScreen",
                                    children=[
                                        html.Div(
                                            className="scrolling-text",
                                            children=[format_delta(d) for d in 200 * prices.deltas()],
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ),
                    dbc.Row(
                        id="NavBar",
                        className="navbar",
                        justify="center",
                        children=[
                            dbc.Col(
                                width=9,
                                children=[
                                    dbc.Tabs(
                                        id="NavBarTabs",
                                        active_tab="performance",
                                        children=[
                                            dbc.Tab(
                                                label="Performance",
                                                tab_id="performance",
                                            ),
                                            dbc.Tab(
                                                label="Analysis",
                                                tab_id="analysis",
                                            ),
                                            dbc.Tab(
                                                label="Intel",
                                                tab_id="intel",
                                            ),
                                            dbc.Tab(
                                                label="Research",
                                                tab_id="research",
                                            ),
                                            dbc.Tab(
                                                label="About",
                                                tab_id="about",
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    ),
                    dbc.Row(
                        id="TabContent",
                        justify="center",
                        children=[
                            dbc.Col(
                                id="TabContentCol",
                                width=9,
                                children=[
                                    html.Div(
                                        id="TabContentInner",
                                        children=[
                                            html.P("spacer", style={"font-size": "2px", "opacity": "0"}),
                                            html.Div(
                                                id="PerformanceContent",
                                                children=_performance_tab,
                                                style={
                                                    "display": "block",
                                                },
                                            ),
                                            html.Div(
                                                id="AnalysisContent",
                                                children=_analysis_tab,
                                                style={
                                                    "display": "none",
                                                },
                                            ),
                                            html.Div(
                                                id="IntelContent",
                                                children=_intel_tab,
                                                style={
                                                    "display": "none",
                                                },
                                            ),
                                            html.Div(
                                                id="ResearchContent",
                                                children=_research_tab,
                                                style={
                                                    "display": "none",
                                                },
                                            ),
                                            html.Div(
                                                id="AboutContent",
                                                children=_about_tab,
                                                style={
                                                    "display": "none",
                                                },
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                ]
            ),
        ],
    )
    return layout
