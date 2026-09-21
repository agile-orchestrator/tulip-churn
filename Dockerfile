FROM python:3.12-slim

WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY pyproject.toml uv.lock README.md ./
COPY src ./src
RUN uv sync --no-dev --frozen

# TODO: model artifact? models/ is gitignored, need to decide how the image gets the model
COPY models ./models

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "tulip_churn.api:app", "--host", "0.0.0.0", "--port", "8000"]
