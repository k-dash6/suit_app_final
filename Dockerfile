FROM python:3.10.0-alpine

WORKDIR /app

EXPOSE 8000

COPY requirements.txt ./

# RUN pip install

CMD ["pip", "install", "requirements.txt"]
COPY . .
CMD ["python", "main_app/manage.py", "runserver"]