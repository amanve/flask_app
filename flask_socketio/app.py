from flask import Flask
from flask_socketio import SocketIO

app = Flask(__name__)

app.config['SECRET_KEY'] = 'mysecret!'

if __name__ == '__main__':
  app.run()
