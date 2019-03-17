import sys
sys.path.insert(0, '../')
import ruleset
import datetime
from dateutil.relativedelta import relativedelta

now = datetime.datetime.now()
week_ago = now - datetime.timedelta(days=7)
one_year_ago = now - relativedelta(years=1)
two_years_ago = now - relativedelta(years=2)

r = ruleset.RuleSet()

def assertResult(given, expected_messages, expected_result):
    result = r.result(given)
    assert result["messages"] == []
    assert result["result"] == "Discretionary"

def test_e():
    print("hi")
    assert ruleset.dummy_input != None

def test_infraction_not_eligible():
    given = {"crimes":
            [{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }
    assertResult(given, [], "Not Eligible")

def test_infraction_mandatory():
    given = {"crimes":
            [{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": two_years_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }
    assertResult(given, [], "Mandatory")

def test_infraction_discretionary():
    given = {"crimes":
            [{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": two_years_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            },{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }
    assertResult(given, [], "Discretionary")

def test_misdemeanor_discretionary():
    given = {"crimes":
            [{
                "crime_type": "Misdemeanor",
                "result": "Up To A Year In County Jail",
                "conviction_date": two_years_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            },{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }
    assertResult(given, [], "Discretionary")

def test_misdemeanor_mandatory():
    given = {"crimes":
            [{
                "crime_type": "Misdemeanor",
                "result": "Up To A Year In County Jail",
                "conviction_date": two_years_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }
    assertResult(given, [], "Mandatory")

def test_misdemeanor_not_eligible():
    given = {"crimes":
            [{
                "crime_type": "Misdemeanor",
                "result": "Up To A Year In County Jail",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }

    assertResult(given, [], "Not Eligible")

def test_misdemeanor_mandatory2():
    given = {"crimes":
            [{
                "crime_type": "Misdemeanor",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Completed"
            }]
        }

    assertResult(given, [], "Mandatory")

def test_misdemeanor_mandatory3():
    given = {"crimes":
            [{
                "crime_type": "Misdemeanor",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Early Termination"
            }]
        }
    
    assertResult(given, [], "Mandatory")

def test_misdemeanor_mandatory4():
    given = {"crimes": [{
                "crime_type": "Misdemeanor",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Not Completed"
            }]}
    assertResult(given, [], "Discretionary")

def test_felony_mandatory2():
    given = {"crimes":
            [{
                "crime_type": "Felony",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Completed"
            }]
        }

    assertResult(given, [], "Mandatory")


def test_felony_mandatory3():
    given = {"crimes":
            [{
                "crime_type": "Felony",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Early Termination"
            }]
        }

    assertResult(given, [], "Mandatory")


def test_felony_discr():
    given = {"crimes":
            [{
                "crime_type": "Felony",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Not Completed"
            }]
        }

    assertResult(given, [], "Discretionary")

def test_felony_county_discr():
    given = {"crimes":
            [{
                "crime_type": "Felony",
                "result": "County Jail",
                "conviction_date": week_ago,
                "offense": "non_violent, non_serious",
                "offense_code": None,
                "probation_status": "Not Completed"
            }]
        }

    assertResult(given, [], "Discretionary")
