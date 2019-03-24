import numpy as np
from weighted_levenshtein import lev, osa, dam_lev



substitute_costs = np.full((128, 128),10, dtype=np.float64)  # make a 2D array of 1's
substitute_costs[ord('I'), ord('1')] = 1.0  # make substituting '' for 'H' cost 1.25 as well
substitute_costs[ord('S'), ord('5')] = 1.0
substitute_costs[ord('O'), ord('0')] = 1.0


print (lev('DISPO', 'DISPO', substitute_costs=substitute_costs))
print (lev('DISPO', 'DAMN', substitute_costs=substitute_costs))
print (lev('DISPO', 'D1SPO', substitute_costs=substitute_costs))  # now it prints '1.25'
print (lev('DISPO', 'D15PO', substitute_costs=substitute_costs))
print (lev('DISPO', 'D15P0', substitute_costs=substitute_costs))

print (lev('NAM 001', 'NAM OO1', substitute_costs=substitute_costs))