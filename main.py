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
def handle_json(data):
    room = data['room']
    answer = data['answer']
    print('received json: ' + str(data) + '\n')
    socketio.emit('json', data, room=room)

@socketio.on('Anouncement')
def handle_announcement(data):
    room = data['room']
    print('received announcement: ' + data + '\n')
    socketio.emit('Anouncement', data, room=room)

#Rooms
@socketio.on('join')
def on_join(data):
    username = data['username']
    room = data['room']
    join_room(room)
    send(username + ' has entered the room.', room=room)

@socketio.on('leave')
def on_leave(data):
    username = data['username']
    room = data['room']
    leave_room(room)
    send(username + ' has left the room.', room=room)
    

#When the server is run __name__ is set to __main__
if __name__ == '__main__':
    socketio.run(app)