import smtplib
from email import encoders
import socket
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.message import EmailMessage
import mimetypes
import io

email_login = 'my_login'
email_pass = 'my_pass'


def post_to_email(from_addr, to_addr, subject, message, email_login, email_pass, buf=None, buf_filename=None, msg_format='plain'):
	msg = EmailMessage()
	msg['From'] = from_addr
	msg['To'] = ';'.join(to_addr)
	msg['Subject'] = subject

	body = message
	msg.attach(MIMEText(body, msg_format))

	if buf is not None:
		buf.seek(0)
		binary_data = buf.read()
		maintype, _, subtype = (mimetypes.guess_type(buf_filename)[0] or 'application/octet-stream').partition('/')
		msg.add_attachment(binary_data, maintype=maintype, subtype=subtype, filename=buf_filename)

	server = smtplib.SMTP('server.com', 111)
	server.login(email_login, email_pass)
	text = msg.as_string()
	print(f'Sending message to {str(to_addr)}')
	server.sendmail(from_addr, to_addr, text)
	server.quit()