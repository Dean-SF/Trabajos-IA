# --------------------------------------------------------------------------------------
# -----------------------------------PARAMETERS-----------------------------------------
# --------------------------------------------------------------------------------------

# DO NOT USE NEGATIVES NUMBERS ANYWHERE IN THE PARAMETERS, WE ASUME EVERY NUMBER IS 
# GOING TO BE ASSIGNED A NUMBER GREATER OR EQUAL TO 0 AND IS NOT CHECKED.

# ----------------------------Constant values for genetic-------------------------------

# >>>>>>>>Individuals<<<<<<<<
STROKES_PER_INDIVIDUAL = 500 # How many strokes the picture is composed by

# >>>>>>>>Generations<<<<<<<<
POPULATION = 100
NUM_GENERATIONS = 500

# Percentages based on total population of how many individuals for the next
# generation will be from fittest selection, mutated or crossovers. This
# percentage needs to equal a whole number or a exception is raised
FITTEST_PERCENT = 0.1   
MUTATED_PERCENT = 0.45
CROSSED_PERCENT = 0.45

# How big the subpopulation is going to be for the selection tournament
TOURNAMENT_PERCENTAGE = 0.2

# >>>>>>>>Mutation<<<<<<<<
MIN_MUTATIONS_STROKE = 1
MAX_MUTATIONS_STROKE = 5 # Can't be more than 5
# -----------------------
MIN_STROKE_TO_MUTATE = 1
MAX_STROKE_TO_MUTATE = 50

# >>>>>>>>Crossover<<<<<<<<
MIN_STROKE_TO_CROSS = 1
MAX_STROKE_TO_CROSS = 50

# ----------------------------Constant values for images--------------------------------
IMG_SIZE = 128

# ---------------------------Constant values for brushes--------------------------------
STROKE_MAX_SIZE = 25
STROKE_MIN_SIZE = 1

# >>>>>>>>better not to touch anything below<<<<<<<<
BACKGROUND_THRESHOLD = 0
MIN_DARK_LEVEL = 0
MAX_DARK_LEVEL = 250

MIN_ANGLE = 0
MAX_ANGLE = 360

NUM_BRUSHES = 4

# --------------------------------------------------------------------------------------

# --------------------------------------------------------------------------------------
# -----------------------------------PARAMETER CHECKER----------------------------------
# --------------------------------------------------------------------------------------
def param_checker():
    fittest_amount = POPULATION*FITTEST_PERCENT
    mutated_amount = POPULATION*MUTATED_PERCENT
    crossed_amount = POPULATION*CROSSED_PERCENT
    
    if(not fittest_amount.is_integer()):
       raise ValueError("FITTEST_PERCENT doesn't result in an integer number")
    
    if(not mutated_amount.is_integer()):
       raise ValueError("MUTATED_PERCENT doesn't result in an integer number")
    
    if(not crossed_amount.is_integer()):
       raise ValueError("CROSSED_PERCENT doesn't result in an integer number")
    
    if(FITTEST_PERCENT+MUTATED_PERCENT+CROSSED_PERCENT != 1): 
        raise ValueError("The sum of FITTEST_PERCENT, MUTATED_PERCENT, and CROSSED_PERCENT doesn't add up to 1")
    
    if(fittest_amount+mutated_amount+crossed_amount != POPULATION):
       raise ValueError("The FITTEST_PERCENT, MUTATED_PERCENT, and CROSSED_PERCENT doesn't add up to the POPULATION value")
    
    if(MAX_MUTATIONS_STROKE > 5):
       raise ValueError("MAX_MUTATIONS_STROKE can't be more than 5, which is the amount of properties in individuals")
    
    if(MAX_DARK_LEVEL > 255):
       raise ValueError("MAX_DARK_LEVEL can't be more than 255")
    
    if(255-MAX_DARK_LEVEL <= BACKGROUND_THRESHOLD):
       raise ValueError("BACKGROUND_THRESHOLD can't be more than or equal than the difference between 255 and MAX_DARK_LEVEL")
    
    if(MAX_STROKE_TO_MUTATE > STROKES_PER_INDIVIDUAL):
       raise ValueError("MAX_STROKE_TO_MUTATE can't be more than STROKES_PER_INDIVIDUAL")
    
    if(MAX_STROKE_TO_CROSS > STROKES_PER_INDIVIDUAL):
       raise ValueError("MAX_STROKE_TO_MUTATE can't be more than STROKES_PER_INDIVIDUAL")
    
param_checker()
# --------------------------------------------------------------------------------------