import math
from typing import List
from sim.person.job import job
from datetime import datetime, timedelta
import random

def check_person_has_current_relationship(person):
    return person.relationship[0] != "single"

def check_person_has_past_marraige(person):
    return person.pastMarraiges[0] != "no change"

def remove_past_marraige(person):
    person.setPastMarriage("no change", None)
    
def remove_relationship(person):
    person.setRelationship("single", None)
    
def link_2_people_in_relationship(p1, p2, relationship_type):
    p1.setRelationship(relationship_type, p2)
    p2.setRelationship(relationship_type, p1)

def link_2_people_in_past_marraige(p1, p2, what_happened_to_the_relationship):
    p1.setPastMarriage(what_happened_to_the_relationship, p2)
    p2.setPastMarriage(what_happened_to_the_relationship, p1)

def calculate_relationship_strength(all_people):
    from config import CONF
    
    for person1 in all_people:
        if person1.relationship_strength != -1: continue 
        person2 = person1.relationship[1]
        if person2 is None: continue
    
        h_op = abs(person1.openness - person2.openness)
        h_co = abs(person1.conscientiousness - person2.conscientiousness)
        h_ne = abs(person1.neuroticism - person2.neuroticism)
        h_ex = abs(person1.extraversion - person2.extraversion)
        h_ag = abs(person1.agreeableness - person2.agreeableness)
        
        average_compatability = (h_op + h_co + h_ne + h_ex + h_ag) / 5
        iq_diff = abs(person1.iq - person2.iq)
        iq_modifier = math.floor(iq_diff/15) 
        
        common_hobbies = []
        for hobby in person1.hobbies:
            for hobby2 in person2.hobbies:
                if hobby[0] == hobby2[0]:
                    common_hobbies.append(hobby)

        expectation_diff = person1.expectations - person2.expectations > 0
        expectation_modifier = (expectation_diff/15)
                    
        #aggregated_compaitability = min(100, (100 - average_compatability) - (iq_modifier * 10) + (len(common_hobbies) * 5) + (-25 if len(common_hobbies) == 0 else 0))
        aggregated_compaitability = min(100, (100 - average_compatability) - (iq_modifier * 10) + (len(common_hobbies) * 5) + (expectation_modifier * 10))
        
        person1.relationship_strength = aggregated_compaitability
        person2.relationship_strength = aggregated_compaitability
        

# Tells us how much an activity suits the person's personality
# and how good the person is at it
# profeciency is determined by iq. 
# profeciency of 0 is average ability
# profeciency under 0 is under performing
# profeciency over 0 is high performing
def getProfeciencyAndEnjoyment(activityName, person, job_or_hobby):
    from config import CONF

    activity = CONF.hobbies[activityName] if job_or_hobby == "hobby" else CONF.jobs[activityName]
    
    h_op = abs(person.openness - activity.op) if activity.op != -1 else 0
    h_co = abs(person.conscientiousness - activity.co) if activity.co != -1 else 0
    h_ne = abs(person.neuroticism - activity.ne) if activity.ne != -1 else 0
    h_ex = abs(person.extraversion - activity.ex) if activity.ex != -1 else 0
    h_ag = abs(person.agreeableness - activity.ag) if activity.ag != -1 else 0
    i = 0
    if (h_op != 0): i += 1
    if (h_co != 0): i += 1
    if (h_ne != 0): i += 1
    if (h_ex != 0): i += 1
    if (h_ag != 0): i += 1
    # this calculates how aligned the activity is to their personality
    sum = h_op + h_co + h_ne + h_ex + h_ag
    
    enjoyment = abs(sum/i)

    # If you don't ejnoy it you won't be as good at it
    enjoyment_modifier = 0
    if (enjoyment < 35): enjoyment_modifier += -1

    # If you're very driven you get a +1 to profeciency
    if (person.expectations > 75) : enjoyment_modifier += 1
    
    # this calculates how many standard deviations away they are in IQ from the mean for this activity
    iq_difference = person.iq - activity.mean_IQ
    iq_std = 15
    iq_profeciency = math.ceil(iq_difference/iq_std)

    # this calculates how many standard deviations away they are in CREATIVITY from the mean for this activity
    creativity_difference = person.creativity - activity.mean_creativity
    creativity_std = 15
    creativity_profeciency = math.floor(creativity_difference/creativity_std)

    # If you're out of the age range the profeciency score is dramatically affected
    age_modifier = 0
    if (person.age < activity.min_age):
        age_modifier = (person.age - activity.max_age) * 0.20
    if (person.age > activity.max_age):
        age_modifier = (activity.max_age - person.age) * 0.20
    # ensure the age modifier is limited to -6
    age_modifier = max(-6, min(0, age_modifier))

    # If they really love the activity their profeciency improves
    activity_passion_modifier = 0
    if enjoyment <= 15:
        activity_passion_modifier = 1
        if enjoyment <= 5:
            activity_passion_modifier = 2

    # combine iq, creativity, and age and passion modifiers to an aggregated metric for profeciency
    aggregated_profeciency = ((iq_profeciency + creativity_profeciency) / 2) + age_modifier + activity_passion_modifier + enjoyment_modifier
    aggregated_profeciency = math.floor(max(-6, min(5, aggregated_profeciency)))

    # Determine the biggest modifier
    biggestModifier = []
    if (aggregated_profeciency < 0):
        biggestModifier = getBiggestNegativeModifier(iq_profeciency, creativity_profeciency, age_modifier, activity_passion_modifier)
    else:
        biggestModifier = getBiggestPositiveModifier(iq_profeciency, creativity_profeciency, age_modifier, activity_passion_modifier)

    return aggregated_profeciency, enjoyment, biggestModifier

def getBiggestNegativeModifier(iq_profeciency, creativity_profeciency, age_modifier, activity_passion_modifier):
    biggest_negative = ["iq_profeciency", iq_profeciency]
    if (creativity_profeciency < biggest_negative[1]): biggest_negative = ["creativity_profeciency", creativity_profeciency]
    if (age_modifier < biggest_negative[1]): biggest_negative = ["age_modifier", age_modifier]
    if (activity_passion_modifier < biggest_negative[1]): biggest_negative = ["activity_passion_modifier", activity_passion_modifier]
    return biggest_negative

def getBiggestPositiveModifier(iq_profeciency, creativity_profeciency, age_modifier, activity_passion_modifier):
    biggest_positive = ["iq_profeciency", iq_profeciency]
    if (creativity_profeciency > biggest_positive[1]): biggest_positive = ["creativity_profeciency", creativity_profeciency]
    if (age_modifier > biggest_positive[1]): biggest_positive = ["age_modifier", age_modifier]
    if (activity_passion_modifier > biggest_positive[1]): biggest_positive = ["activity_passion_modifier", activity_passion_modifier]
    return biggest_positive



# range is -5 to 5
def convert_profeciency_to_string(profeciency_score):
    if (profeciency_score == 3): return "excellent performance"
    if (profeciency_score == 2): return "great performance"
    if (profeciency_score == 1): return "good performance"
    if (profeciency_score == 0): return "average"
    elif (profeciency_score == -1): return "under performance"
    elif (profeciency_score == -2): return "bad performance"
    elif (profeciency_score == -3): return "terrible performance"
    elif (profeciency_score == -3): return "terrible performance"
    elif (profeciency_score == -6): return "incapable"

# Takes a person and a job and return which promotion they're ideal for
# This function is used to initialise the simulation and give everyone a
# starting promotion level
def find_ideal_promotion(person, job):
    from config import CONF
    
    for i in range(len(job.promotional_ladder)):

        result = check_promotion_level_fit(person, job, i)

        if (not result): return max(i-1, 0) # Return the index of the rung
    return len(job.promotional_ladder) - 1

# Takes person, job and the desired promotion level.
# Then checks if person is suitable for a promotion
def check_promotion_level_fit(person, job, promtion_level):
    adjustedIQ_req = job.mean_IQ + (promtion_level * job.IQ_slope)
    adjustedCreativity_req = job.mean_creativity + (promtion_level * job.creativity_slope)

    # this calculates how many standard deviations away they are in IQ from the mean for this activity
    iq_difference = person.iq - adjustedIQ_req
    iq_profeciency = math.ceil(iq_difference/15) # how many stdeviations from the required IQ are you

    # this calculates how many standard deviations away they are in CREATIVITY from the mean for this activity
    creativity_difference = person.creativity - adjustedCreativity_req
    creativity_profeciency = math.floor(creativity_difference/15) # how many stdeviations from the required creativity are you

    experience_modifier = 0
    if person.job:
        # num of years worked - years required for current promotion level.
        # We add 1 on the end beacuse if you meet the required experience you should get a positive modifier.
        # If we didn't +1 meeting the required experience would == 0.
        # Negative numbers are for when you're lacking experience
        experience_modifier = person.job.get_experience() - (person.job.master_job.promotion_curve * promtion_level+1) + 1

    result = math.floor(((iq_profeciency + creativity_profeciency) / 2) + (experience_modifier))

    return result >= 0


# Takes a person and gives you the job AND promotion they're suited for
def find_ideal_job(person):
    from config import CONF
    mostEnjoyed: List[str, int, str] = ["", -6, ""]
    mostProfecient: List[str, int, str] = ["", -6, ""]

    experience_modifier = 0

    for jobName, job in CONF.jobs.items():
        profeciency, enjoyment, reason_for_performance = getProfeciencyAndEnjoyment(jobName, person, "job")

        if enjoyment > mostEnjoyed[1]:
            mostEnjoyed = [jobName, enjoyment, reason_for_performance, profeciency]
        if profeciency > mostProfecient[1]:
            mostProfecient = [jobName, profeciency, reason_for_performance, enjoyment]

    if (mostEnjoyed[0] == mostProfecient[0]): return CONF.jobs[mostEnjoyed[0]]

    enjoyedJob = CONF.jobs[mostEnjoyed[0]]
    profecientJob = CONF.jobs[mostProfecient[0]]
    P_enjoyment, E_enjoyment = mostProfecient[3]/100, mostEnjoyed[1]/100
    P_profeciency, E_profeciency = mostProfecient[1]/100, mostEnjoyed[3]/100

    # How much you'll enjoy the job youre best at but won't enjoy the most
    # Adjusted for life expectations
    expectations = (person.expectations/2)/100 # Normalise to a 0 - 1 scale

    highest_pay_anywhere = 200000

    # how good is the pay compared to the heighest paying job in the city
    P_how_good_is_the_job = profecientJob.highest_rung_pay / highest_pay_anywhere
    E_how_good_is_the_job = enjoyedJob.highest_rung_pay / highest_pay_anywhere

    pay_diff = (E_how_good_is_the_job - P_how_good_is_the_job) / 2 # is positive E is better paid if negative P is better paid

    E_how_good_is_the_job -= ((1 - E_enjoyment) / 2) + (pay_diff if pay_diff > 0 else pay_diff) / 2
    P_how_good_is_the_job -= ((1 - P_enjoyment) / 2) + (pay_diff*-1 if pay_diff > 0 else abs(pay_diff)) / 2

    # If the job they enjoy more pays more too, just return that job
    if (E_how_good_is_the_job > P_how_good_is_the_job): return enjoyedJob
    else : return profecientJob


def generate_job_start_date(person, job:job):
    from config import CONF
    working_years = person.age-18

    # This simulates a person who switched jobs during their career.
    # Otherwise it would be as though person was working here since 18
    adjusted_working_years = working_years - random.randint(0, (working_years))

    job.start_date = CONF.start_date - timedelta(days=365*adjusted_working_years)




# 
def simulate_career_progression(person):
    from config import CONF
    if person.job is None: return


