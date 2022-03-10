from flask import Flask, render_template, jsonify, request
from flask_mail import Mail, Message
import flask_mail 

app = Flask(__name__)

app.config['TESTING'] = False
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

'''
@app.route('/')
def index():
  msg = Message()
  msg.subject='Hello World this is a flask mail!'
  msg.sender=("Me", "me@example.com")
  #assert msg.sender == "Me <me@example.com>"
  msg.recipients=['to@e-mail.com','test@e-mail.com','me@e-mail.com']
  msg.body="test mail"
  msg.html="<h1>testing flask mail</h1>"
  
  mail.send(msg)
  return render_template('index.html')
'''

@app.route('/')
def index():
  msg = Message()
  msg.subject='Hello World this is a flask mail!'
  msg.sender=("Me", "me@example.com")
  #assert msg.sender == "Me <me@example.com>"
  msg.recipients=['to@e-mail.com','test@e-mail.com','me@e-mail.com']
  msg.body="test mail"
  msg.html="<h1>testing flask mail</h1>"
 
  mail.send(msg)
  
  return {'Message':msg.subject,'Sender':msg.sender}


def log_message(msg, app):
  app.logger.debug(msg.subject)
  app.logger.debug(msg.sender)
  app.logger.debug(msg.html)
  app.logger.debug(msg.recipients)
  app.logger.debug(msg.body)


flask_mail.email_dispatched.connect(log_message)

if __name__ == '__main__':
  app.run()
