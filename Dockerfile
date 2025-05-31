FROM python:3.12-bookworm

WORKDIR /usr/src/fastapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./code ./code

WORKDIR /usr/src/fastapi/code
CMD [ "fastapi", "run", "main.py" ]
