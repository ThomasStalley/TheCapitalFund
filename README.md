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
    ├── assets/
    ├── model/
    ├── view/
    └── controller/
```
 