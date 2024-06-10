import sim.population_distributions as popDist
from config import CONF, config
from helpers import generate_names
from sim.person.person_utils import link_2_people_in_relationship, check_person_has_past_marraige, check_person_has_current_relationship, remove_past_marraige, remove_relationship, link_2_people_in_past_marraige
from sim.person.person import Person
import random
import numpy as np

def generate_people():
    how_many_people_to_generate = CONF.how_many_people_to_generate

    popDist.initialise(population_size=how_many_people_to_generate)

    FN, LN = generate_names(how_many_people_to_generate)

    people = []
    link_relationships = []

    # What are links?
    #
    #   When we generate someone we randomly decide if they've been in a relationship or not.
    #   If they are in or have been in a relatinoship we need to generate a "link" - a person
    #   who they will link to for their current or past relationship. We have to do this recursively.
    #
    #   If we need a "link" to fill a relationship, that link may have had a past marraige that we need
    #   to link, and that past marraige partner may have a current relationship which needs linking, and on and on.
    #   But we limit this potentioally infinite recursion with the vars: links and link_limit
    #
    #   links is the var that counts how many times we've had to create a "link" in succession
    #   and link_limit will stop this recusion once links hits the limit.
    #
    links = 0
    link_limit = CONF.recursive_relationship_limit

    j = 0

    while(j < how_many_people_to_generate):

        for LR in link_relationships:
            link_index = LR[0]
            type = LR[0]

            # Generate someone
            newly_created_person = Person(firstName=FN[j%len(FN)], lastName=LN[j%len(FN)], age=people[link_index].age + random.uniform(-5, 5), male_sex=not people[link_index].male_sex)
            people.append(newly_created_person)

            if (type == "CR"):
                relationship_type = people[link_index].relationship[0]
                link_2_people_in_relationship(newly_created_person, people[link_index], relationship_type)

                # if we've reached maximum links then stop the links here
                if (links >= link_limit): remove_past_marraige(newly_created_person)
                # If we have space for more links, then let's create a new person for this link next loop
                elif check_person_has_past_marraige(newly_created_person):
                    link_relationships.append([j, "PM"])
                    links+=1

                j+=1

            elif (type == "PM"):
                what_happened_to_the_relationship = people[link_index].pastMarraiges[0]
                link_2_people_in_past_marraige(newly_created_person, people[link_index], what_happened_to_the_relationship)

                # if we've reached maximum links then stop the links here
                if (links >= link_limit): remove_relationship(newly_created_person)
                # If we have space for more links, then let's create a new person for this link next loop
                elif check_person_has_current_relationship(newly_created_person):
                    link_relationships.append([j, "CR"])
                    links+=1

                j+=1

        # reset links
        link_relationships = []
        links = 0

        newPerson = Person(firstName=FN[j%len(FN)], lastName=LN[j%len(FN)], age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=random.choice([True, False]))
        assert(newPerson.relationship is not None)
        people.append(newPerson)
        
        #
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