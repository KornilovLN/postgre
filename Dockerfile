FROM postgres:15.2-alpine

# Установка nano
RUN apt-get update && apt-get install -y nano

# Копирование init.sql в контейнер
#COPY init.sql /docker-entrypoint-initdb.d/

# Установка переменных окружения
#ENV POSTGRES_USER=starmark
#ENV POSTGRES_PASSWORD=admin
#ENV POSTGRES_DB=Common-Postgres
