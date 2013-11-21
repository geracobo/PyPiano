from serial import Serial

import time

import thread
from Queue import Queue



def arduino_thread(queue_in, queue_out):
    serial = None
    while True:

        # We check the arduino
        if serial != None:
            # Make sure an arduino is actually connected.
            try:
                serial.getDSR()
            except:
                serial = None
                queue_out.put("DISCONNECTED")
                continue

            data = serial.read()
            print data
                
        if not queue_in.empty():
            data_in = queue_in.get()
            if data_in == "CONNECT":
                try:
                    serial = Serial('/dev/ttyACM0', 9600)
                    serial.setTimeout(.1)
                    queue_out.put("CONNECTED")
                except:
                    print "Error connecting"
                    serial = None
            elif data_in == "DISCONNECT":
                try:
                    serial.close()
                    serial = None
                    queue_out.put("DISCONNECTED")
                except:
                    print "Error disconnecting"




class Arduino():
    # We receive information sent from the arduino on this queue.
    queue_in = Queue()
    # We send information to the arduino on this queue.
    queue_out = Queue()
    def __init__(self):
        # We flip the in/out because what goes out from here,
        # goes in on the thread.
        thread.start_new_thread(arduino_thread, (self.queue_out, self.queue_in))

    def connect(self):
        self.queue_out.put("CONNECT")

    def disconnect(self):
        self.queue_out.put("DISCONNECT")

    def get(self):
        try:
            return self.queue_in.get(False)
        except:
            return None

    def send(self, data):
        self.queue_out.put(data)


