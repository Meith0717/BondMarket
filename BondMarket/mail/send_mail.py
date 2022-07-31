import smtplib
import ssl
from email.message import EmailMessage
from app.app_state import AppState



def welcome_mail(receiver: str, name, app_state: AppState):
    port = 587  
    server = app_state.settings["main_service"]["server"]
    username = app_state.settings["main_service"]["user"]
    sender_password = app_state.settings["main_service"]["psw"]
    smtp_server = f"smtp.{server}"

    message = f"""
Hey {name}

I am the mail service of the app BondMarket. With my help, you can easily\
enter purchases from anywhere. I hereby confirm that your mail will not be\
ignored in the future!

__List of commands__

Add new data:
-add quantity,location (use a dot for floating point numbers! e.g.: 10.55)

Do you need help:
-help (not yet available)

Commandos are written to the subjects, text is ignored!

Best regards,
BondMarket Mail Service 
"""
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'Welcome to BondMarket Mail Service'
    msg['From'] = f"{username}@{server}"
    msg['To'] = receiver

    SSL_context = ssl.create_default_context()
    with smtplib.SMTP(smtp_server, port) as server:
        server.starttls(context=SSL_context)
        server.login(msg['From'], sender_password)
        server.sendmail(msg['From'], msg['To'], msg.as_string())


def login_mail(receiver: str, name, app_state: AppState):
    port = 587  
    server = app_state.settings["main_service"]["server"]
    username = app_state.settings["main_service"]["user"]
    sender_password = app_state.settings["main_service"]["psw"]
    smtp_server = f"smtp.{server}"

    message = f"""
Hey {name},

Please confirm your identity by simply returning this email.

Please check that the subject: "-login Your Name" is written in the return.


Kind regards,

BondMarket Mail Service
 
"""
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'-login {name}'
    msg['From'] = f"{username}@{server}"
    msg['To'] = receiver

    try:
        SSL_context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=SSL_context)
            server.login(msg['From'], sender_password)
            server.sendmail(msg['From'], msg['To'], msg.as_string())
        return True
    except:
        return False