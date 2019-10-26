from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
from PyQt5.uic import loadUi

import arduino_communication

import sys

class connect_dial_box(QWidget):    #dialog box class

    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.ui = loadUi('GUI/dial.ui', self)

        self.COMportlineEdit = self.ui.COMportlineEdit
        self.connect_button = self.ui.connect_button
        self.connect_button.clicked.connect(self.check_if_can_connect)
        self.parent.dial = True

    def check_if_can_connect(self):
        port = self.COMportlineEdit.text()
        if (self.parent.ard_com.connect(port)):
            self.connect()
        else:
            self.COMportlineEdit.setText("Can't connect")

    def connect(self):
        self.close()
        self.parent.set_ui()

    def closeEvent(self, event):
        self.parent.dial = False

class Nerf_App(QWidget):    #main window class

    def __init__(self):
        super().__init__()

        self.ui = loadUi('GUI/nerf_turret.ui', self)  #read UI file
        self.show()     #display window


        self.COM_port = ""         #com port to connect to arduino
        self.dial = False          #set true when dial windows is open
        self.connected = False     #set true when connected to arduino
        self.motor_on = False      #set true to turn motor on
        self.shoot = False         #set true to shoot
        self.x = 0.5               #x value 0-253 range
        self.y = 0.5               #y value 0-253 range
        self.on_pad = False        #set true when cursor is oer pad
        self.ard_com = arduino_communication.com_ard(self)  #create object handling communication with arduino

        self.pad_label = self.ui.pad_label                  #pad reference created from ui file
        self.bluetooth_button = self.ui.bluetooth_button    #bluetooth button reference created from ui file
        self.motor_on_button = self.ui.motor_on_button      #motor button reference created from ui file

        self.bluetooth_button.clicked.connect(self.connect_dial_box)   #connect bluettoth button to connect dial box methor
        self.motor_on_button.clicked.connect(self.motor_on_off)     #connect motor button to motor_on_off method


    def connect_dial_box(self):    #create connection dialog box
        if not self.connected and not self.dial:
            dial_box = connect_dial_box(self)
            dial_box.show()

    def set_ui(self):  #enable buttons and pad when conencted
        self.motor_on_button.setEnabled(True)
        self.pad_label.setEnabled(True)
        new_button_img = QIcon('GUI/bluetooth_connect.png')
        self.bluetooth_button.setIcon(new_button_img)


    def motor_on_off(self):    #turn motor on/off
        if self.connected:
            self.motor_on = self.motor_on_button.isChecked()
            self.set_arduino_message()


    def mouseMoveEvent(self, event):
        if (69<event.x()<551 and 69<event.y()<551):   #check if cursor is over the pad , I should create just for that but I am too lazy
            self.x = int(self.remap(event.x(), 0, 253, 70, 550))
            self.y = int(self.remap(event.y(), 0, 253, 70, 550))
            self.on_pad = True
        else:
            self.on_pad = False
            self.shoot = False

        self.set_arduino_message()

    def mousePressEvent(self, event):
        if self.on_pad and self.motor_on:
            self.shoot = True
            self.set_arduino_message()

    def mouseReleaseEvent(self, event):
        if self.on_pad:
            self.shoot = False
            self.set_arduino_message()

    def set_arduino_message(self):
        if self.connected:
            message = bytes([255, self.x, self.y, self.motor_on,self.shoot, 254])
            #self.ard_com.ser.write(message)
            self.ard_com.ser.write(message)

    def remap(self, value_to_map, new_range_min, new_range_max, old_range_min, old_range_max):

        remapped_val = (value_to_map - old_range_min) * (new_range_max - new_range_min) / (
                    old_range_max - old_range_min) + new_range_min

        if (remapped_val > new_range_max):
            remapped_val = new_range_max
        elif (remapped_val < new_range_min):
            remapped_val = new_range_min

        return remapped_val


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Nerf_App()
    app.exec_()
    #sys.exit(app.exec_())