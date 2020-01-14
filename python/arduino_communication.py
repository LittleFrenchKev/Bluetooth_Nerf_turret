import serial

class com_ard():
    def __init__(self, parent):
        self.parent = parent
        print("ard created")


    def connect(self, port):
        try:
            self.ser = serial.Serial(port, 9600)
            self.parent.connected = True
            print("connected to arduino on port : ", port)
            return True
        except:
            print("Not able to connect on this port")
            return False

    def send_message(self, message):
        self.ser.write(message)
        print(message)
