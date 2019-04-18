import numpy as np
from weighted_levenshtein import lev, osa, dam_lev


# Initialuze 2D, 128 x 128 array with costs of all substitutes initialized to 10
substitute_costs = np.full((128, 128),10, dtype=np.float64) 

#Each of these lines sets the cost for replacement lower for similar looking characters
#Need to duplicate each rule so that A-B cost is same as B-A cost
substitute_costs[ord('I'), ord('1')] = 1.0  
substitute_costs[ord('S'), ord('5')] = 1.0

substitute_costs[ord('O'), ord('0')] = 0.5
substitute_costs[ord('0'), ord('O')] = 0.5


substitute_costs[ord('N'), ord('H')] = 0.5
substitute_costs[ord('H'), ord('N')] = 0.5


term_list=["DISPO", "COURT", "NAM/001", "CON"]

#Checks to see if a given word is similar
#to known rap sheet term. Returns [term] if similar, None otherwise
def check_word_similarity(word):
    for term in term_list:
        if lev(term, word, substitute_costs=substitute_costs)<len(term):
            return term

    return None

#Checks to see if input_word is similar to given_term.
#Returns true if clsoe enough, false if not.
#Replaces all byte representations with a single character for sanity's sake.
def check_word_against_term(input_word, given_term):
    new_str = ""
    for chr in input_word:
        if ord(chr) < 128:
            new_str += chr
        else:
            new_str += "?"
    return lev(new_str, given_term, substitute_costs=substitute_costs)<2

#Tests (can be commented out after implementing)
# print ("DISPO and DISPO "+ str(lev('DISPO', 'DISPO', substitute_costs=substitute_costs)))
# print ("DISPO and DAMN "+str(lev('DISPO', 'DAMN', substitute_costs=substitute_costs)))
# print ("DISPO and D1SPO "+str(lev('DISPO', 'D1SPO', substitute_costs=substitute_costs))) 
# print ("DISPO and D15PO "+str(lev('DISPO', 'D15PO', substitute_costs=substitute_costs)))
# print ("DISPO and D15P0 "+str(lev('DISPO', 'D15P0', substitute_costs=substitute_costs)))

# print ("NAM 001 and NAM OO1 "+str(lev('NAM 001', 'NAM OO1', substitute_costs=substitute_costs)))

# print ("COURT and C0URT "+str(lev('COURT', 'C0URT', substitute_costs=substitute_costs)))

# print (check_word_similarity("D15P0"))
# print (check_word_similarity("FELONY"))