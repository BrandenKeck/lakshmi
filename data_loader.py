import requests
import numpy as np
from datetime import date, datetime

# NHL Data Class - Using the Official API
class data_loader():

    # Init constructor
    def __init__(self):
        self.db = firebase_connection()


    # Get current roster
    def get_games(self):

        # Establish current date
        today = date.today()
        yr = today.year
        mo = '{:02d}'.format(today.month)
        dy = '{:02d}'.format(today.day)

        # Extract API Data
        req_url = f'https://statsapi.web.nhl.com/api/v1/schedule?startDate={yr}-{mo}-{dy}&endDate={yr}-{mo}-{dy}'
        api_res = requests.get(req_url).json()
        games = api_res["dates"][0]["games"]

        # Massage into a useful object
        game_data = dict()
        for game in games:
            away_name = game["teams"]["away"]["team"]["name"]
            home_name = game["teams"]["home"]["team"]["name"]
            idx = f'{yr}-{mo}-{dy} {away} @ {home}'.replace(".", "")
            game_data[idx] = {
                "away": {
                    "name": away,
                    "roster": self.get_roster(game["teams"]["away"]["team"]["id"]),
                },
                "home": {
                    "name": home,
                    "roster": self.get_roster(game["teams"]["home"]["team"]["id"])
                }
            }

        # Return Game Data
        self.db.set_node("/game_data", game_data)


    def get_roster(self, team_id):

        # Extract API Data
        req_url = f'https://statsapi.web.nhl.com/api/v1/teams/{team_id}/?expand=team.roster'
        api_res = requests.get(req_url).json()
        players = api_res["teams"][0]["roster"]["roster"]

        # Massage into a useful object
        player_data = []
        for player in players:
            player_data.append({
                "name": player["person"]["fullName"],
                "id": player["person"]["id"],
                "position": player["position"]["type"]
            })

        return player_data

    def init_skater(self, skater_id, seasons):

        # Extract API Data
        games = []
        for season in seasons:
            req_url = f'https://statsapi.web.nhl.com/api/v1/people/{skater_id}/stats?stats=gameLog&season={season}'
            api_res = requests.get(req_url).json()
            games = games + api_res["stats"][0]["splits"]

        # Massage into a useful object
        last_game = "NA"
        norm_goals = []
        norm_pm = []
        player_stats = dict()
        games_bkwd = list(reversed(games))
        for game in games_bkwd[:len(games_bkwd)]:

            # Basic game stats
            date = game["date"]
            is_home = game["isHome"]
            toi = self.toi_to_minutes(game["stat"]["timeOnIce"])
            goals = game["stat"]["goals"]
            pm = game["stat"]["plusMinus"]

            # Running arrays
            norm_goals = self.array_runner(norm_goals, goals/toi, 10)
            norm_pm = self.array_runner(norm_pm, pm/toi, 10)

            # Player data
            player_stats[game["game"]["gamePk"]]
            player_stats[game["game"]["gamePk"]] = {
                "date": date,
                "toi": toi,
                "goals": goals,
                "plusminus": pm,
                "goals_per_toi": goals/toi,
                "plusminus_per_toi": pm/toi,
                "normalized_goals": {
                    "last_03": np.mean(norm_goals[:3]) if len(norm_goals) >=3 else "NA",
                    "last_04": np.mean(norm_goals[:4]) if len(norm_goals) >=4 else "NA",
                    "last_05": np.mean(norm_goals[:5]) if len(norm_goals) >=5 else "NA",
                    "last_06": np.mean(norm_goals[:6]) if len(norm_goals) >=6 else "NA",
                    "last_07": np.mean(norm_goals[:7]) if len(norm_goals) >=7 else "NA",
                    "last_08": np.mean(norm_goals[:8]) if len(norm_goals) >=8 else "NA",
                    "last_09": np.mean(norm_goals[:9]) if len(norm_goals) >=9 else "NA",
                    "last_10": np.mean(norm_goals[:10]) if len(norm_goals) >=10 else "NA"
                },
                "normalized_pm": {
                    "last_03": np.mean(norm_pm[:3]) if len(norm_pm) >=3 else "NA",
                    "last_04": np.mean(norm_pm[:4]) if len(norm_pm) >=4 else "NA",
                    "last_05": np.mean(norm_pm[:5]) if len(norm_pm) >=5 else "NA",
                    "last_06": np.mean(norm_pm[:6]) if len(norm_pm) >=6 else "NA",
                    "last_07": np.mean(norm_pm[:7]) if len(norm_pm) >=7 else "NA",
                    "last_08": np.mean(norm_pm[:8]) if len(norm_pm) >=8 else "NA",
                    "last_09": np.mean(norm_pm[:9]) if len(norm_pm) >=9 else "NA",
                    "last_10": np.mean(norm_pm[:10]) if len(norm_pm) >=10 else "NA"
                },
                "opp_norm_pm": {
                    "last_03": "NA",
                    "last_04": "NA",
                    "last_05": "NA",
                    "last_06": "NA",
                    "last_07": "NA",
                    "last_08": "NA",
                    "last_09": "NA",
                    "last_10": "NA"
                },
                "oppgoal_norm_saves": {
                    "last_03": "NA",
                    "last_04": "NA",
                    "last_05": "NA",
                    "last_06": "NA",
                    "last_07": "NA",
                    "last_08": "NA",
                    "last_09": "NA",
                    "last_10": "NA"
                },
                "oppgoal_norm_ga": {
                    "last_03": "NA",
                    "last_04": "NA",
                    "last_05": "NA",
                    "last_06": "NA",
                    "last_07": "NA",
                    "last_08": "NA",
                    "last_09": "NA",
                    "last_10": "NA"
                },
                "is_home": int(is_home),
                "last_game": "NA" if last_game=="NA" else self.delta_date(date, last_game),
                "opp_last_game": "NA"
            }

            # set last date
            last_game = date

        # Return Game Data
        self.db.set_node(f'/player_data/{skater_id}', player_stats)


    def cross_skater_metrics(self, skater_id):

        # Import skater data
        staker_data = self.db.set_node(f'/player_data/{skater_id}')
        print(staker_data)

    def init_goalie(self, goalie_id):
        pass

    def cross_goalie_metrics(self, goalie_id):
        pass

    def get_level3_goalie_metrics(self, goalie_id):
        pass

    def toi_to_minutes(self, toi):
        min, sec = toi.split(":")
        real_toi = float(min) + float(sec)/60
        return real_toi

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
        cred = credentials.Certificate('service_key.json')
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
