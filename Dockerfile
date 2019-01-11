FROM python:3.6

RUN apt-get update -y && apt-get install -y cron

ADD crontab /etc/cron.d/crontab
RUN chmod 644 /etc/cron.d/crontab

RUN mkdir /app
WORKDIR /app
ADD alembic alembic
ADD block_ip block_ip
ADD bot bot
ADD bot_telegram bot_telegram
ADD bot_viber bot_viber
ADD locale locale
ADD messager messager
ADD mogiminsk mogiminsk
ADD mogiminsk_interaction mogiminsk_interaction
ADD tasklocal tasklocal
ADD tests tests
ADD aiohttp_translation.py aiohttp_translation.py
ADD alembic.ini alembic.ini
ADD conftest.py conftest.py
ADD requirements.txt requirements.txt
ADD start_server.sh start_server.sh

RUN pip install -r requirements.txt

CMD env > /home/cron-env.sh && chmod u+x /home/cron-env.sh && cron && ./start_server.sh

