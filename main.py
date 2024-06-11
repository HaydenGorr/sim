import os
from config import createCONF
createCONF(os.path.join('config.json'))
from sim.simulation import generate_people, match_people, generate_decased_partners
from config import CONF
import sys
import os
from helpers import relationship_linking_sanity_check


if __name__ == "__main__":
    if (not CONF.valid):
        print("Config file is not valid: " + error)
        exit()

    if len(sys.argv) > 1:
        peopleNumber = int(sys.argv[1])  # Convert the first argument to an integer
        CONF.generation.how_many_people_to_generate = peopleNumber

    people, age_buckets, big5_buckets, widowers = generate_people()
    deceased_people = generate_decased_partners(widowers)
    match_people(people, age_buckets, big5_buckets)

    relationship_linking_sanity_check(people)

    pass
