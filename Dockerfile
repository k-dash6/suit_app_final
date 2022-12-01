FROM python:3.10.0-alpine

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8000

COPY requirements.txt ./

# RUN pip install

RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main_app/manage.py", "runserver", "0.0.0.0:8000"]