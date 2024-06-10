from helpers import load_json_array, is_config_json_valid
import datetime as dt

CONF = None

class config:
    def __init__(self, path):
        json = load_json_array(path)
        JSON_valid, errors = is_config_json_valid(json)
        if (not JSON_valid):
            print(errors)

        self.valid = JSON_valid
        self.how_many_people_to_generate = json['generation']['how_many_people_to_generate']
        self.recursive_relationship_limit = json['generation']['recursive_relationship_limit']
        self.start_date = dt.datetime(json['start_date']['year'], json['start_date']['month'], json['start_date']['day'])





def createCONF(path):
    global CONF
    CONF = config(path)





