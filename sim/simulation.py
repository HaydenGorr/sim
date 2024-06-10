import sim.population_distributions as popDist
from config import CONF, config
from helpers import generate_names
from sim.person.person_utils import link_2_people_in_relationship, check_person_has_past_marraige, check_person_has_current_relationship, remove_past_marraige, remove_relationship, define_past_marriage
from sim.person.person import Person
import random
import numpy as np

def generate_people():
    how_many_people_to_generate = CONF.how_many_people_to_generate

    popDist.initialise(population_size=how_many_people_to_generate)

    FN, LN = generate_names(how_many_people_to_generate)

    people = []
    link_relationships = []
    links = 0 # this counts the number of times we've had to generate a person to fill a relationship in a row. To avoid long lines of people who have dated each other we limit this
    link_limit = CONF.recursive_relationship_limit

    j = 0
    for i in range(how_many_people_to_generate):

        if j >= how_many_people_to_generate: break

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

        newPerson = Person(firstName=FN[j%len(FN)], lastName=LN[j%len(FN)], age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=random.choice([True, False]))
        assert(newPerson.relationship is not None)
        people.append(newPerson)
        
        if check_person_has_past_marraige(newPerson): link_relationships.append([j, 'PM'])
        if check_person_has_current_relationship(newPerson): link_relationships.append([j, 'CR'])

        j+=1
        if (j >= how_many_people_to_generate): break


    age = []
    for j in people:  # Looping through the range of how_many_people_to_generate
        print(j.age)
        age.append(j.age)


    # Step 1: Count the frequencies
    # frequency = collections.Counter(age)

    # # Step 2: Visualize the frequencies
    # plt.figure(figsize=(10, 6))
    # plt.bar(frequency.keys(), frequency.values(), color='skyblue')
    # plt.xlabel('Numbers')
    # plt.ylabel('Frequency')
    # plt.title('Frequency of Numbers in Array')
    # plt.xticks(list(frequency.keys()))
    # plt.grid(axis='y')

    # # Show the plot
    # plt.show()