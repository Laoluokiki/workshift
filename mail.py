from fastapi import FastAPI, BackgroundTasks
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from config import settings

app = FastAPI()

def send_email(to_email, subject, body):
    # Set up SMTP server
    smtp_server = settings.smtp_server
    smtp_port = settings.smtp_port
    smtp_username = settings.smtp_username
    smtp_password = settings.smtp_password

    # Create message
    message = MIMEMultipart()
    message['From'] = smtp_username
    message['To'] = to_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))

    # Connect to SMTP server and send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.send_message(message)

# @app.post("/send-email/")
# async def send_plain_email(to_email: str, subject: str, body: str, background_tasks: BackgroundTasks):
#     background_tasks.add_task(send_email, to_email, subject, body)
#     return {"message": "Email will be sent shortly."}