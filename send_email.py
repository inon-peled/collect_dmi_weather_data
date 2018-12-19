import json
from email.message import EmailMessage
import smtplib


def get_smtp_credentials(config_path):
    with open(config_path, 'r') as f:
        return json.load(f)


def send(subject, body, smtp_config_path='smtp_config.json'):
    config = get_smtp_credentials(smtp_config_path)
    msg = EmailMessage()
    msg['From'] = config['user']
    msg['To'] = config['to']
    msg['Subject'] = subject
    msg.set_content(body)

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    server.login(config['user'], config['password'])
    server.send_message(msg)
    server.close()
    print('Email sent')


if __name__ == '__main__':
    send('Testing 123', 'Ignore this message')
