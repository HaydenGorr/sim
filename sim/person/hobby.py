class hobby:

    def __init__(self, name, attributes):
        self.name = name
        self.op = attributes.get('openness')
        self.co = attributes.get('conscientiousness')
        self.ne = attributes.get('neuroticism')
        self.ex = attributes.get('extraversion')
        self.ag = attributes.get('agreeableness')
        self.min_age = attributes.get('min_age')
        self.max_age = attributes.get('max_age')
        self.injury_rating = attributes.get('injury_rating')
        self.mean_IQ = attributes.get('mean_IQ')
        self.mean_creativity = attributes.get('mean_creativity')
