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
-help

Commandos are written to the subjects, text is ignored!

Best regards,
BondMarket Mail Service 
_________________________________________

Hallo {name}

Ich bin der Maildienst der App BondMarket. Mit meiner Hilfe kannst du ganz einfach
Käufe von überall aus eingeben. Ich bestätige hiermit, dass deine Mail nicht
in Zukunft nicht mehr ignoriert wird!

__Liste der Befehle__

Neue Daten hinzufügen:
-Menge,Ort hinzufügen (bei Fließkommazahlen einen Punkt verwenden! z.B.: 10.55)

Benötigen Sie Hilfe?
-help

Befehle werden in die Fächer geschrieben, Text wird ignoriert!

Mit freundlichen Grüßen,
BondMarket Mail Dienst 
_________________________________________

Salut {name}

Je suis le service de messagerie de l'application BondMarket. Avec mon aide, vous pouvez facilement\
saisir des achats de n'importe où. Je confirme par la présente que votre courrier ne sera pas\
ignoré à l'avenir !

__Liste des commandes__

Ajouter de nouvelles données :
-add quantity,location (utilisez un point pour les nombres à virgule flottante ! ex. : 10.55)

Avez-vous besoin d'aide ?
-help

Les commandes sont écrites dans les sujets, le texte est ignoré !

Meilleures salutations,
Service courrier de BondMarket 
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


def confirmation_mail(receiver: str, name, amount, location, date, app_state: AppState):
    port = 587  
    server = app_state.settings["main_service"]["server"]
    username = app_state.settings["main_service"]["user"]
    sender_password = app_state.settings["main_service"]["psw"]
    smtp_server = f"smtp.{server}"

    message = f"""
Hey {name},

your Date: 
    amount: {amount}
    location; {location} 
    date: {date}
were added!

Best regards,
BondMarket Mail Service
"""
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = 'BondMarket Mail Service add Command'
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

Please check that the subject: BondMarket: login Your Name is written in the return.


Kind regards,

BondMarket Mail Service
 
"""
    
    msg = EmailMessage()
    msg.set_content(message)
    msg['Subject'] = f'BondMarket: login {name}'
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