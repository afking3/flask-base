import io
import os
import json
import re
import time
from rapsheet import Rapsheet, Crime
import file_handling
import word_similarity
from google.oauth2 import service_account
from google.cloud import vision

CREDENTIALS = service_account.Credentials.from_service_account_file('NLSLA Re-entry-88f1acf99097.json')

CLIENT = vision.ImageAnnotatorClient(credentials=CREDENTIALS)

def get_similar_word (term, line):  
    new_line=""
    if type(line) == list:
        for word in line:
            new_line+=word
        line=new_line

    words= line.split(":")
    new_words=[]
    for word in words:
        new_words+=word.split(" ")

    words=new_words
    for word in words:
        if matches(term, word):
            return word
    return None
    

def matches(word1, word2):
    return word1 == word2 or word_similarity.check_word_against_term(word1, word2)

# Checks if term is in a line
def check_if_term_present(term, line):
    if term in line:
        return True
    
    words= line.split(" ")
    new_words=[]
    for word in words:
        new_words+=word.split(":")

    words=new_words
    for word in words:
        if matches(term, word):
            return True 
    return False


def detect_document():
    #initialize dictionary [info] with empty crimes field
    #and set [crime_count] to 0 and [pastNameAndDOB] to false
    rapsheet = Rapsheet()
    crime = Crime()
    lastDate=None
    #[pastNameAndDOB] signifies whether the name and
    #date of birth have been found yet
    pastNameAndDOB=False

    #Iterate over the images in the "images" directory
    for pageCount, path in enumerate(os.listdir("images")):
        """Detects document features in an image."""
        

        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)

        response = CLIENT.document_text_detection(image=image)

        breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType
        paragraphs = []
        lines = []
        prev_line=None
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    para = ""
                    line = ""
                    for word in paragraph.words:
                        for symbol in word.symbols:
                            line += symbol.text
                            if symbol.property.detected_break.type == breaks.SPACE:
                                line += ' '
                            if symbol.property.detected_break.type == breaks.EOL_SURE_SPACE:
                                line += ' '
                                lines.append(line)
                                para += line
                                line = ''
                            if symbol.property.detected_break.type == breaks.LINE_BREAK:
                                lines.append(line)
                                para += line
                                line = ''
                    paragraphs.append(para)
                    #In this boilerplate code for Google Vision, a [para]
                    #is more akin to what we would call a line of text
                    
                    # TODO: Create a function for these checks and refactor
                    
                    #Skip if line contains this as it messes with DISPO 
                    #parsing

                    if "\xd3" in para or '\xc7' in para:
                        continue

                    if "NO LONGER INTERESTED" in para:
                        continue

                    if check_if_term_present("CERT BY CLERK OF THE COURT", para):
                        continue

                    #print(para)

                    #Check line for convict's name
                    if check_if_term_present('NAM/001', para):
                        rapsheet.set_name(para.split("NAM/001",1)[1])

                    if prev_line is not None and (check_if_term_present("COURT", prev_line) or check_if_term_present("COURT:", prev_line)):
                        lastDate= getDate(para)
                        if lastDate is None:
                            continue
                        
                        

                    #Check line for convict's occupation, if found set
                    #pastNameAndDOB to true.
                    if check_if_term_present("OCC/", para):
                        rapsheet.set_occupation(para.split("OCC/",1)[1])
                        pastNameAndDOB=True

                    #Start looking for information in past crimes

                    if pastNameAndDOB or pageCount>0:
                        #Check for crime and get PC.
                        #PC stands for penal code
                        if check_if_term_present('PC-', para):
                            if crime != Crime ():
                                rapsheet.add_crime(crime)
                                crime  = Crime()
                            crime.set_offense_code(para.split("PC-",1)[0])
                            if len(para.split("PC-",1)) > 1:
                                crime_type=para.split("PC-",1)[1]
                            crime.set_offense_description(crime_type)
                            if crime.dispo == "" and check_if_term_present("DISPO", para) or check_if_term_present("DISPO:", para):
                                crime.set_dispo(crime_type.split("DISPO",1)[1])
                            #Check for DISPO and add to info.
                            #DISPO is disposition
                            if crime.dispo == "" and 'DISPO' in para:
                                crime.set_dispo(para.split("DISPO",1)[1])
                            if lastDate is not None:
                                crime.set_date(lastDate)
                            rapsheet.add_crime(crime)
                            crime=Crime()
                            

                
                        if check_if_term_present('PC', para):
                            if crime != Crime ():
                                rapsheet.add_crime(crime)
                                crime  = Crime()
                            if lastDate is not None:
                                crime.set_date(lastDate)
                            code=para.split("PC",1)[0]
                            if len(para.split("PC",1)) > 1:
                                crime_type=para.split("PC",1)[1]
                            crime.set_offense_code(code)
                            crime.set_offense_description(crime_type)
                            if crime.dispo == "" and check_if_term_present("DISPO", crime_type) or check_if_term_present("DISPO:", crime_type):
                                crime.set_dispo(crime_type.split("DISPO:",1)[0])
                            if crime.dispo == "" and check_if_term_present("DISPO", para) or check_if_term_present("DISPO:", para):
                                crime.set_dispo(para.split("DISPO:",1)[1])
                            rapsheet.add_crime(crime)
                        
                        elif crime.dispo == "" and check_if_term_present("DISPO", para) or check_if_term_present("DISPO:", para):
                            if len(rapsheet.crimes)==0:
                                crime =Crime()
                            if len(para.split("DISPO:",1)) > 1:
                                crime.set_dispo(para.split("DISPO:",1)[1])
                                rapsheet.add_crime(crime)
                               
                            
                        

   
                        if check_if_term_present('VC-', para):
                            if crime != Crime ():
                                rapsheet.add_crime(crime)
                                crime  = Crime()
                            if lastDate is not None:
                              
                                crime.set_date(lastDate)
                            code=para.split("VC-",1)[0]
                            crime_type=para.split("VC-",1)[1]
                            crime.set_offense_code(code)
                            crime.set_offense_description(crime_type)
                            if crime.dispo=="" and check_if_term_present("DISPO", crime_type) or check_if_term_present("DISPO:", crime_type):
                                crime.set_dispo(crime_type.split(get_similar_word("DISPO", para),1)[0])
                            if crime.dispo=="" and check_if_term_present("DISPO", para) or check_if_term_present("DISPO:", para):
                                crime.set_dispo(para.split(get_similar_word("DISPO:", para),1)[1])
                            rapsheet.add_crime(crime)
                        elif crime.dispo=="" and check_if_term_present("DISPO", para) or check_if_term_present("DISPO:", para):
                            if len(rapsheet.crimes)==0:
                                crime = Crime()
                            else:
                                crimes=rapsheet.crimes
                                crime=crimes[len(crimes)-1]
                                crime.set_dispo(para.split(get_similar_word("DISPO", para),1)[1])
                            if len(para.split(get_similar_word("DISPO", para),1)) > 1:
                                crime.set_dispo(para.split(get_similar_word("DISPO", para),1)[1])

                        
                        if check_if_term_present('CONV STATUS', para) or check_if_term_present('CONV STATUS:', para):
                            convictionStatus=para.split("STATUS",1)[1]
                            convictionStatus=convictionStatus.split("SEN")[0]
                            if len(rapsheet.crimes)==0:
                                crime = Crime()
                            else:
                                crimes=rapsheet.crimes
                                crime=crimes[len(crimes)-1]
                            crime.set_crime_type(convictionStatus)
                        
                        if check_if_term_present('SEN', para) or check_if_term_present('SEN:', para):
                            crimes=rapsheet.crimes
                            if check_if_term_present("PROBATION",crime.result) or check_if_term_present("JAIL",crime.result):
                                continue
                            crime.set_result(para.split("SEN:")[1])


                        prev_line=para
        # print("page: "+str(pageCount))
        # print(paragraphs)
    
    rapsheet.crimes=clean_crimes(rapsheet.crimes)

    # print(info)
    return rapsheet
    #print(lines)

# def codeChecker (codeType, line, Crimes):

# Checks if crime has been entered twice
def dupCheck(crime, crimes):

    for cr in crimes:
        if crime.offense_code == cr.offense_code and crime.date == cr.date:
            return True

    return False
# Counts how many fields are filled
def countFields (crime):
    most=0
    if crime.offense_code is not "":
        most+=1
    if crime.offense_description is not "":
        most+=1
    if crime.crime_type is not "":
        most+=1
    if crime.result is not "":
        most+=1
    
    return most

# Gets crime with most information
def getBestCrime(crime, crimes):
    crimes=list(filter(lambda a:crime.offense_code == a.offense_code and crime.date == a.date, crimes))
    best=crime
    most=countFields(crime)
    for cr in crimes:
        curr = countFields(cr)
        if curr >= most:
            if best in crimes:
                crimes.remove(best)
            best=cr
            most=curr
    
    return best

# Removes duplicate crimes from [crimes]
def removeDupCrimes (crimes): 
    added=[]

    for crime in crimes:
        if not dupCheck(crime, added):
            added.append(getBestCrime(crime, crimes))

    return added


#Removes dispo information from offense description 
def dispo_clean(crime):

    if(crime.offense_description !="" and check_if_term_present("DISPO",crime.offense_description)):
        similar=get_similar_word("DISPO", crime.offense_description)
        desc_split=crime.offense_description.split(similar)
        if len(desc_split) > 1:
            crime.set_offense_description(desc_split[0])
            crime.set_dispo(desc_split[1])
    if(crime.dispo !="" and check_if_term_present("DISPO",crime.dispo)):
        similar=get_similar_word("DISPO", crime.dispo)
        if len(crime.dispo.split(similar))>1:
            crime.set_dispo(crime.dispo.split(similar)[1])

    return crime

# Cleans crimes parsed from rap sheet
def clean_crimes(crimes):
    list(filter(lambda a: a.offense_code!="", crimes))
    clean=[]
    for crime in crimes:
        if not crime.date == None:
            clean.append(crime)
    clean=removeDupCrimes(clean)

    for crime in crimes:
        crime=dispo_clean(crime)

    return clean

def getDate(dateString):
    numCount=0
    for i, c in enumerate(dateString):
        if c.isdigit():
            numCount+=1
        else:
            numCount=0
        if numCount==7:
            return dateString[i-6:i+2]

    return None

    
        
if __name__ == "__main__":
    detect_document().print()

# info={'Crimes':{}}
# detect_document(r"images/Sample RAP Sheet-rotated-3.jpg", info)