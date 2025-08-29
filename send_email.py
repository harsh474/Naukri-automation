import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Email configuration
sender_email = "harshrajput1101@gmail.com"       # yaha apna gmail likho
receiver_email = "princerajput69425@gmail.com"     # yaha jisko mail bhejna hai uska gmail likho
password = "azrl vgyj urvp pgal"

# Create the email content
subject = "Test Email"
body = "Hello, this is a test email sent from Python!"

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = receiver_email
message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

# SMTP Gmail server
with smtplib.SMTP("smtp.gmail.com", 587) as server:
    server.starttls()  # Upgrade the connection to secure encrypted SSL/TLS
    server.login(sender_email, password)  # Login to your email account
    server.send_message(message)  # Send the email

print("Email sent successfully!")
