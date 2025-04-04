import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# AURA Credentials
a="MS_SwopOy@trial-vywj2lpr7pm47oqz.mlsender.net"
b="jageraura@gmail.com"
c="mssp.diOzlkd.v69oxl5wqprl785k.vapdSuH"

# Email details
sender_email = a
receiver_email = b
password = c
smtp_server = "smtp.mailersend.net"
smtp_port = 587

# Create the email content
message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = "AURA"

# Email body
body = "¥"
message.attach(MIMEText(body, "plain"))

# Send the email
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Secure the connection
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, message.as_string())
    print("Email sent successfully!")
except Exception as e:
    print(f"Failed to send email. Error: {e}")
finally:
    server.quit()
