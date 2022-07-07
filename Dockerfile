FROM python:3.9-slim as venv-build
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
RUN apt-get update && apt-get -y install --no-install-recommends tini \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && addgroup --gid 1001 "elg" \
    && adduser --disabled-password --gecos "ELG User,,," --home /elg --ingroup elg --uid 1001 elg \
    && chmod +x /usr/bin/tini
COPY --chown=elg:elg --from=venv-build /opt/venv /opt/venv

USER elg:elg
WORKDIR /elg
COPY --chown=elg:elg app.py docker-entrypoint.sh /elg/
ENV PATH="/opt/venv/bin:$PATH"

ENV WORKERS=2
ENV TIMEOUT=60
ENV WORKER_CLASS=sync
ENV LOGURU_LEVEL=INFO
ENV PYTHON_PATH="/opt/venv/bin"

RUN chmod +x ./docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
