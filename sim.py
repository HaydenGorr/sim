import sys
import os
import json
from sim.person.person import Person, link_2_people_in_relationship
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

    j = 0
    for i in range(Pn):

        if j >= Pn: break

        if (add_current_relationship or add_past_relationship):
            if (add_current_relationship):
                newPerson = Person(firstName=FN[j], lastName=LN[j], age=people[first].age + random.uniform(-5, 5), male_sex=not people[first].male_sex)
                people.append(newPerson)
                
                link_2_people_in_relationship(newPerson, people[first], people[first].relationship[0])

                add_current_relationship = False

                j+=1
                if (j >= Pn): break


            if (add_past_relationship):
                newPerson = Person(firstName=FN[j], lastName=LN[j], age=people[first].age + random.uniform(-5, 5), male_sex=not people[first].male_sex)
                people.append(newPerson)
                people[first].pastMarraiges[1] = people[-1]
                newPerson.pastMarraiges[0] = people[first].pastMarraiges[0]
                newPerson.pastMarraiges[1] = people[first]

                add_past_relationship = False

                j+=1
                if (j >= Pn): break
        else:
            newPerson = Person(firstName=FN[j], lastName=LN[j], age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=random.choice([True, False]))
            people.append(newPerson)

            if (newPerson.relationship[0] != "single"):
                # gap_person = newPerson
                add_current_relationship = True
                first = j

            if (newPerson.pastMarraiges[0] != "no change"):
                # past_gap = newPerson
                add_past_relationship = True
                first = j

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
