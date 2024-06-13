from typing import Tuple

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



# Contains info about the job that a person has.
# A person is a assigned a job class not a masterjob
class job:
    def __init__(self, master_job: MASTER_JOB, start_date: int, end_date: int, profeciency: int, enjoyment: float, reason_for_performance: str):
        self.master_job: MASTER_JOB = master_job
        self.start_date: int = start_date
        self.end_date: int = end_date
        self.current_rung: int = 0
        self.profecieny: int = profeciency
        self.enjoyment: float = enjoyment
        self.reason_for_performance: str = reason_for_performance

    def promote(self):
        if (self.current_rung == len(self.promotional_ladder)-1):
            return False
        self.current_rung += 1
        return True





        
class jobHistory():
    def __init__(self, job: job, start_date: int, end_date: int):
        pass