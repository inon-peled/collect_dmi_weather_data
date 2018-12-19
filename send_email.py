from email.message import EmailMessage
import smtplib

gmail_user = 'dtu.scripts.email@gmail.com'
gmail_password = 'notaverysecurepassword123'

sent_from = gmail_user
to = ['inon.peled@gmail.com', 'inonpe@dtu.dk']
subject = 'Subject'
body = 'Hello'

msg = EmailMessage()
msg['Subject'] = 'Test message 2, ignore'
msg['From'] = gmail_user
msg['To'] = to[0]
msg.set_content('Hello')

server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.ehlo()
server.login(gmail_user, gmail_password)
server.send_message(msg)
server.close()
print('Email sent!')
