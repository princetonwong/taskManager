FROM python:3.11.3-slim-buster
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
WORKDIR /app
COPY pyproject.toml /app
ENV PYTHONPATH=${PYTHONPATH}:${PWD}
RUN poetry install --no-dev --no-interaction --no-ansi
RUN poetry run pip3 install psycopg2-binary
COPY . /app
CMD ["python", "main.py"]