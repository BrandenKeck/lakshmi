from data_loader import data_loader

class lakshmi():

    def __init__(self):
        self.data_loader = data_loader()

ll = lakshmi()
ll.data_loader.init_players()
len(ll.data_loader.players)
ll.data_loader.dump_all_players()

ll.data_loader.players = []
ll.data_loader.players[10].position

xx = ll.data_loader.db.get_node(f'player_data/')
xx['8482078']
ll.data_loader.retrieve_all_players()

#ll.data_loader.init_skater(8471675, [20192020, 20202021, 20212022])
#ll.data_loader.cross_skater_metrics(8471675)
