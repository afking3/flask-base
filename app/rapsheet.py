import datetime

class Rapsheet(object):
    crimes = []
    name = ""
    occ = ""
    def __init__(self):
        pass

    def set_name(self, name):
        self.name = name

    def set_occupation(self, occ):
        self.occ = occ

    def add_crime(self, crime):
        self.crimes.append(crime)

    def print_crimes(self):
        for crime in self.crimes:
            crime.print_crime()
            print("")



class Crime(object):
    date = None
    offense_code = ""
    offense_description = ""
    dispo = ""
    crime_type = ""
    result = ""
    def __init__(self):
        pass

    def set_offense_code(self, ccode):
        self.offense_code = ccode

    def set_offense_description(self, description):
        self.offense_description = description

    def set_dispo(self, dispo):
        self.dispo = dispo

    #Felony/Misdemeanor
    def set_crime_type(self, crime_type):
        self.crime_type=crime_type

    #Either convicted or dismissed or such
    def set_result(self, result):
        self.result=result

    def set_date(self, date):
        year = date[0:4]
        month  = date[4:6]
        day = date[6:]
        self.date = datetime.date(int(year), int(month), int(day))

    def print_crime(self):
        if self.date is not None:
            print("Date: "+self.date.strftime('%m/%d/%Y'))
        if self.offense_code is not None:
            print("Offense code: "+self.offense_code)
        if self.offense_description is not None:
            print("Offense description: "+self.offense_description)
        if self.dispo is not None:
            print("DISPO: "+self.dispo)
        if self.crime_type is not None:
            print("Type: "+self.crime_type)
        if self.result is not None:
            print("Result: "+self.result)
