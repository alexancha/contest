FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN pip install poetry
WORKDIR /app
COPY pyproject.toml poetry.lock README.md /app/
COPY . /app
##RUN poetry config virtualenvs.create false && poetry install
#RUN poetry config virtualenvs.in-project true && \
#    poetry install --only=main --no-root && \
#    poetry build
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi
WORKDIR /app/src
EXPOSE 8000
CMD python manage.py runserver 0.0.0.0:8000
