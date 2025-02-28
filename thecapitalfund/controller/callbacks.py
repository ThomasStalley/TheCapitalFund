import dash
import pandas as pd
from dash import Input, Output

from thecapitalfund.model import prices

prices_data = pd.DataFrame(prices.get_asset_data())


@dash.callback(
    Output("PerformanceContent", "style"),
    Output("AnalysisContent", "style"),
    Output("IntelContent", "style"),
    Output("ResearchContent", "style"),
    Output("AboutContent", "style"),
    Input("NavBarTabs", "active_tab"),
)
def nav_bar_interaction(active_tab):
    """Change main content in response to nav bar tab click."""
    hidden = {"display": "none"}
    visible = {"display": "block"}
    active_tab = active_tab or "performance"
    # delta screen is visible only when performance tab
    contents = ["performance", "analysis", "intel", "research", "about"]
    return [visible if active_tab == content else hidden for content in contents]
