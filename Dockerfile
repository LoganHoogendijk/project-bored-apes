FROM python:3.9-slim-buster

WORKDIR /project-bored-apes

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["flask", "run", "--host=0.0.0.0"]

EXPOSE 5000

