FROM python:3.10.7

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED=1

WORKDIR /app

EXPOSE 8000

COPY requirements.txt ./

RUN pip install -r requirements.txt
RUN pip install "git+https://github.com/ai-forever/Kandinsky-2.git"
RUN pip install "git+https://github.com/openai/CLIP.git"

COPY . .
CMD ["python", "main_app/manage.py", "runserver", "0.0.0.0:8000"]
