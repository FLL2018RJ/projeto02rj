import subprocess
import smtplib
import socket
from email.mime.text import MIMEText
import datetime
from time import sleep

class EnviaEmail(object):
    def email(self, aviso):
        try:
            to = 'aaaaaaaaaaaaaaaa@gmail.com'
            gmail_user = 'aaaaaaa.aaaaaa@al.infnet.edu.br'
            gmail_password = 'aaaaaaaaaaa'
            smtpserver = smtplib.SMTP('smtp.gmail.com', 587)
            smtpserver.ehlo()
            smtpserver.starttls()
            smtpserver.login(gmail_user, gmail_password)
            today = datetime.date.today()
            aviso = aviso
            my_ip='Aviso da estação de alimentação: %s' % aviso
            msg=MIMEText(my_ip)
            msg['Subject']= aviso
            msg['From']= gmail_user
            msg['To'] = to
            smtpserver.sendmail(gmail_user, [to], msg.as_string())
            smtpserver.quit()
        except:
            print("  EMAIL NÃO ENVIADO  ")
            print("  EMAIL NÃO ENVIADO  ")