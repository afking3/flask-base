from datetime import datetime
from dateutil.relativedelta import relativedelta
from messages import *

class Rapsheet():
    def __init__(self, crimes = []):
        self.crimes = crimes

    def addCrime(self, crime):
        self.crimes.append(crime)

    def print(self):
        for crime in self.crimes:
            crime.printCrime()

class Crime():

    ''' '''
    def __init__(self, crime_type, result, convict_date, offense_code, prob_status, nonviolent_nonserious):
        self.crime_type = crime_type
        self.result = result
        self.conviction_date = convict_date
        self.offense_code = offense_code
        self.probation_status = prob_status
        self.nonviolent_nonserious = nonviolent_nonserious

    def printCrime(self):
        string = ""
        string += self.crime_type + " | "
        string += self.result + " | "
        string += self.conviction_date.strftime('%m/%d/%Y') + " | "
        string += self.offense_code + " | "
        string += self.probation_status + " | "
        string += self.nonviolent_nonserious + " | "
        print(string)

example = Rapsheet([
        Crime("Infraction", "Fine", datetime.now(), None, None, None)
    ])

prop47codes = ["487", "490.2", "459.5", "459", "461", "496", "666", "473", "476", "476a", "11350", "11357", "11377"];

def inPropCodes(crime, rapsheet):
    for code in prop47codes:
        if code in crime.offense_code:
            return True
    return False

def notInPropCodes(crime, rapsheet):
    return not inPropCodes(crime, rapsheet)

def isAB109Elig(crime, rapsheet):
    return crime.nonviolent_nonserious

def isPrison(crime, rapsheet):
    return crime.result["jail"] != False and crime.result["jail"] != None and crime.result["jail"] != "None"

def isCountyJail(crime, rapsheet):
    return crime.result["jail"] != False and crime.result["jail"] != None and crime.result["jail"] != "None"

def isProbation(crime, rapsheet):
    return crime.result["probation"] != False and crime.result["probation"] != None and crime.result["probation"] != "None"

def isUpTo1year(crime, rapsheet):
    return True

def isFelony(crime, rapsheet):
    return crime.crime_type == "Felony"

def isMisdemeanor(crime, rapsheet):
    return crime.crime_type == "Misdemeanor"

def isSupervision(crime, rapsheet):
    return crime.result["probation"] != False and crime.result["probation"] != None and crime.result["probation"] != "None"

def isProbationCompletion(crime, rapsheet):
    return crime.probation_status == "Completed"

def isEarlyTermination(crime, rapsheet):
    return crime.probation_status == "Early Termination"

def yearsSinceConvictionDate(crime, rapsheet):
    now = datetime.now()
    return relativedelta(now, crime.conviction_date).years

def hasMoreRecentConviction(crime, rapsheet):
    other_crimes = [c for c in rapsheet.crimes if c != crime]
    if len(other_crimes) < 1:
        return False

    current_crime_date = crime.conviction_date
    for other in other_crimes:
        if other.conviction_date > current_crime_date:
            return True
    return False


class RuleSetNode:
    def __init__(self, id, name, message = ""):
        self.id = id
        self.name = name
        self.message = message

class RuleSetEdge:
    def __init__(self, id, start_node, end_node, condition = (lambda _: True)):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.condition = condition

class RuleSet:

    def __init__(self):
        self.createGraph()

    def result(self, crime, rapsheet):
        assert(isinstance(crime, Crime))
        assert(isinstance(rapsheet, Rapsheet))

        end_node, messages = self.evaluate(crime, rapsheet)
        resulting_obj = {
            'result': end_node.name,
            'messages': messages
        }
        return resulting_obj

    def resultsFromRapSheet(self, rapsheet):
        assert(isinstance(rapsheet, Rapsheet))

        results = [self.result(crime, rapsheet) for crime in rapsheet.crimes]
        return results

    """
    Returns a generator that each time returns a unique int, starting from 0
    To get the next value from the generator, call next(generator).
    """
    def getUniqueId(self):
        temp = 0
        while True:
            yield temp
            temp += 1

    ''' 
        returns a response (node, failure)
        where failure is set to True 
    '''
    def step(self, crime, rapsheet, current_node):
        assert(isinstance(crime, Crime))
        assert(isinstance(rapsheet, Rapsheet))
        assert(isinstance(current_node, RuleSetNode))

        if self.graph[current_node] == []:
            return (current_node, False)

        for (dest, predicate) in self.graph[current_node]:
            assert(type(predicate) == type(lambda x, y: x + y))
            if predicate(crime, rapsheet):
                return (dest, False)
        return (None, True)

    def evaluate(self, crime, rapsheet):
        assert(isinstance(crime, Crime))
        assert(isinstance(rapsheet, Rapsheet))

        messages = []

        try:
            current_node = self.start_node
            while current_node != None and len(self.graph[current_node]) > 0:
                current_message = current_node.message
                if current_message != "":
                    messages.append(current_message)
                current_node, failed = self.step(crime, rapsheet, current_node)
                if failed:
                    messages.append("Inconclusive: unable to find an end result.")
                    return (None, messages)
                    
            #this code can be cleaned up
            current_message = current_node.message
            if current_message != "":
                messages.append(current_message)

            return (current_node, messages)

        except:
            messages.append("Inconclusive: unable to find an end result.")
            return (None, messages)

    """
    Sets the start node of the graph, and connects all nodes of the graph together
    """
    def createGraph(self):
        # nodes = []
        #edges = []
        graph = {}

        node_counter = self.getUniqueId()
        #edge_counter = self.getUniqueId()

        start_node = RuleSetNode(next(node_counter), START)
        self.start_node = start_node

        prison = RuleSetNode(next(node_counter), PRISON)
        file_cr180_misdemeanor = RuleSetNode(next(node_counter), CR180, message = CR180)
        not_prop_47_64_elig = RuleSetNode(next(node_counter), NOT_47_ELIGIBLE)
        ab_109_discretionary = RuleSetNode(next(node_counter), DISCRETIONARY)
        ab_109_options = RuleSetNode(next(node_counter), AB_109_OPTIONS)
        no_probation = RuleSetNode(next(node_counter), NO_PROBATION, message = WAIT_1_YEAR)
        public_defender = RuleSetNode(next(node_counter), LA_PUB_DEF, message = PUBLIC_DEFENDER)
        county_jail_ab_109 = RuleSetNode(next(node_counter), COUNTY_JAIL)
        county_jail_discretionary = RuleSetNode(next(node_counter), DISCRETIONARY, message = COUNTY_JAIL_DISC)
        jail_only = RuleSetNode(next(node_counter), JAIL_ONLY, message = WAIT_2_YEARS)
        jail_and_supervision = RuleSetNode(next(node_counter), JAIL_AND_SUPE, message = WAIT_1_YEAR_1203)

        probation = RuleSetNode(next(node_counter), PROBATION)
        probation_compl_or_early_term = RuleSetNode(next(node_counter), MANDATORY)
        probation_discretionary = RuleSetNode(next(node_counter), DISCRETIONARY)

        up_to_1_year = RuleSetNode(next(node_counter), UP_TO_1_YEAR)
        code_1203_point4a = RuleSetNode(next(node_counter), CODE_1203POINT4A)
        one_year_from_conviction_date = RuleSetNode(next(node_counter), ONE_YEAR_FROM)
        convicted_discretionary = RuleSetNode(next(node_counter), DISCRETIONARY)
        convicted_mandatory = RuleSetNode(next(node_counter), MANDATORY)
        convicted_not_eligible = RuleSetNode(next(node_counter), NOT_ELIGIBLE)

        discretionary = RuleSetNode(next(node_counter), DISCRETIONARY)
        mandatory = RuleSetNode(next(node_counter), MANDATORY)
        not_eligible = RuleSetNode(next(node_counter), NOT_ELIGIBLE)

        graph[discretionary] = []
        graph[mandatory] = []
        graph[not_eligible] = []

        fine = RuleSetNode(next(node_counter), FINE)

        graph[start_node] = [   #create all these helper functions
            (prison, isPrison),
            (county_jail_ab_109, isCountyJail),
            (probation, isProbation),
            (up_to_1_year, isUpTo1year)
        ]

        graph[prison] = [
            (file_cr180_misdemeanor, inPropCodes),
            (not_prop_47_64_elig, notInPropCodes)
        ]

        graph[file_cr180_misdemeanor] = [(code_1203_point4a,  lambda x, y: True)]

        graph[not_prop_47_64_elig] = [
            (ab_109_discretionary, isAB109Elig),
            (ab_109_options, lambda x, y: not isAB109Elig(x, y))
        ]

        graph[ab_109_discretionary] = []

        graph[ab_109_options] = [
            (public_defender, isFelony),
            (probation, lambda x, y: isMisdemeanor(x, y) and isProbation(x, y)),
            (no_probation, lambda x, y: isMisdemeanor(x, y) and not isProbation(x, y))
        ]

        graph[no_probation] = [
            (code_1203_point4a, lambda x, y: True)
        ]

        graph[public_defender] = []

        # graph[county_jail_ab_109] = [
        #     (jail_only, lambda x, y: not isSupervision(x, y)),
        #     (jail_and_supervision, isSupervision)
        # ]

        graph[county_jail_ab_109] = [
            (county_jail_discretionary, lambda x, y: True)
        ]
        graph[county_jail_discretionary] = []

        graph[jail_only] = []
        graph[jail_and_supervision] = []

        graph[probation] = [
            (mandatory, lambda x, y: isProbationCompletion(x, y) or isEarlyTermination(x, y)),
            (discretionary, lambda x, y: not (isProbationCompletion(x, y) and isEarlyTermination(x, y)))
        ]
        graph[probation_compl_or_early_term] = []
        graph[probation_discretionary] = []

        graph[up_to_1_year] = [(code_1203_point4a,  lambda x, y: True)]

        graph[code_1203_point4a] = [
            (one_year_from_conviction_date, lambda x, y: yearsSinceConvictionDate(x, y) >= 1),
            (convicted_not_eligible, lambda x, y: yearsSinceConvictionDate(x, y) < 1)
        ]

        graph[one_year_from_conviction_date] = [
            (convicted_discretionary, lambda x, y: hasMoreRecentConviction(x, y)),
            (convicted_mandatory, lambda x, y: not hasMoreRecentConviction(x, y))
        ]

        graph[convicted_discretionary] = []
        graph[convicted_mandatory] = []
        graph[convicted_not_eligible] = []

        self.graph = graph


c = Crime("Felony", "Prison", None, None, "487", "Not Completed")
given = Rapsheet(
[
    c
])

rs = RuleSet()
g = rs.createGraph()
rs.evaluate(c, given)
