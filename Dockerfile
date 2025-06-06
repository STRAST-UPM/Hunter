FROM python:3.12-bookworm

LABEL org.opencontainers.image.source=https://github.com/STRAST-UPM/Hunter

WORKDIR /usr/src/hunter
COPY ./code/main.py .
COPY ./code/src ./src

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run", "main.py"]
