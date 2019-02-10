class RuleSet:

    """ 
    Inputs: JSON Object
    {
        crimes: [{
            type: [Felony, Misdemeanor, Infraction],
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
        pass

    