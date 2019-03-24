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

def assertResult(given, expected_messages, expected_result):
    result = r.result(given)
    assert result["messages"] == expected_messages
    assert result["result"] == expected_result

def test_infraction_not_eligible():
    given = rs.RapSheet(
        [
            rs.Crime("Infraction", "Fine", week_ago, None, None, None)
        ])
    assertResult(given, [], "Not Eligible")

def test_infraction_mandatory():
    given = rs.RapSheet(
        [
            rs.Crime("Infraction", "Fine", two_years_ago, None, None, None)
        ])
    assertResult(given, [], "Mandatory")

def test_infraction_discretionary():
    given = rs.RapSheet(
        [
            rs.Crime("Infraction", "Fine", two_years_ago, None, None, None), 
            rs.Crime("Infraction", "Fine", week_ago, None, None, None)
        ])
    assertResult(given, [], "Discretionary")

def test_misdemeanor_discretionary():
    given = rs.RapSheet(
        [
            rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None), 
            rs.Crime("Infraction", "Fine", week_ago, None, None, None)
        ])
    assertResult(given, [], "Discretionary")

def test_misdemeanor_mandatory():
    given = rs.RapSheet(
        [
            rs.Crime("Misdemeanor", "Up To A Year In County Jail", two_years_ago, None, None, None), 
        ])
    assertResult(given, [], "Mandatory")

def test_misdemeanor_not_eligible():
    given = rs.RapSheet(
        [
            rs.Crime("Misdemeanor", "Up To A Year In County Jail", week_ago, None, None, None), 
        ])
    assertResult(given, [], "Not Eligible")

def test_misdemeanor_mandatory2():
    given = rs.RapSheet(
        [
            rs.Crime("Misdemeanor", "Probation", week_ago, None, None, None), 
        ])
    assertResult(given, [], "Mandatory")

def test_misdemeanor_mandatory3():
    given = rs.RapSheet(
        [
            rs.Crime("Misdemeanor", "Probation", week_ago, None, None, "Early Termination"), 
        ])
    assertResult(given, [], "Mandatory")

def test_misdemeanor_mandatory4():
    given = rs.RapSheet(
        [
            rs.Crime("Misdemeanor", "Probation", week_ago, None, None, "Not Completed"), 
        ])
    assertResult(given, [], "Discretionary")

def test_felony_mandatory2():
    given = rs.RapSheet(
        [
            rs.Crime("Felony", "Probation", week_ago, None, None, "Completed"), 
        ])
    assertResult(given, [], "Mandatory")

def test_felony_mandatory3():
    given = rs.RapSheet(
        [
            rs.Crime("Felony", "Probation", week_ago, None, None, "Early Termination"), 
        ])
    assertResult(given, [], "Mandatory")


def test_felony_discr():
    given = rs.RapSheet(
        [
            rs.Crime("Felony", "Probation", week_ago, None, None, "Not Completed"), 
        ])
    assertResult(given, [], "Discretionary")

def test_felony_county_discr():
    given = rs.RapSheet(
        [
            rs.Crime("Felony", "County Jail", week_ago, "non_violent, non_serious", None, "Not Completed"), 
        ])
    assertResult(given, [], "Discretionary")
