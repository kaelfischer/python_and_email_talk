#!/usr/bin/env python
"""
send email with attachments and all that.

Adapted from http://stackoverflow.com/a/3363254/730154
"""

import os
import os.path

# all the email stuff is in the standard library
import smtplib
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE

import dotenv



def get_env_variable(var_name):
    """ Get the environment variable or return exception """
    try:
        return os.environ[var_name]
    except KeyError:
        error_msg = "Set the %s environment variable" % var_name
        raise RuntimeError(error_msg)

REAL_PATH = os.path.join(os.path.dirname(os.path.realpath(__file__)))
DOTENV_PATH = os.path.join(REAL_PATH,'.env')
dotenv.load_dotenv(DOTENV_PATH)

SMTP_USER = get_env_variable('SMTP_USER')
SMTP_PASSWORD = get_env_variable('SMTP_PASSWORD')
SMTP_HOST = get_env_variable('SMTP_HOST')
SMTP_PORT = int(get_env_variable('SMTP_PORT'))
DEFAULT_FROM_ADDRESS = get_env_variable('DEFAULT_FROM_ADDRESS')


def send_mail_with_smtp_authetication(send_from, send_to, subject, body, files=None,
                                      smtp_user=SMTP_USER, smtp_password=SMTP_PASSWORD,
                                      smtp_host=SMTP_HOST, smtp_port=SMTP_PORT,
                                      other_msg_headers=None):
    """
    Assemble a multipart mime message and send it to a stmp server using SMTP authentication

    :param send_from: email address
    :param send_to:   iterable of email addresses (may have to be a list)
    :param subject:   text for subject line
    :param body:      text for the message body
    :param files:     list of paths to the files that will be included as attachments
    :param smtp_user:
    :param smtp_password:
    :param smtp_host:
    :param smtp_port:
    :param other_msg_headers: dictionary for things like 'Reply-To'
    :return: None
    """

    msg = MIMEMultipart()

    # message not a real dictionary so we can't use msg.update
    if isinstance(other_msg_headers,dict):
        for k,v in other_msg_headers.iteritems():
            msg[k] = v
    # minimal readers
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Subject'] = subject

    # now the mime bits
    msg.attach(MIMEText(body))
    for f in files or []:
        with open(f, "rb") as this_file:
            part = MIMEApplication(
                this_file.read(),
                Name=os.path.basename(f)
            )
            part['Content-Disposition'] = 'attachment; filename="%s"' % os.path.basename(f)
            msg.attach(part)


    smtp = smtplib.SMTP(smtp_host,smtp_port)
    smtp.starttls()
    smtp.login(smtp_user,smtp_password)
    smtp.sendmail(send_from, send_to, msg.as_string())
    smtp.close()


if __name__ == '__main__':
    # If you run from the command line, I get a frog picture!
    send_mail_with_smtp_authetication(DEFAULT_FROM_ADDRESS,['kael@ubiota.com'],'frog!',
                                      'look at this frog man!\n',
                                      [os.path.join(REAL_PATH,'Tripping-Frog-53343187.jpg')])