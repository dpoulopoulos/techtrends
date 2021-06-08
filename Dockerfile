FROM python:2.7

EXPOSE 3111

WORKDIR /src

COPY . .

WORKDIR /src/techtrends

RUN pip install -r requirements.txt

RUN python init_db.py

CMD ["python", "app.py"]