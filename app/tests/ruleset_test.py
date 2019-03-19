import sys
sys.path.insert(0, '../')
import ruleset as rs 
import datetime
from dateutil.relativedelta import relativedelta

now = datetime.datetime.now()
week_ago = now - datetime.timedelta(days=7)
one_year_ago = now - relativedelta(years=1)
two_years_ago = now - relativedelta(years=2)

r = rs.RuleSet()


def assertResults(rapsheet, list_of_expected): 
    #expected_messages, expected_result):
    results = r.resultsFromRapSheet(rapsheet)
    for i in range(len(results)):
        result = results[i]
        expected_result = list_of_expected[i]
        assert result["messages"] == expected_result[0]
        assert result["result"] == expected_result[1]

def test_infraction_not_eligible():
    given = rs.Rapsheet(
        [
            rs.Crime("Infraction", "Fine", week_ago, None, None, None)
        ])
    expected = [
        [[], "Not Eligible"]
    ]

    assertResults(given, expected)

def test_infraction_mandatory():
    given = rs.Rapsheet(
        [
            rs.Crime("Infraction", "Fine", two_years_ago, None, None, None)
        ])
    expected = [
        [[],  "Mandatory"]
    ]
    assertResults(given, expected)

def test_infraction_discretionary():
    given = rs.Rapsheet(
        [
            rs.Crime("Infraction", "Fine", two_years_ago, None, None, None), 
            rs.Crime("Infraction", "Fine", week_ago, None, None, None)
        ])
    #Fix this test
    expected = [
        [[], "Discretionary"], 
        [[], "Not Eligible"]
    ]
    assertResults(given, expected)

def test_misdemeanor_discretionary():
    given = rs.Rapsheet(
        [
            rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None), 
            rs.Crime("Infraction", "Fine", week_ago, None, None, None)
        ])
    expected = [
        [[], "Discretionary"], 
        [[], "Not Eligible"]
    ]
    assertResults(given, expected)

def test_misdemeanor_mandatory():
    given = rs.Rapsheet(
        [
            rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None), 
        ])
    expected = [
        [[], "Mandatory"], 
    ]
    assertResults(given, expected)

def test_misdemeanor_not_eligible():
    given = rs.Rapsheet(
        [
            rs.Crime("Misdemeanor", "Up To A Year In County Jail", week_ago, None, None, None), 
        ])
    expected = [
        [[], "Not Eligible"], 
    ]
    assertResults(given, expected)

def test_misdemeanor_mandatory2():
    given = rs.Rapsheet(
        [
            rs.Crime("Misdemeanor", "Probation", week_ago, None, None, "Completed"), 
        ])
    expected = [
        [[], "Mandatory"], 
    ]
    assertResults(given, expected)

def test_misdemeanor_mandatory3():
    given = rs.Rapsheet(
        [
            rs.Crime("Misdemeanor", "Probation", week_ago, None, None, "Early Termination"), 
        ])
    expected = [
        [[], "Mandatory"], 
    ]
    assertResults(given, expected)

def test_misdemeanor_mandatory4():
    given = rs.Rapsheet(
        [
            rs.Crime("Misdemeanor", "Probation", week_ago, None, None, "Not Completed"), 
        ])
    expected = [
        [[], "Discretionary"], 
    ]
    assertResults(given, expected)

def test_felony_mandatory2():
    given = rs.Rapsheet(
        [
            rs.Crime("Felony", "Probation", week_ago, None, None, "Completed"), 
        ])
    expected = [
        [[], "Mandatory"], 
    ]
    assertResults(given, expected)

def test_felony_mandatory3():
    given = rs.Rapsheet(
        [
            rs.Crime("Felony", "Probation", week_ago, None, None, "Early Termination"), 
        ])
    expected = [
        [[], "Mandatory"], 
    ]
    assertResults(given, expected)


def test_felony_discr():
    given = rs.Rapsheet(
        [
            rs.Crime("Felony", "Probation", week_ago, None, None, "Not Completed"), 
        ])
    expected = [
        [[], "Discretionary"], 
    ]
    assertResults(given, expected)

def test_felony_county_discr():
    given = rs.Rapsheet(
        [
            rs.Crime("Felony", "County Jail", week_ago, "non_violent, non_serious", None, "Not Completed"), 
        ])
    expected = [
        [[], "Discretionary"], 
    ]
    assertResults(given, expected)