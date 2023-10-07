FROM python:3.10
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY Dockerfile Dockerfile
COPY index.py index.py
COPY schedule_ortools.py schedule_ortools.py
CMD ["gunicorn", "--bind", "0.0.0.0:80", "index:app"]