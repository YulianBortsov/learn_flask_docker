FROM python:3.9.18-alpine
WORKDIR /app
COPY . /app
RUN pip3 install -r /app/requirements.txt
#CMD ["flask", "--app", "hello.py", "run"]
#CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["python3", "hello.py"]
