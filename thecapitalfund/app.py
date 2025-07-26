import os

from dash import Dash
from dash_bootstrap_components.themes import BOOTSTRAP

from thecapitalfund.controller import callbacks  # noqa
from thecapitalfund.view import layout


def main():
    app = Dash(__name__, external_stylesheets=[BOOTSTRAP])
    app.title = "The Capital Fund"
    app.layout = layout.get_layout()
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
