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

""" 
    RuleSetNode{
        id: a unique integer identifier for each edge
        name: a string identifier
    } 
"""
class RuleSetNode:
    def __init__(self, id, name, edges = []):
        self.id = id;
        self.name = name;
        self.out_edges = edges;

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
        self.id = id;
        self.start_node = start_node;
        self.end_node = end_node;
        self.condition = condition;


prop47codes = ["487", "490.2", "459.5", "459", "461", "496", "666", "473", "476", "476a", "11350", "11357", "11377"];

class RuleSet:

    """ 
    Inputs: JSON Object
    {
        crimes: [{
            crime_type: [Felony, Misdemeanor, Infraction],
            result: [Prison, Probation, County Jail, Fine],
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
        self.nodes = self.createGraph();
        #self.edges = edges;

    """
    Returns a generator that each time returns a unique int, starting from 0
    To get the next value from the generator, call next(generator). 
    """
    def getUniqueId(self):
        temp = 0;
        while True:
            yield temp
            temp += 1;

    """
    Returns the graph of the ruleset
    """
    def createGraph(self):
        nodes = [];
        #edges = [];

        node_counter = self.getUniqueId();
        edge_counter = self.getUniqueId();

        prison = RuleSetNode(next(node_counter), "Prison");
        
        prop_47_64_elig = RuleSetNode(next(node_counter), "Prop 47 Eligible");
        not_prop_47_64_elig = RuleSetNode(next(node_counter), "Not Prop 47 Eligible");

        prison_eligible_path = RuleSetEdge(next(edge_counter), prison, prop_47_64_elig, (lamdba crime: crime.offense_code in prop47codes));
        prison_not_eligible_path = RuleSetEdge(next(edge_counter), prison, not_prop_47_64_elig, (lamdba crime: crime.offense_code not in prop47codes));

        nodes.append(prison, prop_47_64_elig, not_prop_47_64_elig);
        #edges.append(prison_eligible_path, prison_not_eligible_path);

        #return (nodes, edges)
        return nodes

    def evaluate(self, json):
        pass


