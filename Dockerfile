FROM python:alpine

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

COPY app/ .

EXPOSE 8000

CMD ["gunicorn", "-w 4", "-b 0.0.0.0:8000", "api:app"]
