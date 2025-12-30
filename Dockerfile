FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential curl && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

ENV PORT=10000

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --no-interaction --no-ansi

COPY . /app

RUN poetry install --no-interaction --no-ansi

EXPOSE 10000

CMD ["poetry", "run", "python", "-u", "thecapitalfund/app.py"]
