import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import datetime
import pandas as pd

data = datetime.datetime.now()
checaDia = data.day
checaMes = data.month
diaMes = str(checaDia) + "_" + str(checaMes) + ".csv"
filename = "Scrapper Pao de Ac " + diaMes
df1 = pd.read_csv(filename, encoding='latin-1')
df1 = df1.to_html()
filename = "Scrapper " + diaMes
df2 = pd.read_csv(filename, encoding='latin-1')
df2 = df2.to_html()

sender_email = "Scrapper.pda@gmail.com"  # Email de quem vai enviar
receiver_email = "lucasfowcosta@gmail.com"  # email de quem vai receber
password = input("Qual a senha do email de quem vai enviar: ")  # senha do email de quem vai enviar


message = MIMEMultipart("alternative")
message["Subject"] = "Preco Cerveja PdA e Adega"
message["From"] = sender_email
message["To"] = receiver_email

html = "<h3>Pao de açucar</h3>" + df1 + "<h3>Adega</h3>" + df2  # a msg do email

part = MIMEText(html, "html")
message.attach(part)

#  Criar uma conexão segura atraves do SSL com o sevidor e enviar o email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(
        sender_email, receiver_email, message.as_string()
    )
