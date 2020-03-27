
import smtplib
from email.message import EmailMessage

username = input("Enter your email address: ")
password = input("Enter the password: ")
email = EmailMessage()
email['from'] = input("Who is sending the email: ")
email['to'] = input("Enter the receiver email id: ")
email['subject'] = input("Please enter the subject: ")


text_msg = input("Enter the message you want to send: ")

email.set_content(text_msg)

#to make a smtp request
with smtplib.SMTP(host="smtp.gmail.com",port=587) as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login(username,password)
    smtp.send_message(email)
    print('..................message sent..........................')