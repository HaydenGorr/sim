import sys
import os
import json
from sim.person.person import Person, link_2_people_in_relationship, define_past_marriage
import random
import sim.population_distributions as popDist
import numpy as np
import datetime as dt

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
    first = -1
    add_current_relationship = False
    add_past_relationship = None
    link_relationships = []

    j = 0
    for i in range(Pn):

        if j >= Pn: break

        if (link_relationships):
            for k in link_relationships:
                link_index = k[0]
                if (k[1] == "CR"):

                    relationship_type = people[link_index].relationship[0]

                    newly_created_person = Person(firstName=FN[j], lastName=LN[j], age=people[link_index].age + random.uniform(-5, 5), male_sex=not people[link_index].male_sex)
                    people.append(newly_created_person)

                    link_2_people_in_relationship(people[-1], people[link_index], relationship_type)
                    j+=1
                if (k[1] == "PR"):

                    what_happened_to_the_relationship = people[first].pastMarraiges[0]

                    newly_created_person = Person(firstName=FN[j], lastName=LN[j], age=people[link_index].age + random.uniform(-5, 5), male_sex=not people[link_index].male_sex)
                    people.append(newly_created_person)

                    define_past_marriage(people[-1], people[link_index], what_happened_to_the_relationship)
                    j+=1
            continue

        newPerson = Person(firstName=FN[j], lastName=LN[j], age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=random.choice([True, False]))
        people.append(newPerson)

        if (newPerson.relationship[0] != "single"):
            # gap_person = newPerson
            add_current_relationship = True
            first = j
            link_relationships.append(j, "CR")


        if (newPerson.pastMarraiges[0] != "no change"):
            # past_gap = newPerson
            add_past_relationship = True
            first = j
            link_relationships.append(j, "PR")

        j+=1
        if (j >= Pn): break


    for j in people:  # Looping through the range of Pn
        print(j.age)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        peopleNumber = int(sys.argv[1])  # Convert the first argument to an integer
    else:
        peopleNumber = 200
    main(peopleNumber)
