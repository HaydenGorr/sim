import sim.population_distributions as popDist
from config import CONF, config
from helpers import load_json_array
from sim.person.person_utils import link_2_people_in_relationship, check_person_has_past_marraige, check_person_has_current_relationship, remove_past_marraige, remove_relationship, link_2_people_in_past_marraige
from sim.person.person import Person
import random
import numpy as np
import bisect
import names
import os

age_ranges = [18, 21, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 100]
big5_traits = ["openness", "conscientiousness", "extraversion", "agreeableness", "neuroticism"]

def generate_people():
    hobby_master_list = load_json_array(os.path.join('resources', 'hobbies_exp.json'))
    how_many_people_to_generate = CONF.how_many_people_to_generate

    popDist.initialise(population_size=how_many_people_to_generate)

    widowed = [] # store refs to widowers here so we can generate deceased partners later
    people = []
    big5_buckets = {trait: {age: [] for age in age_ranges} for trait in big5_traits}
    age_buckets = {18: [], 21: [], 25: [], 30: [], 35: [], 40: [], 45: [], 50: [], 55: [], 60: [], 65: [], 70: [], 75: [], 80: [], 85: [], 90: [], 100: []}

    for x in range(CONF.how_many_people_to_generate):
        is_male = random.choice([True, False])
        newPerson = Person(firstName=names.get_first_name('male' if is_male else 'female'), lastName=names.get_first_name('male' if is_male else 'female'), age=np.random.choice(popDist.AGE_DIST, size=1), male_sex=is_male)

        random_selection = random.sample(list(hobby_master_list.items()), k=random.randint(1, 5))
        newPerson.addHobbies(random_selection)

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

        if (check_person_has_past_marraige(newPerson) and newPerson.pastMarraiges[0] == "widowed"):
            widowed.append(newPerson)

    return people, age_buckets, big5_buckets, widowed

# I thought the recusion wasn't important any more after several refactors, but don't remove the recusion,
# it facilitates link limiting, where we ensure more that a relationship chain of people dating and breaking up
# doesn't go on forever. Removing recusion means there can be an arbritrarily long chain of people dating
# Person a dates person b who dates person c who dated person d and on and on, that's a relationship chain
def recursive_match(person, big_5_key, age_key, big5_buckets, age_buckets, continuous_linking, past):

    if (continuous_linking >= CONF.recursive_relationship_limit): 
        if (past): remove_past_marraige(person)
        else: remove_relationship(person)
        return
    
    if (past and check_person_has_past_marraige(person) and person.pastMarraiges[0] == "widowed"): return

    # We need to store this because we reassign big_5_key under some conditions. Bad code, I know
    original_big_5_key = big_5_key

    # Adjust for neurotic people
    # If the person is neurotic, they'll want someone understanding and conscientious
    if (big_5_key == "neuroticism"): big_5_key = "conscientiousness"

    # If we're not searching past 
    big5_searchable_containers = [big_5_key]

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
        random.shuffle(bucket_search_order)
        big_5_key = random.choice(big5_traits)
        big5_searchable_containers = ["conscientiousness", "openness", "extraversion", "agreeableness", "neuroticism"]
        random.shuffle(big5_searchable_containers)

    matched = False
    currently_searching_age_bucket_index = None

    for currently_searching_age_bucket_index in bucket_search_order:
        for big5 in big5_searchable_containers:
            currently_searching_bucket = big5_buckets[big5][currently_searching_age_bucket_index]
            for p in currently_searching_bucket:
                if p.male_sex == person.male_sex: continue
                if p is person: continue
                if not past and not check_person_has_current_relationship(p): continue # looking for current relationship and the person isn't in a relationship
                if (past and not check_person_has_past_marraige(p)): continue # if looking for past marraige partner and person hasn't had a past marraige
                if (not past and p.relationship[1] is not None): continue # if looking for current relationship and the person hsa already had a relationship set
                if (past and p.pastMarraiges[1] is not None): continue # if looking for past marraige partner and the person has already had a past marraige set

                if not past: link_2_people_in_relationship(person, p, person.relationship[0])
                else: link_2_people_in_past_marraige(person, p, person.pastMarraiges[0])

                value, name = p.getMostProminentBig5()
                if not past and check_person_has_past_marraige(p) and p.pastMarraiges[0] != "widowed":
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

def match_people(people, age_buckets, big5_buckets):
    for big_5_key, big_5_bucket in big5_buckets.items():
         for age_key, age_bucket in big_5_bucket.items():
             for person in age_bucket:
                if check_person_has_current_relationship(person) and person.relationship[1] is None:
                    recursive_match(person, big_5_key, age_key, big5_buckets, age_buckets, 0, False)
                if check_person_has_past_marraige(person) and person.pastMarraiges[1] is None and person.pastMarraiges[0] != "widowed":
                    recursive_match(person, big_5_key, age_key, big5_buckets, age_buckets, 0, True)

def generate_decased_partners(widowed_people):
    deceased_people = []
    for widower in widowed_people:
        if (widower.pastMarraiges[0]!="widowed"): continue
        dead_person = Person(firstName=names.get_first_name('female' if widower.male_sex else 'male'), lastName=names.get_first_name('female' if widower.male_sex else 'male'), age=widower.age + (random.choice(range(-5, 5))), male_sex=not widower.male_sex)
        dead_person.alive = False
        remove_relationship(dead_person)
        link_2_people_in_past_marraige(widower, dead_person, "widowed")
        deceased_people.append(dead_person)

    return deceased_people

