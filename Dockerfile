FROM python:3.7.2-alpine3.9
WORKDIR /usr/src/app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["python", "server.py"]

