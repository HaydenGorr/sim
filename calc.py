import math

a = abs(55-56.632134139086354)
c = abs(75-58.893981525561614)
e = abs(20-50.971271529675484)
n = abs(40-55.48373358232395)
o = abs(60-16.668432644371357)
iq_req = 120

iq_std = 15 # standard deviation of iq


r = (a + c + e + n + o)/5 # temperment calculation

r2 = r

# 100 is max distance from ideal
# 0 is closest to ideal

# 50 means you can enjoy it from a temperment pov
print(r)

iq_dist = 95.5 - iq_req # a negative iq implies inadiquicy 

print (iq_dist)

inability_to_do_task = math.floor(abs(iq_dist/iq_std))
print(inability_to_do_task) # this is the number of standard deviations away from the ideal iq



