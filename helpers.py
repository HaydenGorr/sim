import json
import random
import os
from sim.person.person_utils import check_person_has_past_marraige, check_person_has_current_relationship, convert_profeciency_to_string

# This game uses a config file for basic generation
# ensure this runs on the config file before executing the simulation
def is_config_json_valid(config_json):
    try: 
        missing_list = []

        generation_config = config_json.get('generation', {})

        # Check for the required keys
        if 'how_many_people_to_generate' not in generation_config:
            missing_list.append("Missing key: 'generation.how_many_people_to_generate'")

        if 'recursive_relationship_limit' not in generation_config:
            missing_list.append("Missing key: 'generation.recursive_relationship_limit'")

        
        return True, missing_list
    except json.JSONDecodeError as e:
        return False, f"Invalid JSON: {e}"
    

def load_json_array(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

# Ensures that everyone who has a relationship has been linked to someone else
def relationship_linking_sanity_check(all_people):
    for person in all_people:
        if check_person_has_current_relationship(person):
            assert(person.relationship[1] is not None)

        if check_person_has_past_marraige(person):
            assert(person.pastMarraiges[1] is not None)

def print_a_person(person):
    print(f"Name: {person.firstName} {person.lastName}")
    print(f"Age: {person.age}")
    print(f"Gender: {'male' if person.male_sex else 'female'}")
    print(f"iq: {person.iq}")
    print(f"creativity: {person.creativity}")
    if (person.relationship[1] is not None and person.relationship[0] != 'single'):
        print(f"In a {person.relationship[0]} with: {person.relationship[1].firstName} {person.relationship[1].lastName if person.relationship[1].lastName is not None else ''}")
    if (person.pastMarraiges[1] is not None and person.pastMarraiges[0] != 'single'):
        print(f"Was in a {person.pastMarraiges[0]} with: {person.pastMarraiges[1].firstName} {person.pastMarraiges[1].lastName if person.relationship[1].lastName is not None else ''}")
    print(f"hobbies: {person.hobbies}")
    for hobby in person.hobbies:
        print(f"\t{hobby[0]}\t{convert_profeciency_to_string(hobby[1])}")






