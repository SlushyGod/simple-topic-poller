"""
Creates two analysis engines that process data at two different speeds
"""
from threading import Thread, Lock
import time
import zmq

context = zmq.Context()

def start_analysis_engine(port, timeout = 0):
    """
    Start the analysis engine to process data and ack back when done performing "work"
    """
    socket = context.socket(zmq.REP)
    socket.bind('tcp://*:{}'.format(port))
    print('Binding REP socket to port {}'.format(port))

    while True: # Recv events and ack back
        message = socket.recv()
        print(message)
        time.sleep(timeout) # Perform "work"

        socket.send(b'ack')

if __name__ == '__main__':
    ae1_port = 6000
    ae2_port = 6010
    slow_consumer_timeout = .1 # Simulate work being done for slow consumer

    # Create the analysis engine threads
    ae1_thread = Thread(target = start_analysis_engine, args = (ae1_port, ))
    ae2_thread = Thread(target = start_analysis_engine, args = (ae2_port, slow_consumer_timeout, )) # Create a "slow" consumer

    # Start the threads
    ae1_thread.start()
    ae2_thread.start()