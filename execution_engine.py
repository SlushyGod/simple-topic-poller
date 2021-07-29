"""
Creates two execution engines that send similar data
"""
from threading import Thread, Lock
import zmq

context = zmq.Context()

def start_execution_engine(id, port):
    """
    Start the execution engine and send data whenever the broker is ready
    """
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://localhost:{}'.format(port))
    print('Connecting REQ socket to port {}'.format(port))

    mod_val = id + 1 # Just used to add some variance in the topic
    for i in range(20000):
        topic = b'strace' if (i % mod_val == 0) else b'ftrace'
        data = b'Execution-' + str(id).encode('utf-8') + b': ' + str(i).encode('utf-8')
        message = topic + b'\x00' + data
        socket.send(message)
        print('Sent message: {}'.format(message.decode('utf-8')))

        message = socket.recv() # Ack that broker is ready for more data

if __name__ == '__main__':
    ee1_port = 5000
    ee2_port = 5010
    ee1_thread = Thread(target = start_execution_engine, args = (1, ee1_port, ))
    ee2_thread = Thread(target = start_execution_engine, args = (2, ee2_port, ))
    ee1_thread.start()
    ee2_thread.start()