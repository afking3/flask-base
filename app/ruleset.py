dummy_input = {
    "crimes": [{
        "crime_type": "Felony",
        "result": "Prison",
        "conviction_date": "02-26-1990",
        "offense": None,
        "offense_code": None,
        "probation_status": None
    }]
}

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

def isAB109Elig(crime):
    return True

def isPrison(crime):
    return True

def isCountyJail(crime):
    return True

def isProbation(crime):
    return crime["crimes"][0]["result"] == "Probation"

def isUpTo1year(crime):
    return True

def isFelony(crime):
    return True

def isMisdemeanor(crime):
    return True

def isSupervision(crime):
    return True

def isProbationCompletion(crime):
    True

def isEarlyTermination(crime):
    return True

def yearsSinceConvictionDate(crime):
    return 0

def isConvicted(crime):
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


prop47codes = ["487", "490.2", "459.5", "459", "461", "496", "666", "473", "476", "476a", "11350", "11357", "11377"];

class RuleSet:

    def __init__(self):
        #create the graph here
        #(nodes, edges) = self.createGraph();
        #self.nodes = self.createGraph()
        #self.edges = edges;
        self.createGraph()

    def result(self, json):
        end_node, messages = self.evaluate(json)
        resulting_obj = {
            'result': end_node.name, 
            'messages': messages
        }
        return resulting_obj

    def resultFromRapSheet(self, rapsheet):
        results = [self.result(crime) for crime in rapsheet.crimes]
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

    def step(self, json, node):
        for (dest, predicate) in self.graph[node]:
            if predicate(json):
                return dest
        return None

    def evaluate(self, json, messages = []):
        current_node = self.start_node
        while(current_node != None and len(self.graph[current_node]) > 0):
            current_node = self.step(json, current_node)
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
        edge_counter = self.getUniqueId()

        start_node = RuleSetNode(next(node_counter), "Start")
        self.start_node = start_node

        prison = RuleSetNode(next(node_counter), "Prison")
        file_cr180_misdemeanor = RuleSetNode(next(node_counter), "File CR-180 Misdemeanor")
        not_prop_47_64_elig = RuleSetNode(next(node_counter), "Not Prop 47 Eligible")
        ab_109_discretionary = RuleSetNode(next(node_counter), "Discretionary")
        ab_109_options = RuleSetNode(next(node_counter), """Misdemeanor: NO
        probation, must wait one year. YES probation, see above\n Felony: Refer
        to L.A. Public Defender for \"Certificate of Rehabilitation\"""")
        public_defender = RuleSetNode(next(node_counter), "LA Public Defender: (213) 974-3057")
        county_jail_ab_109 = RuleSetNode(next(node_counter), "COUNTY JAIL AB109")
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
        convicted_not_eligible = RuleSetNode(next(node_counter), "Not eligible")

        fine = RuleSetNode(next(node_counter), "Fine")

        graph[start_node] = [   #create all these helper functions
        (prison, lambda x: isPrison(x)),
        (county_jail_ab_109, lambda x: isCountyJail(x)),
        (probation, lambda x: isProbation(x)),
        (up_to_1_year, lambda x: isUpTo1year(x))
        ]

        graph[prison] = [
        (file_cr180_misdemeanor, lambda x: x in prop47codes),
        (not_prop_47_64_elig, lambda x: x not in prop47codes)
        ]

        graph[file_cr180_misdemeanor] = [(code_1203_point4a, lambda x: True)]

        graph[not_prop_47_64_elig] = [
        (ab_109_discretionary, lambda x: isAB109Elig(x)),
        (ab_109_options, lambda x: not isAB109Elig(x))
        ]

        graph[ab_109_discretionary] = []

        graph[ab_109_options] = [
        (public_defender, lambda x: isFelony(x)),
        (probation, lambda x: isMisdemeanor(x) and isProbation(x)),
        (code_1203_point4a, lambda x: isMisdemeanor(x) and not isProbation(x))
        ]

        graph[public_defender] = []

        graph[county_jail_ab_109] = [
        (jail_only, lambda x: not isSupervision(x)),
        (jail_and_supervision, lambda x: isSupervision(x))
        ]

        graph[jail_only] = []
        graph[jail_and_supervision] = []

        graph[probation] = [
        (probation_completion, lambda x: isProbationCompletion(x)),
        (probation_early_termination, lambda x: isEarlyTermination(x)),
        (probation_discretionary, lambda x: not (isProbationCompletion(x) and isEarlyTermination(x)))
        ]
        graph[probation_completion] = []
        graph[probation_early_termination] = []
        graph[probation_discretionary] = []

        graph[up_to_1_year] = [(code_1203_point4a, lambda x: True)]

        graph[code_1203_point4a] = [
        (one_year_from_conviction_date, lambda x: yearsSinceConvictionDate(x) <= 1),
        (convicted_not_eligible, lambda x: yearsSinceConvictionDate(x) > 1)
        ]

        graph[one_year_from_conviction_date] = [
        (convicted_discretionary, lambda x: isConvicted(x)),
        (convicted_mandatory, lambda x: not isConvicted(x))
        ]

        graph[convicted_discretionary] = []
        graph[convicted_mandatory] = []
        graph[convicted_not_eligible] = []

        self.graph = graph