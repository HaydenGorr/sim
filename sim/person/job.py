from typing import Tuple

class job:
    def __init__(self, location, name, op, co, ne, ex, ag, min_age, max_age, injury_rating, mean_IQ, IQ_slope, mean_creativity, creativity_slope, promotional_ladder, entry_pay, highest_rung_pay):
        self.name: str = name
        self.location: tuple[int, int] = location

        self.op: int = op
        self.co: int = co
        self.ne: int = ne
        self.ex: int = ex
        self.ag: int = ag
        self.min_age: int = min_age
        self.max_age: int = max_age
        self.injury_rating: int = injury_rating
        self.mean_IQ: int = mean_IQ
        self.IQ_slope: int = IQ_slope
        self.mean_creativity: int = mean_creativity
        self.creativity_slope: int = creativity_slope
        self.promotional_ladder: list[str] = promotional_ladder
        self.entry_pay: int = entry_pay
        self.highest_rung_pay: int = highest_rung_pay




















    "Software Developer": {
        "openness": 85,
        "conscientiousness": 75,
        "neuroticism": -1,
        "extraversion": -1,
        "agreeableness": -1,
        "min_age": 22,
        "max_age": 65,
        "injury_rating": 5,
        "mean_IQ": 105,
        "IQ_slope": 5,
        "mean_creativity": 100,
        "creativity_slope": 4,
        "promotional_ladder": ["Junior Developer", "Developer", "Senior Developer", "Lead Developer", "Chief Technology Officer"],
        "entry_pay": 30000,
        "highest_rung_pay": 120000
    },