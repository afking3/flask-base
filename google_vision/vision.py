import io
import os
import json

from google.oauth2 import service_account
from google.cloud import vision


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
                    
                    #Check line for convict's name
                    if 'NAM/001' in para:
                        info['Name']=para.split("NAM/001",1)[1]

                    if prev_line is not None and ('ARR/DET/CITE:' in prev_line or "COURT" in prev_line):
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
    print(paragraphs)
    info=json.dumps(info)
    parsed = json.loads(info)
    # print(json.dumps(parsed, indent=4, sort_keys=True))
    # print(info)
    return info
    #print(lines)

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

    
        

detect_document()

# info={'Crimes':{}}
# detect_document(r"images/Sample RAP Sheet-rotated-3.jpg", info)
