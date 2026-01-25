import serial

class ESP:

    def __init__(self, num_players):
        self.num_players = num_players
        self.esp32 = serial.Serial(port='COM6', baudrate=115200)  # COM port might need to be changed
        
    def deal_preflop(self, start_pos):
        for i in range(self.num_players):
            pos = (i + start_pos) % self.num_players
            angle = pos * 180 / (self.num_players - 1)
            self.turn(angle)
            self.deal(2)
    
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
