import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import beta

# alpha, beta_param = 3, 6

AGE_DIST = None
GENERIC_NORMAL_DIST = None
RELATIONSHIP_PROBS = None
DIVORCED_PROBS = None

def generate_age_distribution(population_size):
    # Define parameters for age groups
    children_mean, children_std = 10, 5
    adults_mean, adults_std = 35, 10
    seniors_mean, seniors_std = 70, 10

    # Proportion of each age group in the population
    children_prop, adults_prop, seniors_prop = 0.65, 0.20, 0.15

    # Generate ages for each group
    children = np.random.normal(children_mean, children_std, int(population_size * children_prop))
    adults = np.random.normal(adults_mean, adults_std, int(population_size * adults_prop))
    seniors = np.random.normal(seniors_mean, seniors_std, int(population_size * seniors_prop))

    # Combine all age groups
    ages = np.concatenate([children, adults, seniors])

    # Clip ages to be within a realistic range
    ages = np.clip(ages, 0, 100)

    return ages

def generate_normal_dist(mean, std_dev):
    # Generate aggression levels using the normal distribution
    normal_levels = np.random.normal(mean, std_dev, 10000)

    # Truncate the values to stay within the range 0-100
    return np.clip(normal_levels, 0, 100)

def initialise(population_size):
    global AGE_DIST
    global GENERIC_NORMAL_DIST
    global RELATIONSHIP_DIST
    global RELATIONSHIP_PROBS
    global DIVORCED_PROBS

    # AGE_DIST = beta.rvs(alpha, beta_param, size=population_size) * 100
    # AGE_DIST = np.clip(AGE_DIST, 0, 100)
    AGE_DIST = generate_age_distribution(population_size)

    GENERIC_NORMAL_DIST = generate_normal_dist(50, 17)

    # single, relationship, married
    RELATIONSHIP_PROBS = {
        (0, 19): [0.8, 0.195, 0.005],
        (20, 25): [0.45, 0.45, 0.10],
        (25, 30): [0.2, 0.45, 0.35],
        (30, 49): [0.1, 0.35, 0.55],
        (50, 59): [0.05, 0.20, 0.75],
        (60, 100): [0.005, 0.05, 0.945]
    }
    RELATIONSHIP_DIST = np.random.choice([0, 1, 2], size=population_size, p=[0.3, 0.4, 0.3])

    # never divorced or widowed, divorced, widowed
    DIVORCED_PROBS = {
        (0, 19): [0.995, 0.005, 0],
        (20, 25): [0.94, 0.0599, 0.0001],
        (25, 30): [0.84, 0.15, 0.001],
        (30, 49): [0.7, 0.25, 0.05],
        (50, 59): [0.6, 0.32, 0.08],
        (60, 79): [0.5, 0.1, 0.4],
        (70, 79): [0.44, 0.06, 0.5],
        (80, 100): [0.25, 0.5, 0.7]
    }



def visualise(inDist):
    # Plot the distribution
    plt.hist(inDist, bins=100, edgecolor='black', density=True)
    plt.title('Base Distribution')
    plt.xlabel('Level')
    plt.ylabel('Probability Density')
    plt.show()