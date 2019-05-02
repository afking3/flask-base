import ruleset as rs
import vision
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
    rapsheet = vision.detect_document(rap)
    rules = rs.RuleSet()
    rapsheet_results = rules.resultsFromRapSheet(rapsheet)

    print("------------------------")
    for crime in rapsheet.crimes:
        crime.printCrime()
    print("------------------------")
    print(rapsheet_results)
    print("------------------------")

    return (rapsheet, rapsheet_results)

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
        #print(crime)
        new_obj = {}
        new_obj["crime_type"] = crime.crime_type
        temp = ""
        if crime.result["probation"] and crime.result["probation"] != "none":
            temp += crime.result["probation"] + " "
        if crime.result["jail"] and crime.result["jail"] != "none":
            temp += crime.result["jail"] + " "
        if crime.result["fine"] and crime.result["fine"] != "none":
            temp += "Fine "
        if temp == "":
            temp = "No Result?"
        new_obj["result"] = temp
        new_obj["convict_date"] = crime.conviction_date
        new_obj["offense_code"] = crime.offense_code
        new_obj["prob_status"] = crime.probation_status
        result = results[index]
        new_obj["expunge_result"] = result["result"]
        new_obj["expunge_messages"] = result["messages"]
        #new_obj["expunge_result"] = ""
        #new_obj["expunge_messages"] = ""
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

    headers = ["Crime Type", "Result", "Convict Date", "Offense Code", "Probation Status", "Expungement Result", "Expungment Messages"]

    assert len(output) > 0
    assert len(headers) == len(output[0])

    for i in range(len(headers)):
        header = headers[i]
        sheet.write(0, i, header, style)

    next_row = 1
    for crime in output:
        sheet.write(next_row, 0,  crime["crime_type"], style)
        sheet.write(next_row, 1, crime["result"], style)
        sheet.write(next_row, 2, crime["convict_date"], style)
        sheet.write(next_row, 3, crime["offense_code"], style)
        sheet.write(next_row, 4, crime["prob_status"], style)
        sheet.write(next_row, 5, crime["expunge_result"], style)
        sheet.write(next_row, 6, crime["expunge_messages"], style)
        next_row = next_row + 1

    # Writting on specified sheet
    if(path[-1] != "/"):
        path = path + "/"
    workbook.save(path + filename)
    return path + filename

if __name__ == "__main__":
    rap = rs.Rapsheet(
        [
            rs.Crime("Felony", "County Jail", "empty", None, "Not Completed", True),
        ])
    res = [
        [["dis"], "Discretionary"],
    ]
    x = formatOutput((rap, res))
    path = createExcelSheet(x, "test2.xls", "tests")
    print(path)
    x, y = getOutputFromRapsheet("google_vision/pdf/Sample RAP Sheet-rotated (1).pdf")
    print(x, y)
