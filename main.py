import os
from config import createCONF
createCONF(os.path.join('config.json'))
from sim.simulation import generate_people, match_people
from config import CONF
import sys
import os
from sim.person.person_utils import check_person_has_past_marraige, check_person_has_current_relationship


if __name__ == "__main__":
    if (not CONF.valid):
        print("Config file is not valid: " + error)
        exit()

    if len(sys.argv) > 1:
        peopleNumber = int(sys.argv[1])  # Convert the first argument to an integer
        CONF.generation.how_many_people_to_generate = peopleNumber

    people, age_buckets, big5_buckets, widowed = generate_people()
    match_people(people, age_buckets, big5_buckets)

    pass

    for person in people:
        if check_person_has_current_relationship(person):
            assert(person.relationship[1] is not None)

        if check_person_has_past_marraige(person) and person.pastMarraiges[0] != "widowed":
            assert(person.pastMarraiges[1] is not None)

    pass
