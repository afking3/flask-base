#import from all the other files



''' 
Outputs a tuple of the rapsheet and results
    i.e.
        def __init__(self, crime_type, result, convict_date, offense, offense_code, prob_status):

        rapsheet = rs.Rapsheet(
            [
                rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None),
                rs.Crime("Infraction", "Fine", week_ago, None, None, None)
            ])
        (i.e. the first element is the messages, the second is the result)
        results = [
            [[], "Discretionary"],
            [[], "Not Eligible"]
        ]

    would return (rapsheet, results)
'''
def getOutputFromRapsheet(rapsheet):

    #vision = GOOGLEVISION(rapsheet)
    #     

''' 
Given an input (rapsheer, results), 
will give an output of the format

    crimes = [
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
    ]
'''
def formatOutput(input):
    pass


'''
Given an formatted input [input], 
will create an excel sheet
from this at the path [path] with the name [filename]

On success, returns the file path. On failure, 
returns None. 
'''
def createExcelSheet(input, filename, path):
    pass

    





