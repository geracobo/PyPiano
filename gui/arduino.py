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

            data = serial.readline()

            if data == "C4\n": queue_out.put("C4")
            elif data == "D4\n": queue_out.put("D4")
            elif data == "E4\n": queue_out.put("E4")
            elif data == "F4\n": queue_out.put("F4")
            elif data == "G4\n": queue_out.put("G4")
            elif data == "A4\n": queue_out.put("A4")
            elif data == "B4\n": queue_out.put("B4")
            elif data == "C5\n": queue_out.put("C5")
            elif data == "D5\n": queue_out.put("D5")
            elif data == "E5\n": queue_out.put("E5")
            elif data == "F5\n": queue_out.put("F5")
            elif data == "G5\n": queue_out.put("G5")
            elif data == "A5\n": queue_out.put("A5")
            elif data == "B5\n": queue_out.put("B5")

        # Check commands
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

            if serial == None:
                continue

            print "Sending ", data_in

            if data_in == "+C4": serial.write('+C4')
            elif data_in == "+D4": serial.write('+D4')
            elif data_in == "+E4": serial.write('+E4')
            elif data_in == "+F4": serial.write('+F4')
            elif data_in == "+G4": serial.write('+G4')
            elif data_in == "+A4": serial.write('+A4')
            elif data_in == "+B4": serial.write('+B4')
            elif data_in == "+C5": serial.write('+C5')
            elif data_in == "+D5": serial.write('+D5')
            elif data_in == "+E5": serial.write('+E5')
            elif data_in == "+F5": serial.write('+F5')
            elif data_in == "+G5": serial.write('+G5')
            elif data_in == "+A5": serial.write('+A5')
            elif data_in == "+B5": serial.write('+B5')
            elif data_in == "-C4": serial.write('-C4')
            elif data_in == "-D4": serial.write('-D4')
            elif data_in == "-E4": serial.write('-E4')
            elif data_in == "-F4": serial.write('-F4')
            elif data_in == "-G4": serial.write('-G4')
            elif data_in == "-A4": serial.write('-A4')
            elif data_in == "-B4": serial.write('-B4')
            elif data_in == "-C5": serial.write('-C5')
            elif data_in == "-D5": serial.write('-D5')
            elif data_in == "-E5": serial.write('-E5')
            elif data_in == "-F5": serial.write('-F5')
            elif data_in == "-G5": serial.write('-G5')
            elif data_in == "-A5": serial.write('-A5')
            elif data_in == "-B5": serial.write('-B5')





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


