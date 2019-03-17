import sys
sys.path.insert(0, '../')
import ruleset
import datetime

now = datetime.datetime.now()
week_ago = now - datetime.timedelta(days=7)
one_year_ago = now - datetime.timedelta(years=1)
two_years_ago = now - datetime.timedelta(years=2)

r = ruleset.RuleSet()

def test_e():
    print("hi")
    assert ruleset.dummy_input != None

def test_infraction_not_eligible():
    given = 
        {"crimes": 
            [{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Not Eligible"

def test_infraction_mandatory():
    given = 
        {"crimes": 
            [{
                "crime_type": "Infraction",
                "result": "Fine",
                "conviction_date": two_years_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }

    result = r.result(given)
    assert result.messages == []
    assert result.res == "Mandatory"

def test_infraction_discretionary():
    given = 
        {"crimes": 
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

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Discretionary"


def test_misdemeanor_discretionary():
    given = 
        {"crimes": 
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

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Discretionary"


def test_misdemeanor_mandatory():
    given = 
        {"crimes": 
            [{
                "crime_type": "Misdemeanor",
                "result": "Up To A Year In County Jail",
                "conviction_date": two_years_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }

    result = r.result(given)
    assert result.messages == []
    assert result.res == "Mandatory"

def test_misdemeanor_not_eligible():
    given = 
        {"crimes": 
            [{
                "crime_type": "Misdemeanor",
                "result": "Up To A Year In County Jail",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": None
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Not Eligible"


def test_misdemeanor_mandatory2():
    given = 
        {"crimes": 
            [{
                "crime_type": "Misdemeanor",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Completed"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Mandatory"

def test_misdemeanor_mandatory3():
    given = 
        {"crimes": 
            [{
                "crime_type": "Misdemeanor",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Early Termination"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Mandatory"

def test_misdemeanor_mandatory4():
    given = 
        {"crimes": 
            [{
                "crime_type": "Misdemeanor",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Not Completed"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Discretionary"

def test_felony_mandatory2():
    given = 
        {"crimes": 
            [{
                "crime_type": "Felony",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Completed"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Mandatory"

def test_felony_mandatory3():
    given = 
        {"crimes": 
            [{
                "crime_type": "Felony",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Early Termination"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Mandatory"

def test_felony_discr():
    given = 
        {"crimes": 
            [{
                "crime_type": "Felony",
                "result": "Probation",
                "conviction_date": week_ago,
                "offense": None,
                "offense_code": None,
                "probation_status": "Not Completed"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Discretionary"

def test_felony_county_discr():
    given = 
        {"crimes": 
            [{
                "crime_type": "Felony",
                "result": "County Jail",
                "conviction_date": week_ago,
                "offense": "non_violent, non_serious",
                "offense_code": None,
                "probation_status": "Not Completed"
            }]
        }

    result = r.result(given)
    assert result.messages == [] 
    assert result.res == "Discretionary"