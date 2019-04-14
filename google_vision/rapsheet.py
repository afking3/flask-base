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

    


class Crime(object):
    date = None
    offense_code = ""
    offense_description = ""
    dispo = ""
    def __init__(self):
        pass
    
    def set_offense_code(self, ccode):
        self.offense_code = ccode

    def set_offense_description(self, description):
        self.offense_description = description

    def set_dispo(self, dispo):
        self.dispo = dispo
    
    def set_date(self, date):
        year = date[0:3]
        month  = date[4:6]
        day = date[7:]
        self.date = datetime.date(int(year), int(month), int(day))
    
    