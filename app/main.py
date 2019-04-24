import ruleset
#import vision
import xlwt 
from xlwt import Workbook

''' 
Outputs a tuple of the rapsheet and results
    i.e.
        def __init__(self, crime_type, result, convict_date, offense, offense_code, prob_status):

        rapsheet = rs.Rapsheet(
            [
                rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None),
                rs.Crime("Infraction", "Fine", week_ago, None, None, None)
            ])
        results = [
            [[], "Discretionary"],
            [[], "Not Eligible"]
        ]

    would return (rapsheet, results)
'''
def getOutputFromRapsheet(rap):
    #json = vision.detect_document(rap)
    #rapsheet = vision.parse_document(json)
    #rules = ruleset.RuleSet()
    #rapsheet_results = rules.resultsFromRapSheet(rapsheet)
    #return (rapsheet, rapsheet_results)
    pass

''' 
Given an input (rapsheet, results), 
will give an output of the format

    crimes = [
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
        {crime_type, result, convict_date, offsense, offense_code, prob_status, expunge_result, expunge_messages}
    ]
'''
def formatOutput(_input):
    rapsheet = _input[0]
    crimes = rapsheet.crimes
    results = _input[1]

    final_crimes = []
    for index in range(len(crimes)):
        crime = crimes[index]
        new_obj = {}
        new_obj.crime_type = crime.crime_type
        new_obj.result = crime.result
        new_obj.convict_date = crime.convict_date
        new_obj.offense = crime.offense
        new_obj.offense_code = crime.offense_code
        new_obj.prob_status = crime.prob_status
        result = results[index]
        new_obj.expunge_result = result[1]
        new_obj.expunge_messages = result[0]
        final_crimes.append(new_obj)
    return final_crimes

'''
Given an formatted input [input], 
will create an excel sheet
from this at the path [path] with the name [filename]

On success, returns the file path. On failure, 
returns None. 
'''
def createExcelSheet(output, filename, path):
    workbook = xlwt.Workbook()  
    
    sheet = workbook.add_sheet("Test") 
    
    # Specifying style 
    style = xlwt.easyxf('font: bold 1') 
    
    headers = ["Crime Type", "Result", "Convict Date", "Offense", "Offense Code", "Probation Status", "Expungement Result", "Expungment Messages"]

    assert len(output) > 0
    assert len(headers) == len(output[0])

    for i in range(len(headers)):
        header = headers[i]
        sheet.write(i, 0, header, style) 

    next_row = 1
    for crime in output:
        sheet.write(0, next_row, crime.crime_type, style)
        sheet.write(1, next_row, crime.result, style)
        sheet.write(2, next_row, crime.convict_date, style)
        sheet.write(3, next_row, crime.offense, style)
        sheet.write(4, next_row, crime.offense_code, style)
        sheet.write(5, next_row, crime.prob_status, style)
        sheet.write(6, next_row, crime.expunge_result, style)
        sheet.write(7, next_row, crime.expunge_messages, style)
        next_row = new_row + 1
        
    # Writting on specified sheet 
    if(path[-1] != "/"):
        path = path + "/"
    workbook.save(path + filename)

if __name__ == "__main__":
    given = rs.Rapsheet(
        [
            rs.Crime("Felony", "County Jail", week_ago, None, "Not Completed", True),
        ])
    expected = [
        [[COUNTY_JAIL_DISC], "Discretionary"],
    ]
    x = formatOutput((given, expected))
    path = createExcelSheet(x, "test.xls", "tests")
    print path
