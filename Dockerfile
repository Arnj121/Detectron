FROM python:3.7

WORKDIR /app
COPY . .
EXPOSE 3033 3034

RUN pip install -r requirements.txt
ENV FLASK_APP=server.py
CMD flask run -h 0.0.0.0 -p 3033

ENV FLASK_APP=searchServer.py
CMD flask run -h 0.0.0.0 -p 3034 
