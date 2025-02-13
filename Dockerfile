FROM python:3.12-slim

WORKDIR  /app
COPY ./pyproject.toml ./poetry.lock* /app/
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY ./src/ .
EXPOSE 8000
CMD ["poetry", "run", "uvicorn", "whats_for_dinner.main:app", "--reload", "--host", "0.0.0.0"]