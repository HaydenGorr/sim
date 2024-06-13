from helpers import load_json_array, is_config_json_valid
import datetime as dt
from typing import List, Dict
from sim.person.hobby import hobby
from sim.person.job import MASTER_JOB

CONF = None

class config:
    def __init__(self, config_json_path, hobbies_json_path, jobs_json_path):

        json = load_json_array(config_json_path)
        JSON_valid, errors = is_config_json_valid(json)
        if (not JSON_valid):
            print(errors)

        self.valid: bool = JSON_valid
        self.how_many_people_to_generate: int = json['generation']['how_many_people_to_generate']
        self.recursive_relationship_limit: int = json['generation']['recursive_relationship_limit']
        self.start_date: dt.datetime = dt.datetime(json['start_date']['year'], json['start_date']['month'], json['start_date']['day'])
        self.current_date: dt.datetime = dt.datetime(json['start_date']['year'], json['start_date']['month'], json['start_date']['day'])

        self.city_sizex: int = json['city_sizex']
        self.city_sizey: int = json['city_sizey']
        self.city_sizez: int = json['city_sizez']

        self.hobbies: Dict[str, hobby] = {name: hobby(name, attributes) for name, attributes in load_json_array(hobbies_json_path).items()}
        self.jobs: Dict[str, MASTER_JOB] = {name: MASTER_JOB(name, attributes) for name, attributes in load_json_array(jobs_json_path).items()}

        self.retirement_age: int = json['retirement_age']

    def increment_date(self):
        self.current_date += dt.timedelta(days=1)


def createCONF(config_json_path, hobbies_json_path, jobs_json_path):
    global CONF
    CONF = config(config_json_path, hobbies_json_path, jobs_json_path)





