from typing import Tuple, List
import math

# Contains base info about a job
class MASTER_JOB:
    def __init__(self, name, attributes):
        self.name: str = name
        self.op: int = attributes["openness"]
        self.co: int = attributes["conscientiousness"]
        self.ne: int = attributes["neuroticism"]
        self.ex: int = attributes["extraversion"]
        self.ag: int = attributes["agreeableness"]
        self.min_age: int = attributes["min_age"]
        self.max_age: int = attributes["max_age"]
        self.injury_rating: int = attributes["injury_rating"]
        self.mean_IQ: int = attributes["mean_IQ"]
        self.IQ_slope: int = attributes["IQ_slope"]
        self.mean_creativity: int = attributes["mean_creativity"]
        self.creativity_slope: int = attributes["creativity_slope"]
        self.promotional_ladder: list[str] = attributes["promotional_ladder"]
        self.current_rung: int = 0
        self.entry_pay: int = attributes["entry_pay"]
        self.highest_rung_pay: int = attributes["highest_rung_pay"]
        self.promotion_curve: int = attributes["promotion_curve"]
        self.pay_incriment: int = (self.highest_rung_pay - self.entry_pay) / len(self.promotional_ladder)
        self.pay_ladder: List[int] = [self.entry_pay + (self.pay_incriment * i) for i in range(len(self.promotional_ladder))]
        self.promotion_experience_equirement: List[int] = [self.entry_pay + (self.pay_incriment * i) for i in range(len(self.promotional_ladder))]

# Contains info about the job that a person has.
# A person is a assigned a job class not a masterjob
class job:
    def __init__(self, master_job: MASTER_JOB, start_date: int, end_date: int, profeciency: int, enjoyment: float, reason_for_performance: str):
        self.master_job: MASTER_JOB = master_job
        self.start_date: int = start_date
        self.days_since_promotion: int = start_date
        self.end_date: int = end_date
        self.current_rung: int = 0
        self.profecieny: int = profeciency
        self.enjoyment: float = enjoyment
        self.reason_for_performance: str = reason_for_performance
        self.current_pay: int = self.master_job.pay_ladder[self.current_rung]

    def get_experience(self):
        from config import CONF
        diff = CONF.current_date - self.start_date
        return math.floor(diff.days/356)

    def get_promotion_level(self):
        from config import CONF
        diff = CONF.current_date - self.start_date
        year_diff = diff.years
        promotion_level = math.floor(year_diff % self.master_job.promotion_curve)
        
        promotion_level = min(promotion_level, len(self.master_job.promotional_ladder)-1)

        if (promotion_level > self.current_rung):
            self.promote()
    
    def update_pay(self):
        self.current_pay = self.master_job.pay_ladder[self.current_rung]

    def promote(self, level:int = -1):
        from config import CONF
        if (self.current_rung == len(self.master_job.promotional_ladder)-1):
            return False
        
        if level != -1: self.current_rung = level
        else: self.current_rung += 1

        self.days_since_promotion = CONF.current_date

        self.update_pay()

        return True





        
class jobHistory():
    def __init__(self, job: job, start_date: int, end_date: int):
        pass