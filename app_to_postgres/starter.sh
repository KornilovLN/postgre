#!/bin/bash

# Создание Docker-образа:
docker build -t app_to_postgers .

# Запуск Docker-контейнера:
docker run --name app_postgres_cont -p 5000:5000 app_to_postgers
