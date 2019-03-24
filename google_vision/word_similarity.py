import numpy as np
from weighted_levenshtein import lev, osa, dam_lev



substitute_costs = np.full((128, 128),10, dtype=np.float64)  # make a 2D array of 1's
substitute_costs[ord('I'), ord('1')] = 1.0  # make substituting '' for 'H' cost 1.25 as well
substitute_costs[ord('S'), ord('5')] = 1.0
substitute_costs[ord('O'), ord('0')] = 1.0



print ("DISPO and DISPO "+ str(lev('DISPO', 'DISPO', substitute_costs=substitute_costs)))
print ("DISPO and DAMN "+str(lev('DISPO', 'DAMN', substitute_costs=substitute_costs)))
print ("DISPO and D1SPO "+str(lev('DISPO', 'D1SPO', substitute_costs=substitute_costs))) 
print ("DISPO and D15PO "+str(lev('DISPO', 'D15PO', substitute_costs=substitute_costs)))
print ("DISPO and D15P0 "+str(lev('DISPO', 'D15P0', substitute_costs=substitute_costs)))

print ("NAM 001 and NAM OO1 "+str(lev('NAM 001', 'NAM OO1', substitute_costs=substitute_costs)))

print ("COURT and C0URT "+str(lev('COURT', 'C0URT', substitute_costs=substitute_costs)))

