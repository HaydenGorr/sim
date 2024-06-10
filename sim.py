import sys
import os
import json
from sim.person.person import Person, link_2_people_in_relationship, define_past_marriage
import random
import sim.population_distributions as popDist
import numpy as np
import datetime as dt
from sim.person.person_utils import check_person_has_current_relationship, check_person_has_past_marraige, remove_past_marraige, remove_relationship

START_DATE = dt.datetime(1997, 1, 1)

def load_json_array(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

def generate_names(Pn):
    # Load the JSON arrays
    first_names = load_json_array(os.path.join('resources', 'first_names.json'))
    last_names = load_json_array(os.path.join('resources', 'last_names.json'))

    random_first_names = random.sample(first_names, min(Pn, len(first_names))) 
    random_last_names = random.sample(last_names, min(Pn, len(last_names))) 

    return random_first_names, random_last_names

def main(Pn=5):

    popDist.initialise(population_size=Pn)

    FN, LN = generate_names(Pn)

    people = []
    link_relationships = []
    links = 0 # this counts the number of times we've had to generate a person to fill a relationship in a row. To avoid long lines of people who have dated each other we limit this
    link_limit = 3

    j = 0
    for i in range(Pn):

        if j >= Pn: break

        if (link_relationships):
            for k in link_relationships:
                link_index = k[0]
                if (k[1] == "CR"):

                    relationship_type = people[link_index].relationship[0]

                    newly_created_person = Person(firstName=FN[j%len(FN)], lastName=LN[j%len(FN)], age=people[link_index].age + random.uniform(-5, 5), male_sex=not people[link_index].male_sex)
                    people.append(newly_created_person)

                    link_2_people_in_relationship(newly_created_person, people[link_index], relationship_type)
                    
                    # Check if the person we've just made has a past relatinoship, because we'll need to make someone to be in their past relationship
                    if (check_person_has_past_marraige(newly_created_person)):
                        if (links < link_limit):
                            link_relationships.append([j, "PM"])
                            links+=1
                        else:
                            remove_past_marraige(newly_created_person)
                            
                    j+=1

                elif (k[1] == "PM"):

                    what_happened_to_the_relationship = people[link_index].pastMarraiges[0]
                    
                    if (what_happened_to_the_relationship == "widowed"):
                        people[link_index].pastMarraiges[1] = None
                        continue

                    newly_created_person = Person(firstName=FN[j%len(FN)], lastName=LN[j%len(FN)], age=people[link_index].age + random.uniform(-5, 5), male_sex=not people[link_index].male_sex)
                    people.append(newly_created_person)

                    define_past_marriage(people[-1], people[link_index], what_happened_to_the_relationship)

                    if (check_person_has_current_relationship(newly_created_person)):
                        if (links < link_limit):
                            link_relationships.append([j, "CR"])
                            links+=1
                        else:
                            remove_relationship(newly_created_person)
                            
                    j+=1
                    
            link_relationships = []
            continue
        
        links = 0

        newPerson = Person(firstName=FN[j], lastName=LN[j], age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=random.choice([True, False]))
        assert(newPerson.relationship is not None)
        people.append(newPerson)
        
        if check_person_has_past_marraige(newPerson): link_relationships.append([j, 'PM'])
        if check_person_has_current_relationship(newPerson): link_relationships.append([j, 'CR'])

        j+=1
        if (j >= Pn): break


    for j in people:  # Looping through the range of Pn
        print(j.age)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        peopleNumber = int(sys.argv[1])  # Convert the first argument to an integer
    else:
        peopleNumber = 100
    main(peopleNumber)
