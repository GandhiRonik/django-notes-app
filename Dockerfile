FROM python:3.9

WORKDIR /app/backend

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y gcc default-libmysqlclient-dev pkg-config \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/backend/
RUN pip install --no-cache-dir mysqlclient
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/backend/

EXPOSE 8000

CMD ["gunicorn", "notesapp.wsgi", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
