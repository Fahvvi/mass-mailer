import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase    
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders
import os
import csv

# Gmail account credentials
GMAIL_USERNAME = 'yourmail@gmail.com'
GMAIL_PASSWORD = 'xxxxxxx' #paste app password without spaces

# SMTP server settings
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587

# Folder path containing files to attach
FILE_FOLDER = r'C:\xx\xx\xx\File'

# CSV file path containing target email addresses
CSV_FILE = r'C:\xx\xx\xx\targets.csv'

# Function to send email with attachment
def send_email(subject, message, from_addr, to_addr, file_path):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg['Date'] = formatdate(localtime=True)

    # Attach file
    attachment = MIMEBase('application', 'octet-stream')
    attachment.set_payload(open(file_path, 'rb').read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', 'attachment; filename= "%s"' % os.path.basename(file_path))
    msg.attach(attachment)

    # Add message body
    msg.attach(MIMEText(message, 'plain'))

    # Send email
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(GMAIL_USERNAME, GMAIL_PASSWORD)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

# Read targets from CSV file
targets = []
with open(CSV_FILE, 'r') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        print(row)  # Add this line to see what's in the row list
        email, file_name = row[0].split(';')
        targets.append({'email': email, 'file_path': os.path.join(FILE_FOLDER, file_name)})

subject = 'Test'
message = 'Test email mass-mailer with attachments'

for target in targets:
    send_email(subject, message, GMAIL_USERNAME, target['email'], target['file_path'])
