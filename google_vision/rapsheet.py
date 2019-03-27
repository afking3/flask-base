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
    def __init__(self):
        pass
    
    def set_type(self, ctype):
        self.crime_type = ctype

    def set_result(self, result):
        self.result = result
    
    #Sets date. Takes a rapsheet-formatted date (yyyymmdd)
    #def
    
    