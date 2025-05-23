FROM python:3.11-slim AS build

RUN apt-get update && \
    apt-get install -y --no-install-recommends build-essential gcc libpcre3 libpcre3-dev

WORKDIR /usr/app

RUN python -m venv /usr/app/venv
ENV PATH="/usr/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN python manage.py collectstatic --noinput

# --- multistage build
FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends libpcre3 && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /usr/app

COPY --from=build /usr/app/venv ./venv
COPY --from=build /usr/app /usr/app

ENV PATH="/usr/app/venv/bin:$PATH"

RUN useradd uwsgi && \
    chown -R uwsgi:uwsgi /usr/app

USER uwsgi

EXPOSE 8000

CMD ["uwsgi", "--master", "--enable-threads", "--thunder-lock", "--single-interpreter", "--http", ":8000", "--module", "war.wsgi", "--static-map", "/static=/usr/app/staticfiles"]
