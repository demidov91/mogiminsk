FROM python:3.7-stretch

RUN mkdir /app
WORKDIR /app


COPY requirements.in /app/requirements.in
COPY requirements.txt /app/requirements.txt

# For the case if I forgot to update requirements.txt
RUN pip install pip-tools
RUN pip-compile

# Install requirements.
RUN pip install -r requirements.txt

# Prepare an image to deploy to ECS. Copy directories...
COPY block_ip block_ip
COPY bot bot
COPY bot_telegram bot_telegram
COPY bot_viber bot_viber
COPY locale locale
COPY messager messager
COPY mogiminsk mogiminsk
COPY mogiminsk_interaction mogiminsk_interaction
COPY tasklocal tasklocal
# ... and files.
COPY aiohttp_translation.py .
COPY start.sh .

# Start gunicorn.
CMD ./start.sh
