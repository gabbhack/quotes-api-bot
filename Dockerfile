FROM python:3.9-slim-buster as production

ENV PYTHONPATH "${PYTHONPATH}:/app"

WORKDIR /app

# Install Poetry
RUN set +x \
 && apt update \
 && apt install -y curl \
 && curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python \
 && cd /usr/local/bin \
 && ln -s /opt/poetry/bin/poetry \
 && poetry config virtualenvs.create false \
 && rm -rf /var/lib/apt/lists/*

# Add code & install dependencies
ADD pyproject.toml poetry.lock* /app/
RUN poetry install -n --no-dev
ADD ./app /app/app

CMD [ "python", "-m", "app" ]
