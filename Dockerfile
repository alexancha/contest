# Используем базовый образ Python с установленным Poetry
FROM python:3.11

# Устанавливаем переменную окружения PYTHONUNBUFFERED для более предсказуемого вывода
ENV PYTHONUNBUFFERED 1

# Устанавливаем Poetry
RUN pip install poetry

# Создаем и устанавливаем рабочую директорию /app
WORKDIR /app

# Копируем файлы pyproject.toml и poetry.lock для установки зависимостей
COPY pyproject.toml poetry.lock /app/

# Устанавливаем зависимости Poetry
RUN poetry install --no-root --no-interaction

# Копируем все файлы проекта в рабочую директорию
COPY . /app/

RUN ls -la /app

EXPOSE 8000
#
#CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]


# Определяем переменные окружения для PostgreSQL
#ENV POSTGRES_DB=mydatabase \
#    POSTGRES_USER=mydatabaseuser \
#    POSTGRES_PASSWORD=mypassword \
#    POSTGRES_HOST=db \
#    POSTGRES_PORT=5432

# Ожидаем, чтобы PostgreSQL была готова принимать подключения
COPY wait-for-it.sh /usr/wait-for-it.sh
RUN chmod +x /usr/wait-for-it.sh

# Запускаем команду для ожидания готовности PostgreSQL и запуска Django-приложения
CMD /usr/wait-for-it.sh $POSTGRES_HOST:$POSTGRES_PORT -- gunicorn myproject.wsgi:application -b 0.0.0.0:8000
