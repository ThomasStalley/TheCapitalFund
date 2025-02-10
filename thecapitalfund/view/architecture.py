from graphviz import Digraph

dot = Digraph(name="architecture")
# codebase architecture:
with dot.subgraph(name="cluster_codebase") as codebase:
    codebase.attr(
        label="<<I>Repositories</I>>",
        labelloc="b",
        labeljust="r",
        style="rounded",
        color="black",
    )
    codebase.node(
        name="backend",
        label="""<<B>GitHub: Backend</B><br/>API: FastAPI for prices, members and transactions.<br/>Daily: Scrape latest prices, update databases and send update email.<br/>Data: SQLite databases for prices, members and transactions.<br/>>""",
        shape="box",
        style="rounded,dashed",
        color="black",
        fontname="Serif",
        width="7",
        height="1.0",
    )
    codebase.node(
        name="frontend",
        label="""<<B>GitHub: Frontend</B><br/>App: Model-View-Controller dash web app.<br/>>""",
        shape="box",
        style="rounded,dashed",
        color="black",
        fontname="Serif",
        width="7",
        height="1.0",
    )
# hosting architecture:
with dot.subgraph(name="cluster_hosting") as hosting:
    hosting.attr(
        label="<<I>Deployment</I>>",
        labelloc="b",
        labeljust="r",
        style="rounded",
        color="black",
    )
    hosting.node(
        name="hosting_backend",
        label="""<<B>AWS Elastic Container Service</B><br/>Latest image is ran service @ capitalapi.auchester.com>""",
        shape="box",
        style="rounded,dashed",
        color="black",
        fontname="Serif",
        width="7",
        height="1.0",
    )
    hosting.node(
        name="hosting_frontend",
        label="""<<B>Render Web Service</B><br/>Latest image is ran as web service @ thecapitalfund.onrender.com>""",
        shape="box",
        style="rounded,dashed",
        color="black",
        fontname="Serif",
        width="7",
        height="1.0",
    )
# link the nodes with arrows:
dot.edge(
    "backend",
    "hosting_backend",
    style="dotted",
    color="black",
    arrowhead="normal",
)
dot.edge(
    "frontend",
    "hosting_frontend",
    style="dotted",
    color="black",
    arrowhead="normal",
)
# save figure as img:
dot.format = "png"
dot.attr(dpi="300")
dot.render("thecapitalfund/assets/architecture")
