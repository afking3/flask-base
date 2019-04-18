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
from sort import wordBoxSort


CREDENTIALS = service_account.Credentials.from_service_account_file('NLSLA Re-entry-88f1acf99097.json')

CLIENT = vision.ImageAnnotatorClient(credentials=CREDENTIALS)





def detect_document():
    #initialize dictionary [info] with empty crimes field
    #and set [crime_count] to 0 and [pastNameAndDOB] to false
    info={'Courts':{}}
    Courts={}
    Crimes={}
    court_count=0
    crime_count=0
    lastDate=None

    rapsheet = Rapsheet()

    #[pastNameAndDOB] signifies whether the name and
    #date of birth have been found yet
    pastNameAndDOB=False

    #Iterate over the images in the "images" directory
    for pageCount, path in enumerate(os.listdir("images")):
        """Detects document features in an image."""
        
        with io.open(path, 'rb') as image_file:
            content = image_file.read()
            
        response = get_response(content)

        words = get_words(response)

        for i in range(len(words)):
            if words[i] == 'NAM/001':
                rapsheet.set_name(words[i+1] + words[i+2])

            if ('ARR/DET/CITE:' in prev_line or "COURT" in prev_line):
                if lastDate is not None:
                    Courts[str(court_count)]={"Date":lastDate ,"Crimes":removeDupCrimes(Crimes)}
                    Crimes={}
                    crime_count=0
                    court_count+=1

                lastDate= getDate(para)
                if lastDate is None:
                    continue
                
                

            #Check line for convict's occupation, if found set
            #pastNameAndDOB to true.
            if 'OCC/' in para:
                info['Occupation']=para.split("OCC/",1)[1]
                pastNameAndDOB=True

            #Start looking for information in past crimes

            if pastNameAndDOB or pageCount>0:
                #Check for crime and get PC.
                #PC stands for penal code
                if 'PC-' in para:
                    code=para.split("PC",1)[0]
                    crime_type=para.split("PC",1)[1]
                    if 'DISPO' in crime_type:
                        crime_type=crime_type.split("DISPO:",1)[0]
                    crime_count+=1
                    Crimes[str(crime_count)]={"Code":str(code), "Type":crime_type}
                    #Check for DISPO and add to info.
                    #DISPO is disposition
                    if 'DISPO' in para:
                        crime=Crimes[str(crime_count)]
                        crime["DISPO"]=para.split("DISPO:",1)[1]

                #TODO: Refactor this
                if 'PC' in para:
                    code=para.split("PC",1)[0]
                    crime_type=para.split("PC",1)[1]
                    if 'DISPO' in crime_type:
                        crime_type=crime_type.split("DISPO:",1)[0]
                    crime_count+=1
                    Crimes[str(crime_count)]={"Code":str(code), "Type":crime_type}
                    if 'DISPO' in para:
                        crime=Crimes[str(crime_count)]
                        crime["DISPO"]=para.split("DISPO:",1)[1]
                elif 'DISPO' in para:
                    if crime_count==0:
                        crime={}
                    else:
                        crime=Crimes[str(crime_count)]
                    crime["DISPO"]=para.split("DISPO:",1)[1]
                
                if 'CONV STATUS' in para:
                    convictionStatus=para.split("STATUS",1)[1].split("SEN",1)[0]
                    if crime_count==0:
                        crime={}
                    else:
                        crime=Crimes[str(crime_count)]
                    crime["CONV"]=convictionStatus
                
                if 'SEN' in para:
                    sentence=para.split("STATUS",1)[1].split("PROBATION",1)[0]
                    start=0
                    for index, character in enumerate(sentence):
                        if character.isdigit():
                            start=index
                            break
                    sentence = sentence[index:]
                    if crime_count==0:
                        crime={}
                    else:
                        crime=Crimes[str(crime_count)]
                    crime["PROBATION"]=sentence

                
                prev_line=para
                   
    info['Courts']=Courts
    
    info=json.dumps(info)
    parsed = json.loads(info)
    print(json.dumps(parsed, indent=4, sort_keys=True))
    # print(info)
    return info
    #print(lines)

# def codeChecker (codeType, line, Crimes):


def removeDupCrimes (Crimes): 
    newCrimes={}

    for key,value in Crimes.items():
        if value["Type"]!="":
            if value not in newCrimes.values():
                newCrimes[key] = value

    return newCrimes

def getDate(dateString):
    numCount=0
    for i, c in enumerate(dateString):
        if c.isdigit():
            numCount+=1
        else:
            numCount=0
        if numCount==7:
            dateString=dateString[i-7:i+2]
            year=dateString[:5]
            month=dateString[5:7]
            day=dateString[7:]
            date={"Month":month, "Day":day, "Year":year}
            return date

    return None

"""
 **************************
 NEW STUFF
***************************
"""

"""
Outputs the response from google vision as a list of words.
"""
def get_words(response):
    breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType
    tokens = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                para = ""
                line = ""
                token = ""
                for word in paragraph.words:
                    for symbol in word.symbols:
                        token += symbol.text
                        if symbol.property.detected_break.type in [breaks.SPACE, breaks.EOL_SURE_SPACE, breaks.LINE_BREAK]:
                            tokens.append(token)
                            token = ""
    return tokens

def getBoundBoxes(response):
    tokens = []
    for page in response.full_text_annotation.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                para = ""
                line = ""
                token = ""
                for word in paragraph.words:
                    #print(word.bounding_box)
                    tokens.append(word)
    return tokens

def getWordFromBox(box):
    breaks = vision.enums.TextAnnotation.DetectedBreak.BreakType
    token=""
    for symbol in box.symbols:
        token += symbol.text
        if symbol.property.detected_break.type in [breaks.SPACE, breaks.EOL_SURE_SPACE, breaks.LINE_BREAK]:
            return token


def get_response(image):
    img = vision.types.Image(content=image)


    return CLIENT.document_text_detection(image=img)

def matches(word1, word2):
    return word1 == word2 or word_similarity.check_word_against_term(word1, word2)


"""Simplifies getting a list of crimes for a single citation
Returns index, crime list"""
def get_crimes(line_index, word_index, line_list):
    #index is the index of "Court:"    
    crimes = []
    line_index+=1
    date=line_list[line_index][0]
    print(date)
    
    # TODO: this part
    while ( not matches('ARR/DET/CITE:', line_list[line_index][word_index])): 
        if matches(line_list[line_index][word_index], '001'):
            crime = Crime()
            crime.set_date(date)
            index = line_list.index("_newline", index)+1 #at offense code
            crime.set_offense_code(line_list[index])
            crime_desc = ""
            while (line_list[index] != "_newline"):
                crime_desc += "" if 'TOC:' in line_list[index] else line_list[index]
                index += 1
            crime.set_offense_description = crime_desc




"""
Takes in a list of words sorted by y-position and converts into lines

"""
def sepIntoLines (words):
    lines=[]
    line=[]
    lastY=words[0].bounding_box.vertices[3].y
    for word in words:
        if word is not None:
            currY=word.bounding_box.vertices[3].y
            if abs(currY - lastY )> 10:
                lines.append(line)
                line=[]
                print(getWordFromBox(word))
            
            # str_word is the string form of box
            str_word=getWordFromBox(word)
            if str_word is not None:
                line.append(str_word)
            lastY=currY
    if(len(line) > 0):
        lines.append(line)
    return lines

bad_words={':',"", "-",",", "*"}

def is_clean(word):
    return not (word in bad_words)

def sanitize (doc):
    new_doc=[]
    for line in doc:
        new_doc.append(list(filter(lambda a: is_clean(a),line)))
    
    return new_doc

def parse_document(filename):
    entire_doc = []
    imgs = file_handling.open_file(filename)
    for img in imgs:
        boxes=getBoundBoxes(get_response(img))
        wordBoxSort(boxes)
        entire_doc +=boxes 
    entire_doc=sepIntoLines(entire_doc)

    for line in entire_doc:
        for word in line:
            if type(word)==str:
                word=word.encode('UTF-8')
    
    entire_doc=sanitize(entire_doc)

    print(entire_doc)

    # print(entire_doc)

    rapsheet = Rapsheet()

    i = 0
    j = 0
    while i < len(entire_doc):
        while j < len(entire_doc[i]):
            if (len(entire_doc[i][j])==len("COURT") and matches(entire_doc[i][j],"COURT")):
                line_index,word_index, crimes = get_crimes(i, j, entire_doc)
            
            j += 1
        j=0
        i += 1

    print(rapsheet.name)


#if __name__ == "__main__":
    parse_document("sample rap sheet.pdf")
