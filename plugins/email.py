from flask_mail import Message

from app import mail


def send_email(subject, recipients, template):
    """
    Function used to send e-mail.
    """
    msg = Message(subject,
                  sender="scp.library.app@noreply.com",
                  html=template,
                  recipients=[recipients])
    mail.send(msg)
