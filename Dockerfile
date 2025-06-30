FROM python:3.9-slim-bullseye
RUN apt-get update && apt-get upgrade -y && apt-get install -y --no-install-recommends \
	&& apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 20777/udp
CMD ["python", "main.py"]
