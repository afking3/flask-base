from datetime import datetime
from dateutil.relativedelta import relativedelta
from messages import *

class Rapsheet():
    def __init__(self, crimes = []):
        self.crimes = crimes

    def addCrime(self, crime):
        self.crimes.append(crime)

class Crime():
    def __init__(self, crime_type, result, convict_date, offense, offense_code, prob_status):
        self.crime_type = crime_type
        self.result = result
        self.conviction_date = convict_date
        self.offense = offense
        self.offense_code = offense_code
        self.probation_status = prob_status

example = Rapsheet([
        Crime("Infraction", "Fine", datetime.now(), None, None, None)
    ])

prop47codes = ["487", "490.2", "459.5", "459", "461", "496", "666", "473", "476", "476a", "11350", "11357", "11377"];

def inPropCodes(crime, rapsheet):
    return crime.offense_code in prop47codes

def notInPropCodes(crime, rapsheet):
    return not inPropCodes(crime, rapsheet)

def isAB109Elig(crime, rapsheet):
    return True

def isPrison(crime, rapsheet):
    return crime.result == "Prison"

def isCountyJail(crime, rapsheet):
    return crime.result == "County Jail"

def isProbation(crime, rapsheet):
    return crime.result == "Probation"

def isUpTo1year(crime, rapsheet):
    return True

def isFelony(crime, rapsheet):
    return crime.crime_type == "Felony"

def isMisdemeanor(crime, rapsheet):
    return crime.crime_type == "Misdemeanor"

def isSupervision(crime, rapsheet):
    return crime.result == "Probation"

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
        

def isConvicted(crime, rapsheet):
    return True

class RuleSetNode:
    def __init__(self, id, name, messages = []):
        self.id = id
        self.name = name
        self.messages = messages

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

    def step(self, crime, rapsheet, current_node):
        assert(isinstance(crime, Crime))
        assert(isinstance(rapsheet, Rapsheet))
        assert(isinstance(current_node, RuleSetNode))

        for (dest, predicate) in self.graph[current_node]:
            assert(type(predicate) == type(lambda x, y: x + y))
            if predicate(crime, rapsheet):
                return dest
        return None

    def evaluate(self, crime, rapsheet, messages = []):
        assert(isinstance(crime, Crime))
        assert(isinstance(rapsheet, Rapsheet))
        assert(type(messages) == type([]))

        current_node = self.start_node
        while(current_node != None and len(self.graph[current_node]) > 0):
            current_node = self.step(crime, rapsheet, current_node)
            if(current_node != None and current_node.messages):
                messages.append(current_node.messages)
        return (current_node, messages)

    """
    Sets the start node of the graph, and connects all nodes of the graph together
    """
    def createGraph(self):
        # nodes = []
        #edges = []
        graph = {}

        node_counter = self.getUniqueId()
        #edge_counter = self.getUniqueId()

        start_node = RuleSetNode(next(node_counter), "Start")
        self.start_node = start_node

        prison = RuleSetNode(next(node_counter), "Prison")
        file_cr180_misdemeanor = RuleSetNode(next(node_counter), "File CR-180 Misdemeanor")
        not_prop_47_64_elig = RuleSetNode(next(node_counter), "Not Prop 47 Eligible")
        ab_109_discretionary = RuleSetNode(next(node_counter), DISCRETIONARY)
        ab_109_options = RuleSetNode(next(node_counter), """Misdemeanor: NO
        probation, must wait one year. YES probation, see above\n Felony: Refer
        to L.A. Public Defender for \"Certificate of Rehabilitation\"""")
        public_defender = RuleSetNode(next(node_counter), "LA Public Defender: (213) 974-3057")
        county_jail_ab_109 = RuleSetNode(next(node_counter), "COUNTY JAIL AB109", "If Jail and Mandatory Supervision - must wait 1 year to apply under 1203.41. If Jail only and no mandatory supervision, must wait 2 years to apply under 1203.41.")
        jail_only = RuleSetNode(next(node_counter), """Jail Only, NO mandatory
        supervision. Must wait 2 years after release date to apply under 1203.41""")
        jail_and_supervision = RuleSetNode(next(node_counter), """Jail and mandatory
        supervision - must wait 1 year to apply under 1203.41""")

        probation = RuleSetNode(next(node_counter), "Probation")
        probation_completion = RuleSetNode(next(node_counter), """Successful completion
        of probation (Mandatory)""")
        probation_early_termination = RuleSetNode(next(node_counter), """Early
        termination of probation (Mandatory)""")
        probation_discretionary = RuleSetNode(next(node_counter), "Discretionary")

        up_to_1_year = RuleSetNode(next(node_counter), "Up to 1 year in county jail")
        code_1203_point4a = RuleSetNode(next(node_counter), "1203.4a")
        one_year_from_conviction_date = RuleSetNode(next(node_counter), """1 year
        from conviction date""")
        convicted_discretionary = RuleSetNode(next(node_counter), "Discretionary")
        convicted_mandatory = RuleSetNode(next(node_counter), "Mandatory")
        convicted_not_eligible = RuleSetNode(next(node_counter), "Not Eligible")

        discretionary = RuleSetNode(next(node_counter), "Discretionary")
        mandatory = RuleSetNode(next(node_counter), "Mandatory")
        not_eligible = RuleSetNode(next(node_counter), "Not Eligible")

        graph[discretionary] = []
        graph[mandatory] = []
        graph[not_eligible] = []

        fine = RuleSetNode(next(node_counter), "Fine")

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

        graph[file_cr180_misdemeanor] = [(code_1203_point4a,  True)]

        graph[not_prop_47_64_elig] = [
            (ab_109_discretionary, isAB109Elig),
            (ab_109_options, lambda x, y: not isAB109Elig(x, y))
        ]

        graph[ab_109_discretionary] = []

        graph[ab_109_options] = [
            (public_defender, isFelony),
            (probation, lambda x, y: isMisdemeanor(x, y) and isProbation(x, y)),
            (code_1203_point4a, lambda x, y: isMisdemeanor(x, y) and not isProbation(x, y))
        ]

        graph[public_defender] = []

        # graph[county_jail_ab_109] = [
        #     (jail_only, lambda x, y: not isSupervision(x, y)),
        #     (jail_and_supervision, isSupervision)
        # ]

        graph[county_jail_ab_109] = [
            (discretionary, lambda x, y: True)
        ]

        graph[jail_only] = []
        graph[jail_and_supervision] = []

        graph[probation] = [
            (mandatory, lambda x, y: isProbationCompletion(x, y) or isEarlyTermination(x, y)),
            (discretionary, lambda x, y: not (isProbationCompletion(x, y) and isEarlyTermination(x, y)))
        ]
        graph[probation_completion] = []
        graph[probation_early_termination] = []
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
