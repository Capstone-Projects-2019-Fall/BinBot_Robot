class Treads:
    def __init__(self):
        pass

    def execute(self, list):
        for e in list:
            self.turn(e["angle"])
            self.forward(e["distance"])

    def turn(self, angle):
        print("Treads turned " + angle + " degrees.")

    def forward(self, distance):
        print("Moved " + distance + " meters forward.")