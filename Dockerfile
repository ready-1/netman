FROM python:3.8-slim

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN pip install poetry && poetry install --no-root

COPY netman/ netman/

CMD ["poetry", "run", "python", "netman/app.py"]