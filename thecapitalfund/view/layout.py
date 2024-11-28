import dash_bootstrap_components as dbc
from dash import dcc, html

from thecapitalfund.model import prices
from thecapitalfund.view import plotting


def get_layout() -> html.Div:
    """Construct and return app layout."""
    asset_data = prices.get_asset_data()
    today = prices.today()
    # construct tab layouts:
    _performance_tab = dbc.Container(
        id="PerformanceTab",
        fluid=True,
        children=[
            dbc.Row(
                id="PlottingContainer",
                children=[
                    dbc.Row(
                        dbc.Col(
                            id="TotalPlottingContainer",
                            children=[
                                dcc.Loading(
                                    children=dcc.Graph(
                                        id="TotalPlot",
                                        figure=plotting.total(asset_data),
                                        config={"displayModeBar": False},
                                        style={"height": "500px"},
                                    ),
                                    type="circle",
                                    color="#000000",
                                ),
                            ],
                        ),
                    ),
                    dbc.Row(
                        dbc.Col(
                            id="AssetsPlottingContainer",
                            children=[
                                html.Div(
                                    children=dcc.Graph(
                                        id="AssetsPlot",
                                        figure=plotting.assets(asset_data),
                                        config={"displayModeBar": False},
                                        style={"height": "350px"},
                                    )
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        ],
    )
    _fund_tab = dbc.Container(
        id="FundTab",
        children=[
            dbc.Row(
                dbc.Col(
                    dbc.Table(
                        [
                            html.Thead(
                                html.Tr(
                                    [
                                        html.Th("Asset", id="asset-header", className="red-temp"),
                                        html.Th("Code", id="code-header", className="red-temp"),
                                        html.Th("Units", id="unit-header", className="red-temp"),
                                        html.Th("Price", id="price-header", className="red-temp"),
                                        html.Th("Day", id="daily-header", className="red-temp"),
                                        html.Th("Week", id="weekly-header", className="red-temp"),
                                        html.Th("All", id="all-time-header", className="red-temp"),
                                    ]
                                )
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Financial assets comprising The Capital Fund.",
                                        className="popover-text",
                                    )
                                ],
                                id="asset-popover",
                                target="asset-header",
                                trigger="hover",
                                className="table-header-popover",
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Financial asset code.",
                                        className="popover-text",
                                    ),
                                ],
                                id="code-popover",
                                target="code-header",
                                trigger="hover",
                                className="table-header-popover popover-text",
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Amount of the financial asset held in 1 unit of The Capital Fund.",
                                        className="popover-text",
                                    ),
                                ],
                                id="unit-popover",
                                target="unit-header",
                                trigger="hover",
                                className="table-header-popover popover-text",
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Price is from previous market day close.",
                                        className="popover-text",
                                    ),
                                ],
                                id="price-popover",
                                target="price-header",
                                trigger="hover",
                                className="table-header-popover popover-text",
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Daily percentage change in price.",
                                        className="popover-text",
                                    ),
                                ],
                                id="daily-popover",
                                target="daily-header",
                                trigger="hover",
                                className="table-header-popover popover-text",
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Weekly percentage change in price.",
                                        className="popover-text",
                                    ),
                                ],
                                id="weekly-popover",
                                target="weekly-header",
                                trigger="hover",
                                className="table-header-popover popover-text",
                            ),
                            dbc.Popover(
                                [
                                    dbc.PopoverBody(
                                        "Percentage change in price since fund opening.",
                                        className="popover-text",
                                    ),
                                ],
                                id="all-time-popover",
                                target="all-time-header",
                                trigger="hover",
                                className="table-header-popover popover-text",
                            ),
                            html.Tbody(
                                [
                                    html.Tr(
                                        [
                                            html.Td("The Capital Fund"),
                                            html.Td("TCF-GBP"),
                                            html.Td("1.00"),
                                            html.Td(f"£{today.get('tcf_price')}"),
                                            html.Td(f"{today.get('day_percent_change_tcf')}%"),
                                            html.Td(f"{today.get('week_percent_change_tcf')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_tcf')}%"),
                                        ],
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("World Index Fund"),
                                            html.Td("VAEIAGA"),
                                            html.Td("8.00"),
                                            html.Td(f"£{today.get('van_price')}"),
                                            html.Td(f"{today.get('day_percent_change_van')}%"),
                                            html.Td(f"{today.get('week_percent_change_van')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_van')}%"),
                                        ]
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("Bitcoin"),
                                            html.Td("BTC-GBP"),
                                            html.Td("0.0014349"),
                                            html.Td(f"£{today.get('btc_price')}"),
                                            html.Td(f"{today.get('day_percent_change_btc')}%"),
                                            html.Td(f"{today.get('week_percent_change_btc')}%"),
                                            html.Td(f"{today.get('all_time_percent_change_btc')}%"),
                                        ]
                                    ),
                                    html.Tr(
                                        [
                                            html.Td("Ether"),
                                            html.Td("ETH-GBP"),
                                            html.Td("0.0199347"),
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
                    ),
                    width=10,
                ),
                justify="center",
            ),
        ],
    )
    _assets_tab = dbc.Container(
        id="AssetsTab",
        children=[
            dbc.Row(dbc.Col(html.P("The Capital Fund", className="temp middle subtitle"))),
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "The Capital Fund is a mixed asset investment fund. The Capital Fund integrates the "
                            "stability and ethical considerations of the Vanguard ESG Developed World All Cap Equity Index "
                            "Fund with the innovative potential of the cryptocurrencies Bitcoin and Ether. The Capital Fund "
                            "is defined by its one and only core value - optimism."
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
            dbc.Row(dbc.Col(html.P("Vanguard ESG Developed World Index Fund", className="temp middle subtitle"))),
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "The Vanguard ESG Developed World All Cap Equity Index Fund is a mutual fund that aims to provide l"
                            "ong-term growth by tracking the performance of the FTSE Developed All Cap Choice Index. This index"
                            " reflects the performance of stocks from developed countries worldwide, excluding companies involv"
                            "ed in non-renewable energy, weapons, vice products, and other activities deemed not to meet certai"
                            "n environmental, social, and governance (ESG) criteria."
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Bitcoin", className="temp middle subtitle"),
                ),
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "Bitcoin (BTC) is the first and most well-known cryptocurrency, founded in 2009 by an individual or"
                            " group of individuals operating under the pseudonym Satoshi Nakamoto. It is a decentralized digita"
                            "l currency that allows for peer-to-peer transactions across a global network without the need for "
                            "intermediaries such as banks or governments. Bitcoin operates on a blockchain, a distributed ledge"
                            "r technology that records all transactions across a network of computers to ensure security and tr"
                            "ansparency. Bitcoin's supply is capped at 21 million coins, a feature that aims to mimic th"
                            "e scarcity and value of precious metals and to prevent inflation."
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
            dbc.Row(
                dbc.Col(
                    html.P("Ether", className="temp middle subtitle"),
                ),
            ),
            dbc.Row(
                dbc.Col(
                    [
                        html.P(
                            "Ether (ETH) is the native cryptocurrency of the Ethereum platform, which is a decentralized, open-"
                            "source blockchain system. Ethereum was proposed in late 2013 by programmer Vitalik Buterin and dev"
                            "elopment was crowdfunded in 2014, and the network went live on 30 July 2015. ETH serves as a mediu"
                            "m of exchange and a store of value, but it is also used to compensate participant nodes for comput"
                            "ations performed. Unlike Bitcoin, Ethereum is designed to be more than a payment system; it is a p"
                            "latform for building decentralized applications (dApps) using smart contracts, which are self-exec"
                            "uting contracts with the terms of the agreement between buyer and seller directly written into lin"
                            "es of code."
                        ),
                    ],
                    width=10,
                ),
                justify="center",
            ),
        ],
    )
    _about_tab = dbc.Container(
        id="AboutTab",
        children=[
            dbc.Row(
                children=[
                    html.P(
                        "This is a personal programming project, the goal being to create a production level, investment fund platform."
                    ),
                    html.P(
                        "The app is updated daily, with real world financial data, sourced from an asset price api."
                    ),
                    html.P(
                        " . . . ",
                        className="temp",
                    ),
                    html.P(
                        [
                            "See the source code in github: ",
                            html.A(
                                "github.com/thomasstalley/thecapitalfund",
                                href="https://github.com/thomasstalley/thecapitalfund",
                                target="_blank",
                                style={"color": "#BD0404"},
                            ),
                            ".",
                        ]
                    ),
                    html.P(
                        " . . . ",
                        className="temp",
                    ),
                    html.P(
                        [
                            "Built with dash, by plotly: ",
                            html.A(
                                "dash.plotly.com",
                                href="https://dash.plotly.com/",
                                target="_blank",
                                style={"color": "#BD0404"},
                            ),
                            ".",
                        ]
                    ),
                ],
                className="ebg middle",
            ),
        ],
    )
    # construct main layout:
    layout = html.Div(
        id="AppContainer",
        style={"padding-top": "5px", "padding-bottom": "5px"},
        children=[
            dcc.Location(id="url", refresh=False),
            dcc.Store(id="home_session", storage_type="session"),
            dcc.Store(id="active_tab_store", data={"active_tab": "performance"}),
            html.Div(
                children=[
                    dbc.Modal(
                        id="ModalLogin",
                        size="sm",
                        backdrop=True,
                        is_open=False,
                        fade=True,
                        children=[
                            dbc.ModalHeader(
                                id="ModalHeader",
                                close_button=False,
                                style={"display": "flex", "flexDirection": "column", "alignItems": "center"},
                                children=[
                                    html.P("Log In", id="ModalHeaderText"),
                                    html.P(
                                        "example username: EXAMPLE", id="HeaderTwoValueText", style={"display": "none"}
                                    ),
                                    html.P(
                                        "example password: 112233", id="HeaderThrValueText", style={"display": "none"}
                                    ),
                                ],
                            ),
                            dcc.Loading(
                                type="circle",
                                color="#000000",
                                children=[
                                    dbc.ModalBody(
                                        children=[
                                            html.Div(
                                                id="UserIdOuter",
                                                children=[
                                                    dcc.Input(
                                                        id="UserIdInput",
                                                        type="text",
                                                        value="",
                                                        placeholder="Username: 'EXAMPLE'",
                                                    ),
                                                ],
                                            ),
                                            html.Div(
                                                id="UserPasswordOuter",
                                                children=[
                                                    dcc.Input(
                                                        id="UserPasswordInput",
                                                        type="password",
                                                        value="",
                                                        placeholder="Password: 'PASSWRD'",
                                                    ),
                                                ],
                                            ),
                                        ]
                                    ),
                                ],
                            ),
                            dbc.ModalFooter(
                                id="ModalFooter",
                                children=dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Button(
                                                "↺",
                                                id="FooterHomeButton",
                                                n_clicks=0,
                                                className="temp btn btn-primary",
                                            ),
                                            width=6,
                                        ),
                                        dbc.Col(
                                            dbc.Button(
                                                "→",
                                                id="FooterLoginButton",
                                                n_clicks=0,
                                                className="temp btn btn-primary3",
                                            ),
                                            width=6,
                                        ),
                                    ],
                                    justify="around",
                                    align="center",
                                ),
                            ),
                        ],
                    ),
                    html.P(
                        id="AppTitle",
                        className="temp middle title",
                        children=[
                            "The Capital Fund",
                        ],
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
                                                label="Holdings",
                                                tab_id="fund",
                                            ),
                                            dbc.Tab(
                                                label="Assets",
                                                tab_id="asset",
                                            ),
                                            dbc.Tab(
                                                label="About",
                                                tab_id="about",
                                            ),
                                            dbc.Tab(
                                                label="Log In",
                                                tab_id="login",
                                                id="OpenModalLogin",
                                                label_style={},
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
                                            html.P(
                                                "spacer",
                                                style={
                                                    "font-size": "1px",
                                                    "opacity": "0",
                                                },
                                            ),
                                            html.Div(
                                                id="PerformanceContent",
                                                children=_performance_tab,
                                                style={
                                                    "display": "block",
                                                },
                                            ),
                                            html.Div(
                                                id="FundContent",
                                                children=_fund_tab,
                                                style={
                                                    "display": "none",
                                                },
                                            ),
                                            html.Div(
                                                id="AssetContent",
                                                children=_assets_tab,
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
