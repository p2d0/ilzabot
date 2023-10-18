FROM python:3.9

WORKDIR /app
COPY . /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends $(cat Aptfile)

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "iLzabot.py"]
