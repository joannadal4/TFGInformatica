FROM python:3.7-slim
    
COPY requirements.txt requirements.txt 
RUN pip install -r requirements.txt  
RUN apt-get update -y
RUN apt-get install -y hmmer2
<<<<<<< HEAD
=======
COPY . /    
>>>>>>> 2c113271bd97b7914f3a51fffd8b77e415e8a600
WORKDIR app

CMD ["python", "main.py"]


