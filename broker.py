"""
Simple broker that establishes connection with an "execution engine" and an "analysis engine"
Note: Because this is just a simple script, the dynamic connection with the analysis engine
    is assumed to be added through another channel
"""
from threading import Thread, Lock
import time
import zmq

context = zmq.Context()

# Establish connection with execution engines
ee1_socket = context.socket(zmq.REP)
ee2_socket = context.socket(zmq.REP)
ee1_socket.bind("tcp://*:5000")
ee2_socket.bind("tcp://*:5010")
print('Binded execution engines sockets to port 5000 and 5010')

# The sockets will be created dynamically as a consumer connects to the broker
# There should be some sortve timeout for recving an ack back to remove dead consumers
ae1_socket = context.socket(zmq.REQ)
ae2_socket = context.socket(zmq.REQ)
ae1_socket.connect("tcp://localhost:6000")
ae2_socket.connect("tcp://localhost:6010")
print('Connected analysis engines sockets to port 6000 and 6010')

# Assume you create this object through req/repl sockets on init
topic_channels = {
  'strace': [ae1_socket, ae2_socket],
  'ftrace': [ae1_socket]
}

# Mutex to control send_topic function call
mutex = Lock()

# Would normally use dealer sockets instead of request
def send_topic(b_topic, b_message):
    """
    Sends a topic to all analysis engines that want the data and waits for their reply
    """
    sockets = topic_channels[b_topic.decode('utf-8')]
    for socket in sockets:
        try:
            socket.send(b_topic + b'\x00' + b_message)
            message = socket.recv()
        except:
            # Call exception for timeout error, if it timeouts then remove the consumer
            print('error')

def start_execution_engine_pull(socket):
    """
    Start pulling data from the execution engine and send them when they can
    """
    while True:
        message = socket.recv()
        b_topic, b_message = message.split(b'\x00', 1)
        print('Topic: {}, Message: {}'.format(b_topic, b_message))

        mutex.acquire()
        try:
            send_topic(b_topic, b_message)
        finally:
            mutex.release()

        socket.send(b'reply') # Pull Data

if __name__ == '__main__':
    ee1_thread = Thread(target = start_execution_engine_pull, args = (ee1_socket,))
    ee2_thread = Thread(target = start_execution_engine_pull, args = (ee2_socket,))
    ee1_thread.start()
    ee2_thread.start()
