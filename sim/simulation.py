import sim.population_distributions as popDist
from config import CONF, config
from helpers import generate_names
from sim.person.person_utils import link_2_people_in_relationship, check_person_has_past_marraige, check_person_has_current_relationship, remove_past_marraige, remove_relationship, link_2_people_in_past_marraige
from sim.person.person import Person
import random
import numpy as np
import bisect

age_ranges = [18, 21, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100]
big5_traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

def generate_people():
    how_many_people_to_generate = CONF.how_many_people_to_generate

    popDist.initialise(population_size=how_many_people_to_generate)

    FN, LN = generate_names(how_many_people_to_generate)

    people = []
    big5_buckets = {trait: {age: [] for age in age_ranges} for trait in big5_traits}

    age_buckets = {18: [], 21: [], 25: [], 30: [], 35: [], 40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [], 75: [], 80: [], 85: [], 90: [], 100: []}
    # big5_buckets = {"openness":[], "conscientiousness":[], "extraversion":[], "agreeableness":[], "neuroticism":[]}

    for x in range(CONF.how_many_people_to_generate):
        newPerson = Person(firstName=FN[x%len(FN)], lastName=LN[x%len(FN)], age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=random.choice([True, False]))

        people.append(newPerson)

        # We use the age and big5 buckets to facilitate relationship matching after
        # if the new person as no relationship, we don't need them in the buckets
        if (not check_person_has_current_relationship(newPerson) and not check_person_has_past_marraige(newPerson)): continue

        age_bucket_key = 0

        for idx, key in enumerate(age_buckets):
            if (newPerson.age <= key):
                age_bucket_key = key
                age_buckets[key].append(newPerson)
                break

        value, name = newPerson.getMostProminentBig5()
        big5_buckets[name][age_bucket_key].append(newPerson)

    return people, age_buckets, big5_buckets

def recursive_match(person, big_5_key, age_key, big5_buckets, age_buckets, continuous_linking, past):

    if (continuous_linking >= CONF.recursive_relationship_limit): 
        if (past): remove_past_marraige(person)
        else: remove_relationship(person)
        return

    original_big_5_key = big_5_key

    # Adjust for neurotic people
    # If the person is neurotic, they'll want someone understanding and conscientious
    if (big_5_key == "neuroticism"): big_5_key = "conscientiousness"

    bucket_indx = age_ranges.index(age_key)
    younger_bucket = age_ranges[bucket_indx - (1 if (bucket_indx > 1) else 0)]
    older_bucket = age_ranges[bucket_indx + (1 if (age_ranges.index(age_key) < 16) else 0)]
    if (past):
        younger_bucket2 = age_ranges[bucket_indx - (2 if (bucket_indx > 2) else 0)]
        older_bucket2 = age_ranges[bucket_indx + (2 if (age_ranges.index(age_key) < 15) else 0)]

    bucket_search_order = []
    # This simulates women looking for older men and men looking for younger women
    # The age gap is only by 1 bucket, so the dispersion of ages will never be huge
    if (person.male_sex): bucket_search_order = [age_key, younger_bucket, older_bucket]
    else: bucket_search_order = [age_key, older_bucket, younger_bucket]

    # past is true if the relationship we're matching was a past marraige
    # in this case, we look through a random personality bucket and less than 
    # ideal age buckets
    if (past):
        bucket_search_order.append(younger_bucket2)
        bucket_search_order.append(older_bucket2)
        bucket_search_order.reverse()
        big_5_key = random.choice(big5_traits)


    matched = False
    currently_searching_age_bucket_index = None

    for currently_searching_age_bucket_index in bucket_search_order:
        currently_searching_bucket = big5_buckets[big_5_key][currently_searching_age_bucket_index]
        for p in currently_searching_bucket:
            if p.male_sex == person.male_sex: continue
            if p is person: continue
            if not past and not check_person_has_current_relationship(p): continue
            if (past and not check_person_has_past_marraige(p)): continue

            if not past: link_2_people_in_relationship(person, p, person.relationship[0])
            else: link_2_people_in_past_marraige(person, p, person.pastMarraiges[0])

            value, name = p.getMostProminentBig5()
            if not past and check_person_has_past_marraige(p):
                recursive_match(p, name, currently_searching_age_bucket_index, big5_buckets, age_buckets, continuous_linking + 1, True)
            elif past and check_person_has_current_relationship(p):
                recursive_match(p, name, currently_searching_age_bucket_index, big5_buckets, age_buckets, continuous_linking + 1, False)

            matched = True

            break
        if matched: break

    if not matched:
        if not past: remove_relationship(person)
        else: remove_past_marraige(person)

        if check_person_has_current_relationship(person) and check_person_has_past_marraige(person): 
            big5_buckets[original_big_5_key][age_key].remove(person)
    
    if matched or not(check_person_has_current_relationship(person) and check_person_has_past_marraige(person)):
        try:
            big5_buckets[original_big_5_key][age_key].remove(person)
        except: pass
        
        try:
            big5_buckets[big_5_key][currently_searching_age_bucket_index].remove(p)
        except: pass




def match_people(people, age_buckets, big5_buckets):
    for big_5_key, big_5_bucket in big5_buckets.items():
         for age_key, age_bucket in big_5_bucket.items():
             for person in age_bucket:
                if check_person_has_current_relationship(person):
                    recursive_match(person, big_5_key, age_key, big5_buckets, age_buckets, 0, False)
                elif check_person_has_past_marraige(person):
                    recursive_match(person, big_5_key, age_key, big5_buckets, age_buckets, 0, True)

    pass

    age = []
    for j in people:  # Looping through the range of how_many_people_to_generate
        print(j.age)
        age.append(j.age)