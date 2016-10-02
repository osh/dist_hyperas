#!/usr/bin/env python
from flask import Flask, render_template
from flask_socketio import SocketIO
import client
import threading,time
app = Flask(__name__)
c = client.Client()
socketio = SocketIO(app)

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.tmpl')
    #return "Hello, World!"

@socketio.on('message')
def handle_message(message):
    print('received message: ' + message)

@socketio.on('json')
def handle_json(json):
    print('received json: ' + str(json))

@socketio.on('my event')
def handle_my_custom_event(json):
    print('received json: ' + str(json))

@socketio.on('devices')
def handle_my_custom_event(json):
    print('new devices connection: ' + str(json))

def runClient():
    while True:
        msg = c.rx_msg()
        print msg
        op = msg[0]
        if(op=="devices"):
            socketio.emit('devices', msg[1], broadcast=True)
        if(op=="tasks"):
            socketio.emit('tasks', msg[1], broadcast=True)

def poller():
    while True:
        print "requesting new stats ..."
        c.socket.send_json( ("req_devices",) )
        c.socket.send_json( ("req_tasks",) )
        time.sleep(1.0)

t1 = threading.Thread(target=runClient)
t1.start()
t2 = threading.Thread(target=poller)
t2.start()

socketio.run(app)
#app.run(debug=True)


