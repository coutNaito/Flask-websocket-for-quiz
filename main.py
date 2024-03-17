from flask import Flask, render_template
from flask_socketio import SocketIO, join_room, leave_room, send

app = Flask(__name__)
app.config['SECRET_KEY'] = 'somerandomKey'
socketio = SocketIO(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/waiting_room')
def waiting_room():
    return render_template('waiting_room.html')

#Communication between server and client
#Broadcast to all clients on websocket
@socketio.on('message')
def handle_message(data):
    print('received message: ' + data + '\n')
    socketio.emit('message', data)

@socketio.on('json')
def handle_json(data):
    room = data['room']
    answer = data['answer']
    print('received json: ' + str(data) + '\n')
    socketio.emit('json', data, room=room)

#Rooms
@socketio.on('join')
def on_join(data):
    #Create Room for User
    username = data['username']
    room = data['room']
    join_room(room)
    with open('Quiz_session/Flask-websocket-for-quiz/templates/waiting_room.html', 'r') as f:
        new_content = f.read()
    socketio.emit('update_content', {'new_content': new_content})
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