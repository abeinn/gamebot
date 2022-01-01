import serial

UP_HEIGHT = 61
DOWN_HEIGHT = 59.5
DEFAULT_SPEED = 10000

class Printer():

    def __init__(self, PrinterCOM):
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = DEFAULT_SPEED
        self.printerSerial = serial.Serial(PrinterCOM, 115200)
        self.printerSerial.write("G28\n".encode())
        self.printerSerial.write("G00 F{} Z{}\n".format(DEFAULT_SPEED, UP_HEIGHT).encode())

    def move(self, x, y):
        command = "G00 F{} X{} Y{}\n".format(self.speed, x, y)
        self.printerSerial.write(command.encode())
        self.x = x
        self.y = y

    def movez(self, x, y, z):
        command = "G00 F{} X{} Y{} Z{}\n".format(self.speed, x, y, z)
        self.printerSerial.write(command.encode())
        self.x = x
        self.y = y
        self.z = z

    def adjust(self, dx, dy, dz):
        x = self.x + dx
        y = self.y + dy
        z = self.z + dz
        self.movez(x, y, z)
        self.x = x
        self.y = y
        self.z = z


    def up(self):
        self.movez(self.x, self.y, UP_HEIGHT)

    def down(self):
        self.movez(self.x, self.y, DOWN_HEIGHT)

    def tap(self):
        self.down()
        self.up()

    def reset(self):
        self.up()
        self.move(145, 65)
        self.down()