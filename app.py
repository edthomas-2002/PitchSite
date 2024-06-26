from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit, disconnect
from time import sleep
import random
from threading import Thread, Event

from pitch_processing.pitch_extractor import PitchExtractor

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}})
socketio = SocketIO(app, cors_allowed_origins="*")

thread = Thread()
thread_stop_event = Event()

class DataThread(Thread):
    def __init__(self, pitch_extractor):
        self.delay = 0.01
        self.pitch_extractor = pitch_extractor
        super(DataThread, self).__init__()
    def dataGenerator(self):
        print("Initialising Data Stream to Frontend")
        try:
            while not thread_stop_event.is_set():
                pitch = float(self.pitch_extractor.get_latest_pitch())
                socketio.emit('responseMessage', {'pitch': pitch})
                sleep(self.delay)
        except KeyboardInterrupt:
            # kill()
            print("Keyboard  Interrupt")
    def run(self):
        self.dataGenerator()

# Handle the webapp connecting to the websocket
@socketio.on('connect')
def test_connect():
    print('someone connected to websocket')
    emit('responseMessage', {'data': 'Connected! ayy'})

# Handle the webapp sending a message to the websocket
@socketio.on('message')
def handle_message(message):
    print('Data', message["data"])
    print('Status', message["status"])
    global thread
    global thread_stop_event
    if (message["status"]=="On"):
        if not thread.is_alive():
            thread_stop_event.clear()
            print("Starting Data Thread")
            pe = PitchExtractor()
            pe.start_audio_processing()
            thread = DataThread(pe)
            thread.start()
    elif (message["status"]=="Off"):
        if thread.is_alive():
            thread_stop_event.set()
            thread.pitch_extractor.stop_audio_processing()
        else:
            print("Data Thread not alive")
    else:
        print("Unknown command")


@socketio.on_error_default  # handles all namespaces without an explicit error handler
def default_error_handler(e):
    print('An error occured:')
    print(e)

if __name__ == '__main__':
    socketio.run(app, debug=True, port=5001)
