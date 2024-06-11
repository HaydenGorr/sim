import numpy as np
import sim.population_distributions as popDist
import datetime
import math
from dateutil.relativedelta import relativedelta
from config import CONF
from sim.person.person_utils import getProfeciencyAndEnjoyment

# age is a random float generated between 0 - 100
# we use the first 2 sig figs to get birth date
# and we use the decimals to decide where in the year
# the birthday is
def getBirthday(age):
    year_progress = age % 1
    Year = math.floor(age)
    dayOfYear = math.floor(year_progress * 365)
    # return datetime.datetime(CONF.start_date.year-Year, CONF.start_date.month, CONF.start_date.day) + datetime.timedelta(days=dayOfYear)
    adjusted_date = CONF.start_date.replace(year=CONF.start_date.year - Year)
    resulting_date = adjusted_date + datetime.timedelta(days=dayOfYear - 1)
    return resulting_date

def initialise_Relationship(person):
    age = person.age
    if (age<18):
        return person.setRelationship("single", None)

    P = [1.0, 0.0, 0.0]
    for age_range, probs in popDist.RELATIONSHIP_PROBS.items():
        if age_range[0] <= age <= age_range[1]:
            P = probs
    
    choice = np.random.choice([0, 1, 2], p=P)
    asd = ["single", "relationship", "marraige"]
    return person.setRelationship(asd[choice], None)

def isDivorced(age, agreeableness, openness):
    if (age < 18): return ["no change", None]

    P = [1.0, 0.0, 0.0]
    for age_range, probs in popDist.DIVORCED_PROBS.items():
        if age_range[0] <= age <= age_range[1]:
            P = probs
            break

    nothing, divorced, widowed = P

    agreeableness = agreeableness / 100
    openness = openness / 100

    agreeableness_factor = 1 - agreeableness  # Higher factor if less agreeable
    openness_factor = openness  # Higher factor if more open

    # Adjust the probabilities based on personality traits
    divorced_adjusted = divorced + (0.3 * agreeableness_factor) - (0.3 * openness_factor)
    nothing_adjusted = nothing - (0.3 * agreeableness_factor) + (0.3 * openness_factor)
    widowed_adjusted = widowed

    # Ensure probabilities remain within a valid range [0, 1]
    divorced_adjusted = max(0, min(1, divorced_adjusted))
    nothing_adjusted = max(0, min(1, nothing_adjusted))
    widowed_adjusted = max(0, min(1, widowed_adjusted))

    total = divorced_adjusted + nothing_adjusted + widowed_adjusted
    if total > 0:
        divorced_adjusted /= total
        nothing_adjusted /= total
        widowed_adjusted /= total
    else:
        divorced_adjusted = 0
        nothing_adjusted = 1
        widowed_adjusted = 0

    new_probabilities = [nothing_adjusted, divorced_adjusted, widowed_adjusted]

    return [np.random.choice(["no change", "divorced", "widowed"], p=new_probabilities), None]

class Person:

    def __repr__(self):
        return f"MyObject({self.age})"

    def __init__(self, firstName, lastName, age=-1, male_sex=False, alive=True):

        self.alive = alive

        # Personality
        self.openness = np.random.choice(popDist.generate_normal_dist(50, 25))
        self.conscientiousness = np.random.choice(popDist.generate_normal_dist(50, 25))
        self.extraversion = np.random.choice(popDist.generate_normal_dist(50, 30)) + (5 if male_sex else 0)
        self.agreeableness = np.random.choice(popDist.generate_normal_dist(50, 25)) + (0 if male_sex else 5)
        self.neuroticism = np.random.choice(popDist.generate_normal_dist(50, 15))

        # FACTS
        self.firstName = firstName
        self.lastName = lastName
        self.male_sex = male_sex
        self.birthday = getBirthday(age)
        self.age = abs(relativedelta(self.birthday, datetime.datetime(CONF.start_date.year, CONF.start_date.month, CONF.start_date.day))).years
        self.iq = math.floor(np.random.choice(popDist.IQ_DIST))
        self.creativity = math.floor(np.random.choice(popDist.IQ_DIST)) + (self.iq - 100) * 0.5 # adjusted by intelligence

        self.relationship = None
        initialise_Relationship(self) # 0=single, 1=relationship, 2=married
        assert(self.relationship is not None)

        self.relationship_strength = -1
        self.pastMarraiges = isDivorced(self.age, self.agreeableness, self.openness) # never divorced, divorced, widowed

        #LIKES
        self.hobbies = [] # list of hobbies

    def setRelationship(self, relationship, person):
        assert(relationship in ["single", "relationship", "marraige"])
        assert isinstance(person, Person) or person is None, "Argument must be an instance of Person or None"
        
        self.relationship = [relationship, person]

    def setPastMarriage(self, what_happened_to_the_relationship, person):
        assert(what_happened_to_the_relationship in ["no change", "divorced", "widowed"])
        assert isinstance(person, Person) or person is None, "Argument must be an instance of Person or None"
        self.pastMarraiges = [what_happened_to_the_relationship, person]

    def addHobbies(self, inHobbies):
        hobbies_to_add = []
        for hobbyName, hobbyData in inHobbies:
            profeciency, enjoyment, reason_for_performance = getProfeciencyAndEnjoyment(hobbyName, self)

            hobbies_to_add.append((hobbyName, profeciency, enjoyment))

        self.hobbies.extend(hobbies_to_add)
        
    def getMostProminentBig5(self):
        name = "openness"
        value = self.openness
        if (value < self.conscientiousness):
            value = self.conscientiousness
            name="conscientiousness"
        if (value < self.extraversion):
            value = self.extraversion
            name="extraversion"
        if (value < self.agreeableness):
            value = self.agreeableness
            name="agreeableness"
        if (value < self.neuroticism):
            value = self.neuroticism
            name="neuroticism"

        return value, name


# Define a function to adjust aggression based on age
def adjust_aggression_for_age(aggression, age):
    max_age = 80
    min_age = 18
    max_scale = 1.5
    min_scale = 0.5
    
    # Linear scaling factor
    scale_factor = max_scale - ((age - min_age) / (max_age - min_age)) * (max_scale - min_scale)
    
    return aggression * scale_factor

def link_2_people_in_relationship(p1, p2, relationship_type):
    p1.setRelationship(relationship_type, p2)
    p2.setRelationship(relationship_type, p1)

def define_past_marriage(p1, p2, what_happened_to_the_relationship):
    p1.setPastMarriage(what_happened_to_the_relationship, p2)
    p2.setPastMarriage(what_happened_to_the_relationship, p1)
