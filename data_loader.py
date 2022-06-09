import json
import requests
import numpy as np
from datetime import date, datetime
from marshmallow import Schema, fields, post_load

def array_runner(self, arr, val, ll):
    arr.insert(0, val)
    if(len(arr) > ll):
        arr.pop()
    return arr

def delta_date(self, curr, last):
    a = datetime.strptime(curr, "%Y-%m-%d")
    b = datetime.strptime(last, "%Y-%m-%d")
    delta = a - b
    return delta.days


class match_up():

    def __init__(id):

        self.id = id

        # # Extract API Data
        # today = date.today()
        # yr = today.year
        # mo = '{:02d}'.format(today.month)
        # dy = '{:02d}'.format(today.day)
        # req_url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={yr}-{mo}-{dy}&endDate={yr}-{mo}-{dy}'
        # req_url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate=2021-09-02&endDate={yr}-{mo}-{dy}'
        # api_res = requests.get(req_url).json()
        # games = api_res["dates"][0]["games"]
        # len(games)

class player():

    def __init__(self, id, name, position, stats=dict()):

        self.id = id
        self.name = name
        self.position = position
        self.stats = stats

    def load_games(self, season):

        season = "20212022"
        id = "8465009"
        req_url = f'https://statsapi.web.nhl.com/api/v1/people/{id}/stats?stats=gameLog&season={season}'
        game_stats = requests.get(req_url).json()
        games = games + api_res["stats"][0]["splits"]
        for game in games:

            stats[game] = {
                "is_home": game["isHome"],
                "toi": self.toi_to_minutes(game["stat"]["timeOnIce"]),
                "goals": game["stat"]["goals"],
                "pm": game["stat"]["plusMinus"]
            }

    def toi_to_minutes(self, toi):
        min, sec = toi.split(":")
        real_toi = float(min) + float(sec)/60
        return real_toi

    def to_marshmallow(self):
        return player_schema().dump(self)

class player_schema(Schema):
    class Meta:
        fields = ('id', 'name', 'position', 'stats')

    @post_load
    def make_player(self, data, **kwargs):
        return player(**data)

    # def get_stats(self, game):
    #
    #     self.stats
    #
    #     req_url = f'https://statsapi.web.nhl.com/api/v1/people/{skater_id}/stats?stats=gameLog&season={season}'
    #     api_res = requests.get(req_url).json()
    #     games = games + api_res["stats"][0]["splits"]
    #
    #     # Basic game stats
    #     date = game["date"]
    #     is_home = game["isHome"]
    #     toi = self.toi_to_minutes(game["stat"]["timeOnIce"])
    #     goals = game["stat"]["goals"]
    #     pm = game["stat"]["plusMinus"]
    #
    #     # Running arrays
    #     norm_goals = self.array_runner(norm_goals, goals/toi, 10)
    #     norm_pm = self.array_runner(norm_pm, pm/toi, 10)
    #
    #     # Player data
    #     player_stats[game["game"]["gamePk"]]
    #     player_stats[game["game"]["gamePk"]] = {
    #         "date": date,
    #         "toi": toi,
    #         "goals": goals,
    #         "plusminus": pm,
    #         "goals_per_toi": goals/toi,
    #         "plusminus_per_toi": pm/toi,
    #         "normalized_goals": {
    #             "last_03": np.mean(norm_goals[:3]) if len(norm_goals) >=3 else "NA",
    #             "last_04": np.mean(norm_goals[:4]) if len(norm_goals) >=4 else "NA",
    #             "last_05": np.mean(norm_goals[:5]) if len(norm_goals) >=5 else "NA",
    #             "last_06": np.mean(norm_goals[:6]) if len(norm_goals) >=6 else "NA",
    #             "last_07": np.mean(norm_goals[:7]) if len(norm_goals) >=7 else "NA",
    #             "last_08": np.mean(norm_goals[:8]) if len(norm_goals) >=8 else "NA",
    #             "last_09": np.mean(norm_goals[:9]) if len(norm_goals) >=9 else "NA",
    #             "last_10": np.mean(norm_goals[:10]) if len(norm_goals) >=10 else "NA"
    #         },
    #         "normalized_pm": {
    #             "last_03": np.mean(norm_pm[:3]) if len(norm_pm) >=3 else "NA",
    #             "last_04": np.mean(norm_pm[:4]) if len(norm_pm) >=4 else "NA",
    #             "last_05": np.mean(norm_pm[:5]) if len(norm_pm) >=5 else "NA",
    #             "last_06": np.mean(norm_pm[:6]) if len(norm_pm) >=6 else "NA",
    #             "last_07": np.mean(norm_pm[:7]) if len(norm_pm) >=7 else "NA",
    #             "last_08": np.mean(norm_pm[:8]) if len(norm_pm) >=8 else "NA",
    #             "last_09": np.mean(norm_pm[:9]) if len(norm_pm) >=9 else "NA",
    #             "last_10": np.mean(norm_pm[:10]) if len(norm_pm) >=10 else "NA"
    #         },
    #         "opp_norm_pm": {
    #             "last_03": "NA",
    #             "last_04": "NA",
    #             "last_05": "NA",
    #             "last_06": "NA",
    #             "last_07": "NA",
    #             "last_08": "NA",
    #             "last_09": "NA",
    #             "last_10": "NA"
    #         },
    #         "oppgoal_norm_saves": {
    #             "last_03": "NA",
    #             "last_04": "NA",
    #             "last_05": "NA",
    #             "last_06": "NA",
    #             "last_07": "NA",
    #             "last_08": "NA",
    #             "last_09": "NA",
    #             "last_10": "NA"
    #         },
    #         "oppgoal_norm_ga": {
    #             "last_03": "NA",
    #             "last_04": "NA",
    #             "last_05": "NA",
    #             "last_06": "NA",
    #             "last_07": "NA",
    #             "last_08": "NA",
    #             "last_09": "NA",
    #             "last_10": "NA"
    #         },
    #         "is_home": int(is_home),
    #         "last_game": "NA" if last_game=="NA" else self.delta_date(date, last_game),
    #         "opp_last_game": "NA"
    #     }

# NHL Data Class - Using the Official API
class data_loader:

    # Init constructor
    def __init__(self):

        self.db = firebase_connection()
        self.players = []

    def init_players(self):

        teams_data = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams').json()
        for t in teams_data["teams"]:
            players_data = requests.get(f'https://statsapi.web.nhl.com/api/v1/teams/{t["id"]}/?expand=team.roster').json()
            for p in players_data["teams"][0]["roster"]["roster"]:
                self.players.append(player(p["person"]["id"], p["person"]["fullName"], p["position"]["type"]))

    def retrieve_all_players(self):

        self.players = []
        players_data = self.db.get_node(f'player_data/')
        for p_id in players_data:
            plyr = player_schema().make_player(players_data[p_id])
            self.players.append(plyr)

    def dump_all_players(self):

        for p in self.players:
            self.db.set_node(f'player_data/{p.id}', p.to_marshmallow())


# Custom Database Class (Using Google Firebase)
class firebase_connection():

    # Init constructor
    def __init__(self):

        # Import Firebase / DB Keys
        import json
        import firebase_admin
        from firebase_admin import credentials
        from firebase_admin import db
        self.db = db

        # Get database config for connection
        with open('api_info.json') as file:
            self.api_info = json.load(file)

        # Establish connection
        cred = credentials.Certificate("service_key.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': self.api_info['databaseURL']
        })

    # Handle data get
    def get_node(self, path):
        ref = self.db.reference(path)
        return ref.get()

    # Handle data post
    def set_node(self, path, data):
        ref = self.db.reference(path)
        ref.set(data)
