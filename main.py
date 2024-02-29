from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somerandomKey'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

#Communication between server and client
@socketio.on('message')
def handle_message(message):
    print('received message: ' + message + '\n')
    socketio.emit('message', message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json) + '\n')
    socketio.emit('json', json)

#Rooms
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', to=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', to=room)
    
#When the server is run __name__ is set to __main__
if __name__ == '__main__':
    socketio.run(app)