from helpers import load_json_array, is_config_json_valid
import datetime as dt
from typing import List, Dict
from sim.person.hobby import hobby

CONF = None

class config:
    def __init__(self, config_json_path, hobbies_json_path):

        json = load_json_array(config_json_path)
        JSON_valid, errors = is_config_json_valid(json)
        if (not JSON_valid):
            print(errors)

        self.valid: bool = JSON_valid
        self.how_many_people_to_generate: int = json['generation']['how_many_people_to_generate']
        self.recursive_relationship_limit: int = json['generation']['recursive_relationship_limit']
        self.start_date: dt.datetime = dt.datetime(json['start_date']['year'], json['start_date']['month'], json['start_date']['day'])

        self.city_sizex: int = json['city_sizex']
        self.city_sizey: int = json['city_sizey']
        self.city_sizez: int = json['city_sizez']

        self.hobbies: Dict[str, hobby] = setHobbies(load_json_array(hobbies_json_path))

def setHobbies(hobbies_json):
    hobby_list: Dict[str, hobby] = {}
    for name, attributes in hobbies_json.items():
        hobby_instance = hobby(
            name,
            attributes.get('openness'),
            attributes.get('conscientiousness'),
            attributes.get('neuroticism'),
            attributes.get('extraversion'),
            attributes.get('agreeableness'),
            attributes.get('min_age'),
            attributes.get('max_age'),
            attributes.get('injury_rating'),
            attributes.get('mean_IQ'),
            attributes.get('mean_creativity')
        )
        hobby_list[name]=hobby_instance
    return hobby_list

def createCONF(config_json_path, hobbies_json_path):
    global CONF
    CONF = config(config_json_path, hobbies_json_path)





