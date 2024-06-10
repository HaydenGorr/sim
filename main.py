import os
from config import createCONF
createCONF(os.path.join('config.json'))
from sim.simulation import generate_people
from config import CONF
import sys
import os
if __name__ == "__main__":
    if (not CONF.valid):
        print("Config file is not valid: " + error)
        exit()

    if len(sys.argv) > 1:
        peopleNumber = int(sys.argv[1])  # Convert the first argument to an integer
        CONF.generation.how_many_people_to_generate = peopleNumber

    generate_people()
