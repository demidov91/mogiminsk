from collections import defaultdict
import logging
import smtplib

from email.message import EmailMessage

from mogiminsk.services.conversation import ConversationService
from mogiminsk.settings import (
    EMAIL_FEEDBACK_SUBJECT,
    EMAIL_HOST, EMAIL_PORT,
    EMAIL_FROM, EMAIL_TO,
    EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
)
from mogiminsk.utils import threaded_session


logger = logging.getLogger(__name__)


def build_user_thread(messages):
    message = messages[0]
    caption = f'{message.messenger}\n' \
              f'{message.user.first_name} ({message.user.phone})'

    return caption + '\n' '\n~\n'.join(build_message(x) for x in messages)


def build_message(message):
    return f'{message.created_at}\n{message.text}\n{message.context}'


def send(content):
    email_message = EmailMessage()
    email_message.set_content(content)
    email_message['Subject'] = EMAIL_FEEDBACK_SUBJECT
    email_message['From'] = EMAIL_FROM
    email_message['To'] = EMAIL_TO

    server = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    server.ehlo()
    server.starttls()
    server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    server_response = server.sendmail(EMAIL_FROM, EMAIL_TO, email_message.as_string())
    logger.info('SMTP server response: %s', server_response)
    server.close()


def run():
    not_seen_messages = ConversationService.not_seen()
    conversations = defaultdict(list)
    for msg in not_seen_messages:
        conversations[(msg.user_id, msg.messenger)].append(msg)

    if not conversations:
        logger.debug('No feedback.')
        return

    text = '\n\n----------\n\n'.join(build_user_thread(x) for x in conversations.values())
    send(text)
    not_seen_messages.update({'seen': True})
    threaded_session().commit()


if __name__ == '__main__':
    run()