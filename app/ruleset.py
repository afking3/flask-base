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

"Returns boolean of if crime is AB 109 eligible"
def isAB109Elig(crime):
    return True



"""
    RuleSetNode{
        id: a unique integer identifier for each edge
        name: a string identifier
    }
"""
class RuleSetNode:
    def __init__(self, id, name, edges = []):
        self.id = id
        self.name = name
        self.out_edges = edges

    def addEdge(self, edge):
        self.out_edges.append(edge)

"""
    RuleSetEdge{
        id: a unique integer identifier for each edge
        start_node: the origin node
        end_node: the destination node
        condition: a function (dict -> bool) that checks if the
    }
"""
class RuleSetEdge:
    def __init__(self, id, start_node, end_node, condition = (lambda _: True)):
        self.id = id
        self.start_node = start_node
        self.end_node = end_node
        self.condition = condition


prop47codes = ["487", "490.2", "459.5", "459", "461", "496", "666", "473", "476", "476a", "11350", "11357", "11377"];

class RuleSet:

    """
    Inputs: JSON Object
    {
        crimes: [{
            crime_type: [Felony, Misdemeanor, Infraction],
            result: [Prison, Probation, County Jail, Fine, N/A, Dispo],
            conviction_date: [date],
            offense: [etc],
            offense_code: [some type],
            probation_status: [some type],
        }],
    }

    Outputs: JSON Object
    {
        crime_results: [{
            types: [Discretionary, Mandatory, Not Eligible, Wait/Deferred, Reduction],
            wait_time: [int],
            deferment_result: []
        }]
    }
    """

    def __init__(self):
        #create the graph here
        #(nodes, edges) = self.createGraph();
        #self.nodes = self.createGraph()
        #self.edges = edges;
        self.createGraph()

    """
    Returns a generator that each time returns a unique int, starting from 0
    To get the next value from the generator, call next(generator).
    """
    def getUniqueId(self):
        temp = 0
        while True:
            yield temp
            temp += 1

    def isAB109Elig(self, crime):
        return True

    def step(self, json, node):
        for edge in node.out_edges:
            if edge.condition(json):
                return edge.end_node
        return None

    def evaluate(self, json):
        current_node = self.start_node
        while(current_node != None and current_node.out_edges != []):
            current_node = self.step(json, current_node)
        return current_node

    """
    Sets the start node of the graph, and connects all nodes of the graph together
    """
    def createGraph(self):
        # nodes = []
        #edges = []

        node_counter = self.getUniqueId()
        edge_counter = self.getUniqueId()

        start_node = RuleSetNode(next(node_counter), "Start")
        self.start_node = start_node
    
        prison = RuleSetNode(next(node_counter), "Prison")
        prop_47_64_elig = RuleSetNode(next(node_counter), "Prop 47 Eligible")
        not_prop_47_64_elig = RuleSetNode(next(node_counter), "Not Prop 47 Eligible")
        file_cr180_misdemeanor = RuleSetNode(next(node_counter), "File CR-180 Misdemeanor")
        ab_109_eligible = RuleSetNode(next(node_counter), "Would've been AB 109 eligible")
        not_ab_109_eligible = RuleSetNode(next(node_counter), """
        Would not have been AB 109 eligible""")
        ab_109_discretionary = RuleSetNode(next(node_counter), "Discretionary")
        ab_109_options = RuleSetNode(next(node_counter), """Misdemeanor: NO
        probation, must wait one year. YES probation, see above\n Felony: Refer
        to L.A. Public Defender for \"Certificate of Rehabilitation\"""")

        county_jail_ab_109 = RuleSetNode(next(node_counter), "COUNTY JAIL AB109")
        county_jail_discretionary = RuleSetNode(next(node_counter), "Discretionary")
        jail_only = RuleSetNode(next(node_counter), """Jail Only, NO mandatory
        supervision. Must wait 2 years after release date to apply under 1203.41""")
        jail_and_supervision = RuleSetNode(next(node_counter), """Jail and mandatory
        supervision - must wait 1 year to apply under 1203.41""")
        probation = RuleSetNode(next(node_counter), "Probation")
        code_1203_point_4 = RuleSetNode(next(node_counter), "1203.4")
        probation_completion = RuleSetNode(next(node_counter), """Successful completion
        of probation (Mandatory)""")
        probation_early_termination = RuleSetNode(next(node_counter), """Early
        termination of probation (Mandatory)""")
        probation_discretionary = RuleSetNode(next(node_counter), "Discretionary")

        up_to_1_year = RuleSetNode(next(node_counter), "Up to 1 year in county jail")
        code_1203_point4a = RuleSetNode(next(node_counter), "1203.4a")
        one_year_from_conviction_date = RuleSetNode(next(node_counter), """1 year
        from conviction date""")
        convicted_of_crime_within_that_time = RuleSetNode(next(node_counter),
        "Convicted of a crime within that time")
        convicted_discretionary = RuleSetNode(next(node_counter), "Discretionary")
        not_convicted_of_a_crime_within_that_time = RuleSetNode(next(node_counter),
        "Not convicted of a crime within that time")
        convicted_mandatory = RuleSetNode(next(node_counter), "Mandatory")
        not_one_year_from_conviction_date = RuleSetNode(next(node_counter),
        """Not 1 year from conviction date""")
        convicted_not_eligible = RuleSetNode(next(node_counter), "Not eligible")

        fine = RuleSetNode(next(node_counter), "Fine")

        # (lamdba crime: crime.offense_code in prop47codes)
        #(amdba crime: crime.offense_code not in prop47codes)
        prison_eligible_path = RuleSetEdge(next(edge_counter), prison, prop_47_64_elig, lambda crime: crime.offense_code in prop47codes)
        prison_not_eligible_path = RuleSetEdge(next(edge_counter), prison, not_prop_47_64_elig, lambda crime: crime.offense_code not in prop47codes)
        
        go_to_1203_pointa_path = RuleSetEdge(next(edge_counter), file_cr180_misdemeanor, code_1203_point4a, lambda crime: True)

        not_ab109_eligible_path = RuleSetEdge(next(edge_counter), not_prop_47_64_elig, not_ab_109_eligible, lambda crime: isAB109Elig(crime))