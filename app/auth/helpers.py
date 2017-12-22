"""
Helper functions for auth module
"""
from flask_security.confirmable import generate_confirmation_link
from flask_mail import Message

from app import mail


def confirm_email(user):
    confirmation_link, token = generate_confirmation_link(user)

    subject = 'Confirmation Email for ' + user.first_name

    content = '''
              Please confirm your email with the following link: \n \n
    
              {}
              '''.format(confirmation_link)

    msg = Message(subject=subject, body=content, recipients=[user.email])

    mail.send(msg)
