# Standard Imports
import json
import requests
import numpy as np

# Import Firebase / DB Keys
from firebase import Firebase

# Database Class (Using Google Firebase)
class hockeydb():

    # Init
    def __init__(self):

        # Get database config for connection
        with open('keys.json') as file:
            keys = json.load(file)

        # Establish connection
        self.db = Firebase(keys["config"]).database()

    # Handle data post
    def set_node(self, path):
        self.db.child(path).set(
            {"Test": 1234}
        )

    # Handle delete all
    def delete_node(self, path):
        self.db.child(path).remove()


hdb = hockeydb()
hdb.test_post()
#hdb.delete_all()

# REQUESTS:
#
# https://statsapi.web.nhl.com/api/v1/schedule
# https://statsapi.web.nhl.com/api/v1/schedule?startDate=2021-10-18&endDate=2021-12-20
# https://statsapi.web.nhl.com/api/v1/teams/
# https://statsapi.web.nhl.com/api/v1/teams/5/roster
# https://statsapi.web.nhl.com/api/v1/teams/1/?expand=team.roster
# https://statsapi.web.nhl.com/api/v1/people/8477404/stats?stats=statsSingleSeason&season=20202021
