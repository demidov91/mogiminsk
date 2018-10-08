FROM python:3.7-stretch

RUN mkdir /app
WORKDIR /app


COPY requirements.in /app/requirements.in
COPY requirements.txt /app/requirements.txt

# For the case if I forgot to update requirements.txt
RUN pip install pip-tools
RUN pip-compile

RUN pip install -r requirements.txt

CMD ./start.sh
