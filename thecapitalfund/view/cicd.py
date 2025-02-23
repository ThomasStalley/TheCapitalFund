from graphviz import Digraph

WIDTH = "5.8"
HEIGHT = "1"

dot = Digraph(name="cicd")

# daily run:
dot.node(
    "daily_update",
    """<
<B>Daily Update @ 4:40AM</B><br/>
• Get latest news stories, upload to db.<br/>
• Get latest price data, upload to db.<br/>
• Update members database using previous day transactions.<br/>
>""",
    shape="box",
    style="rounded",
    fontname="Serif",
    width=WIDTH,
    height=HEIGHT,
    fixedsize="true",
)
# redeploy of backend:
dot.node(
    "redeploy_backend",
    """<
<B>Redeploy Backend @ 4:50AM</B><br/>
• CI: Testing with pytest, linting with ruff.<br/>
• CD: Upload latest docker image to AWS elastic container repository.<br/>
• CD: Redeploy latest image as AWS elastic container service.<br/>
>""",
    shape="box",
    style="rounded",
    fontname="Serif",
    width=WIDTH,
    height=HEIGHT,
    fixedsize="true",
)
# redeploy of frontend:
dot.node(
    "redeploy_frontend",
    """<
<B>Redeploy Frontend @ 5:00AM</B><br/>
• CI: Testing with pytest, linting with ruff.<br/>
• CD: Trigger redeploy via post request to Render webhook.<br/>
• CD: Latest code redeployed on Render.<br/>
>""",
    shape="box",
    style="rounded",
    fontname="Serif",
    width=WIDTH,
    height=HEIGHT,
    fixedsize="true",
)
# link the nodes with arrows:
dot.edge("daily_update", "redeploy_backend")
dot.edge("redeploy_backend", "redeploy_frontend")
dot.attr(rankdir="LR")
# save figure as img:
dot.format = "png"
dot.attr(dpi="300")
dot.render("thecapitalfund/assets/cicd")
