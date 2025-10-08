MAINTAINER urielf

FROM python:3.13-alpine
WORKDIR /app
COPY requirements.txt .
RUN pip install -r --no-cache-dir reuirements.txt
COPY . .
EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:app"]