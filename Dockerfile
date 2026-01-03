FROM python:3.10-slim

RUN apt update && apt install -y build-essential gcc clang clang-tools libgl1 python3-dev cppcheck valgrind afl++ \
     gcc-multilib

# Копируем наши зависимости
COPY ./requirements.txt /requirements.txt

# Устанавливаем требуемые пакеты
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение
COPY ./app /app
WORKDIR /app

ENTRYPOINT bash run.sh
