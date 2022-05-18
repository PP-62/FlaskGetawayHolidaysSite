from flask import Flask
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.yandex.ru'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'pormgmdfmbpcbomwevdrgmdvbnrt@yandex.ru'  # введите свой адрес электронной почты здесь
app.config['MAIL_DEFAULT_SENDER'] = 'pormgmdfmbpcbomwevdrgmdvbnrt@yandex.ru'  # и здесь
app.config['MAIL_PASSWORD'] = 'qwecxvrgthfjn'  # введите пароль
from app import routes