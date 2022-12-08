FROM python:3.11-slim
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip && pip install -r requirements.txt


CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 8000