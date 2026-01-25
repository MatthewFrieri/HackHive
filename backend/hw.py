import serial

class ESP:

    def __init__(self, players):
        self.players = players
        self.esp32 = serial.Serial(port='COM6', baudrate=115200)  # COM port might need to be changed
        
    def deal_preflop(self, offset):
        for _ in range(self.players):
            self.deal(2)
            self.turn(30)
    
    def deal_n(self, n):
        self.deal(n)

    def turn(self, angle):
        # Command robot rotation angle (0-270 degs)
        command = f't{angle}'
        command = command.encode("utf-8")
        #print(command)
        self.esp32.write(command)

    def deal(self, cards_num):
        # Command robot to deal "cards_num" number of cards (0-270 degs)
        command = f'd{cards_num}'
        command = command.encode("utf-8")
        #print(command)
        self.esp32.write(command)
