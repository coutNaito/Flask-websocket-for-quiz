from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somerandomKey'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message + '\n')
    socketio.emit('message', message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json) + '\n')
    socketio.emit('json', json)

if __name__ == '__main__':
    socketio.run(app)