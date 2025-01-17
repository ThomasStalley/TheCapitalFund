_**📈 The Capital Fund 📈**_

A mock investment fund web application - built with <a href="https://dash.plotly.com/">dash, by plotly</a>.

The app is updated daily, with real world financial data, sourced from an asset price api.

$$. . .$$

_**🚀 Quick Start 🚀**_

build the docker container:
```
docker-compose build --no-cache
```

run the container:
```
docker-compose up -d
```

stop the container:
```
docker-compose down
```

$$. . .$$

_**🗂 Project Structure 🗂**_

model-view-controller architecture:
```
.
├── Dockerfile
├── README.md
├── docker-compose.yml
├── poetry.lock
├── pyproject.toml
└── thecapitalfund
    ├── __init__.py
    ├── app.py
    ├── assets
    │   ├── architecture.png
    │   ├── cicd.png
    │   ├── dots.ttf
    │   ├── favicon.ico
    │   ├── style.css
    │   └── temp.ttf
    ├── controller
    │   ├── callbacks.py
    │   ├── login.py
    │   └── models.py
    ├── model
    │   ├── api.py
    │   ├── members.py
    │   ├── prices.py
    │   └── transactions.py
    ├── testing
    │   ├── __init__.py
    │   └── test_login.py
    └── view
        ├── layout.py
        └── plotting.py
```
 