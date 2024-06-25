import os
from config import createCONF
createCONF(os.path.join('config.json'), os.path.join('resources', 'hobbies.json'), os.path.join('resources', 'jobs.json'))
from sim.simulation import generate_people, match_people, generate_decased_partners
from config import CONF
import sys
import os
from helpers import relationship_linking_sanity_check, print_a_person
from sim.person.person_utils import calculate_relationship_strength, check_promotion_level_fit

def simulation_loop(all_people, limit):
    for x in range(0, limit):
        for person in all_people:
            what_happened = person.simulate_day()










if __name__ == "__main__":
    if (not CONF.valid):
        print("Config file is not valid")
        exit()

    if len(sys.argv) > 1:
        peopleNumber = int(sys.argv[1])  # Convert the first argument to an integer
        CONF.generation.how_many_people_to_generate = peopleNumber

    all_people, age_buckets, big5_buckets, widowers = generate_people()
    deceased_people = generate_decased_partners(widowers)
    match_people(all_people, age_buckets, big5_buckets)
    calculate_relationship_strength(all_people)
    relationship_linking_sanity_check(all_people)

    for person in all_people: person.updateHappyness()

    limit = 100
    simulation_loop(all_people, limit)

    check_promotion_level_fit(all_people[23], all_people[23].job.master_job, all_people[23].job.current_rung+1)

    pass
