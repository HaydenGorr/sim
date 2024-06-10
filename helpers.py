import json

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