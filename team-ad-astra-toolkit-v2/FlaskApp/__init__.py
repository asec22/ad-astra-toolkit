from flask import Flask, render_template, request
from flask_socketio import SocketIO
from random import random
from threading import Lock
from datetime import datetime
import time
from FlaskApp.package.pyduino2 import *


"""
Background Thread
"""
thread = None
thread_lock = Lock()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'donsky!'
socketio = SocketIO(app, cors_allowed_origins='*')

a=Arduino(serial_port='COM9')
time.sleep(3)

a.servo_attach(1,9)

a.sevenSeg_setup(1,3,4,2)

a.set_pin_mode(5,'O')

index1=0

"""
Get current date time
"""
def get_current_datetime():
    now = datetime.now()
    return now.strftime("%m/%d/%Y %H:%M:%S")

"""
Generate random sequence of dummy sensor values and send it to our clients
"""
def background_thread():
    print("Reading the Photoresistor..")
    while True:
        if index1==1:
            a.analog_write(5,0)
            svalue1 = int((a.analog_read(0)/1023)*180)
            socketio.emit('updateSensorData1', {'value1': svalue1,'date': get_current_datetime()})
            a.servo_write(1,svalue1)
            if svalue1 < 20:
                a.sevenSeg_write(9,0)
            elif svalue1 < 40:
                a.sevenSeg_write(9,1)
            elif svalue1 < 60:
                a.sevenSeg_write(9,2)
            elif svalue1 < 80:
                a.sevenSeg_write(9,3)    
            elif svalue1 < 100:
                a.sevenSeg_write(9,4)
            elif svalue1 < 120:
                a.sevenSeg_write(9,5)
            elif svalue1 < 140:
                a.sevenSeg_write(9,6)
            elif svalue1 < 160:
                a.sevenSeg_write(9,7)
            else:
                a.sevenSeg_write(9,8)
        if index1==2:
            svalue2 = int(((1023-a.analog_read(1))/1023)*255)
            socketio.emit('updateSensorData2', {'value2': svalue2,'date': get_current_datetime()})
            a.analog_write(5,svalue2)          
        else:
            a.analog_write(5,0)        
        socketio.sleep(2)
        

"""
Serve root index file
"""
@app.route('/',methods=["GET","POST"])
def index():
     # variables for template page (templates/index.html)
    global index1
    index1=0
    global pow_value1
    pow_value1="OFF"
    global pow_value2
    pow_value2 ="OFF"                    
                        

    # if we make a post request on the webpage aka press button then do stuff
    if request.method == 'POST':

        # if we press the turn on button
        if request.form['submit'] == 'Turn Off': 
            index1=0
            pow_value1 ="OFF"
            pow_value2="OFF"
                   
        # if we press the turn off button
        elif request.form['submit'] == 'Control Servo/Seven Segment':
            index1=1
            pow_value1="ON"
            pow_value2="OFF"

        elif request.form['submit'] == 'Light LED':
            index1=2
            pow_value1="OFF"
            pow_value2="ON"    

        else:
            pass
    
    # read in analog value from photoresistor
    # the default page to display will be our template with our template variables
    return render_template('index2.html',value1=pow_value1,index=index1,value2=pow_value2)        

"""
Decorator for connect
"""
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)

"""
Decorator for disconnect
"""
@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

if __name__ == '__main__':
    socketio.run(app)