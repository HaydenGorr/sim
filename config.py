from helpers import load_json_array, is_config_json_valid
import datetime as dt

CONF = None

class config:
    def __init__(self, config_json_path, hobbies_json_path):

        json = load_json_array(config_json_path)
        JSON_valid, errors = is_config_json_valid(json)
        if (not JSON_valid):
            print(errors)

        self.valid = JSON_valid
        self.how_many_people_to_generate = json['generation']['how_many_people_to_generate']
        self.recursive_relationship_limit = json['generation']['recursive_relationship_limit']
        self.start_date = dt.datetime(json['start_date']['year'], json['start_date']['month'], json['start_date']['day'])

        self.hobbies = setHobbies(load_json_array(hobbies_json_path))

class hobby:
    def __init__(self, name, op, co, ne, ex, ag, min_age, max_age, injury_rating, mean_IQ, mean_creativity):
        self.name = name
        self.op = op
        self.co = co
        self.ne = ne
        self.ex = ex
        self.ag = ag
        self.min_age = min_age
        self.max_age = max_age
        self.injury_rating = injury_rating
        self.mean_IQ = mean_IQ
        self.mean_creativity = mean_creativity

def setHobbies(hobbies_json):
    hobby_list = {}
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





