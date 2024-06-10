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

def define_past_marriage(p1, p2, what_happened_to_the_relationship):
    p1.setPastMarriage(what_happened_to_the_relationship, p2)
    p2.setPastMarriage(what_happened_to_the_relationship, p1)
