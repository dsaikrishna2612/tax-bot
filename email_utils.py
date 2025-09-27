from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def send_email(to_email, pdf_buffer, data):
    # --- Configure SMTP ---
    # Example for Gmail: replace with your credentials
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "dsaikrishna487@gmail.com"
    sender_password = "yxbl zepx bdws hwkh"

    import re
    # Basic email validation
    if not to_email or not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", to_email):
        raise ValueError(f"Invalid recipient email address: '{to_email}'")
    
    # Personalized subject using data
    subject=f"Income Tax Summary - {data['name']} (AY 2026-27)"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText("Please check your attached Summary of Income Tax details PDF.", 'plain'))
    part = MIMEApplication(pdf_buffer.read(), Name="tax_details.pdf")
    part['Content-Disposition'] = 'attachment; filename="tax_details.pdf"'
    msg.attach(part)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(sender_email, sender_password)
    server.send_message(msg)
    server.quit()
