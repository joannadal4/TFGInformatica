FROM python:3.7-slim
    
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt  
RUN apt-get update -y
RUN apt-get install -y hmmer2
WORKDIR app

CMD ["python", "main.py"]

COPY . /    

