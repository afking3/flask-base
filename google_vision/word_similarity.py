import numpy as np
from weighted_levenshtein import lev, osa, dam_lev


# Initialuze 2D, 128 x 128 array with costs of all substitutes initialized to 10
substitute_costs = np.full((128, 128),10, dtype=np.float64) 

#Each of these lines sets the cost for replacement lower for similar looking characters
substitute_costs[ord('I'), ord('1')] = 1.0  
substitute_costs[ord('S'), ord('5')] = 1.0
substitute_costs[ord('O'), ord('0')] = 1.0

term_list=["DISPO", "COURT", "NAM 001", "CON"]

#Checks to see if a given word is similar
#to known rap sheet term. Returns [term] if similar, None otherwise
def check_word_similarity(word):
    for term in term_list:
        if lev(term, word, substitute_costs=substitute_costs)<len(term):
            return term

    return None

#Tests (can be commented out after implementing)
print ("DISPO and DISPO "+ str(lev('DISPO', 'DISPO', substitute_costs=substitute_costs)))
print ("DISPO and DAMN "+str(lev('DISPO', 'DAMN', substitute_costs=substitute_costs)))
print ("DISPO and D1SPO "+str(lev('DISPO', 'D1SPO', substitute_costs=substitute_costs))) 
print ("DISPO and D15PO "+str(lev('DISPO', 'D15PO', substitute_costs=substitute_costs)))
print ("DISPO and D15P0 "+str(lev('DISPO', 'D15P0', substitute_costs=substitute_costs)))

print ("NAM 001 and NAM OO1 "+str(lev('NAM 001', 'NAM OO1', substitute_costs=substitute_costs)))

print ("COURT and C0URT "+str(lev('COURT', 'C0URT', substitute_costs=substitute_costs)))

print (check_word_similarity("D15P0"))
print (check_word_similarity("FELONY"))

