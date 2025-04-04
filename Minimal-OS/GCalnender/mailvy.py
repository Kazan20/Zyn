import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import pygame

# Email client configuration
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_password"

# Initialize pygame for sound playback
pygame.mixer.init()

def send_email(recipient_email, subject, body):
    # Set up the MIME structure
    message = MIMEMultipart()
    message['From'] = SENDER_EMAIL
    message['To'] = recipient_email
    message['Subject'] = subject

    # Add body to the email
    message.attach(MIMEText(body, 'plain'))

    # Send the email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.sendmail(SENDER_EMAIL, recipient_email, message.as_string())
        server.quit()
        print("Email sent successfully!")

        # Play the "You got mail!" sound
        pygame.mixer.music.load('you_got_mail.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print(f"Failed to send email: {e}")

if __name__ == "__main__":
    recipient = "recipient_email@gmail.com"
    subject = "Test Email"
    body = "This is a test email."

    send_email(recipient, subject, body)
