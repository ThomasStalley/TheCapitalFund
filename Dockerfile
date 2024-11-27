# use python 3.10 slim as base:
FROM python:3.10-slim
# set workdir:
WORKDIR /app
# install system dependencies:
RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*
# install poetry:
RUN curl -sSL https://install.python-poetry.org | python3 -
# set poetry path:
ENV PATH="/root/.local/bin:$PATH"
# copy poetry files:
COPY pyproject.toml poetry.lock /app/
# install dependencies and project:
RUN poetry install
# copy app code:
COPY . /app
# expose port 8050:
EXPOSE 8050
# set entrypoint:
CMD ["poetry", "run", "python", "-m", "thecapitalfund.app"]