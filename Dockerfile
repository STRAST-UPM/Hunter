FROM python:3.12-slim-bookworm

LABEL org.opencontainers.image.source=https://github.com/STRAST-UPM/Hunter

WORKDIR /usr/src/hunter

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./code/main.py ./code/.
COPY ./code/src ./code/src

CMD ["fastapi", "run", "code/main.py"]
