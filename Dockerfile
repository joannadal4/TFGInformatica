FROM python:3.7-slim

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN apt-get update -y
RUN apt-get install -y hmmer

CMD ["python", "main.py", "final_list.hmms"]

COPY . /

