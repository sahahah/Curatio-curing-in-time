import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender_email, receiver_email, subject, message, app_password):
    # Encode subject and message to ASCII, ignore characters that cannot be encoded
    subject = subject.encode('ascii', 'ignore').decode('ascii')
    message = message.encode('ascii', 'ignore').decode('ascii')

    # Setup the email
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())

# Usage example
sender_email = 'kvzui.fx@gmail.com'
receiver_email = 'sahasrini@gmail.com'
subject = 'Subject with non-ASCII characters: Café'
message = 'Message with non-ASCII characters: Café'
app_password = 'fejt grzm lchr iloq'
send_email(sender_email, receiver_email, subject, message, app_password)
print('hi')
