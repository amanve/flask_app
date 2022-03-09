from flask import Flask, render_template
from flask_mail import Mail, Message
from flask_mail import *

app = Flask(__name__)

app.config['TESTING'] = True
app.config['SECRET_KEY'] = 'mysecret!'

app.config['MAIL_SERVER'] = 'localhost'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TSL'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = None
app.config['MAIL_PASSWORD'] = None
app.config['MAIL_DEFAULT_SENDER'] = None
app.config['MAIL_MAX_EMAILS'] = 5
app.config['MAIL_SUPPRESS_SEND'] = True
app.config['MAIL_ASCII_ATTACHMENTS'] = False

mail = Mail(app)


@app.route('/')
def index():
  msg = Message('Hello World this is a flask mail!',
                sender='myname@e-mail.com',
                recipients=['to@e-mail.com'])
  mail.send(msg)
  return render_template('index.html')


def log_message(msg, app):
  app.logger.debug(msg.subject)


email_dispatched.connect(log_message)

if __name__ == '__main__':
  app.run()
