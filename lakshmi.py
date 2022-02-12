from data_loader import data_loader

class lakshmi():

    def __init__(self):
        self.data_loader = data_loader()

    def get_todays_games(self):
        self.data_loader.get_games()

ll = lakshmi()
ll.data_loader.init_skater(8471675, [20192020, 20202021, 20212022])
