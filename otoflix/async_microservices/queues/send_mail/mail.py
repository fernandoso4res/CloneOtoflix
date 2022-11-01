import smtplib
import email.message
import sys
from jinja2 import FileSystemLoader, Environment
from config import *


def send_mail(mail_data):
    try:
        msg = prepare_message(mail_data)
        with smtplib.SMTP(MAIL_HOST, MAIL_PORT) as server:
            server.login(MAIL_USERNAME, MAIL_PASSWORD)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
    except Exception as e:
        print('e', e)
        print(sys.exc_info())


def prepare_message(mail_data):
    subject, payload = get_email_subject_and_payload(
        mail_data['email_type'], mail_data['kwargs'])
    msg = email.message.Message()
    msg['Subject'] = subject
    msg['From'] = MAIL_DEFAULT_SENDER
    msg['To'] = mail_data['recipients']
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(payload)
    msg.set_charset('utf-8')
    return msg


def get_email_subject_and_payload(email_type, kwargs):
    subject = None
    payload = None
    match email_type:
        case 'forgot_password_send_token':
            subject = 'Otoflix - Solicitação de redefinição de senha'
            payload = get_email_template(
                'forgot_password_send_token.html', kwargs)
    return subject, payload


def get_email_template(html_name, kwargs):
    loader = FileSystemLoader('templates')
    env = Environment(loader=loader)
    template = env.get_template(html_name)
    return template.render(**kwargs)
