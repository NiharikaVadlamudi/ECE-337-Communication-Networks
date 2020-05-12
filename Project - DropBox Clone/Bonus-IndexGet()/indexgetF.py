import os 
import glob 
import sys 
import re 
from os.path import getmtime
from datetime import datetime
import json



def check(file,keyword):
    with open(file) as f:
        datafile = f.readlines()
    for line in datafile:
        if keyword in line:
            return True
    return False


def indexGet(flagType,startTime=0,endTime=0,dataPath='',bonus=None,keyWord='Programmer'):
    #Result 
    res=[]
    fileNames=[]

    #Error Testing .
    try : 
        assert(os.path.exists(dataPath))
    except:
        res=[]
        res.append("Invalid Directory")
        data=json.dumps(res,indent=4)
        return(data)
    
    

    if(bonus==None):
        fileNames=os.listdir(dataPath)
    else:
        if(bonus!=None):
            fileNames=[file for file in os.listdir(dataPath) if file.endswith(str(bonus))]
    
    #Case 1 : Shortlist , bonus invariant.
    if(flagType=="shortlist"):
        os.chdir(dataPath)
        for f in fileNames:
            statObj=os.stat(str(f))
            startTime=startTime.strip('[').strip(']')
            endTime=endTime.strip('[').strip(']')

            stmp=datetime.strptime(startTime,'%Y-%m-%d %H:%M:%S')
            endtmp=datetime.strptime(endTime,'%Y-%m-%d %H:%M:%S')
            curtmp=datetime.strptime(str(datetime.fromtimestamp(int(os.path.getmtime(f)))),'%Y-%m-%d %H:%M:%S')
            dt_object=datetime.fromtimestamp(statObj.st_mtime)

            if( (curtmp>stmp) and (curtmp<endtmp)) :
                res.append ( {  "Name: " : f[:f.find('.')],
                                "Size: " : statObj.st_size,
                                "Timestamp: " : dt_object.strftime('%Y-%m-%d %H:%M:%S'),
                                "File Format: ": f[f.find('.'):] 
                            } )
                
    #Case 2 : Longlist , bonus invariant.
    if(flagType=="longlist" and bonus==".txt"):
        os.chdir(dataPath)
        for f in fileNames:
            isOpen=check(str(dataPath)+'/'+f,keyWord)
            if(isOpen):
                statObj=os.stat(str(dataPath)+'/'+f)
                dt_object =datetime.fromtimestamp(statObj.st_mtime)
                res.append ( {  "Name: " : f[:f.find('.')],
                                "Size: " : statObj.st_size,
                                "Timestamp: " : dt_object.strftime('%Y-%m-%d %H:%M:%S'),
                                "File Format: ": f[f.find('.'):] 
                             } )

    #Case 3: Longlist, NO bonus
    #Case 2 : Longlist , bonus invariant.
    if(flagType=="longlist" and bonus==None):
        os.chdir(dataPath)
        for f in fileNames:
            statObj=os.stat(str(dataPath)+'/'+f)
            dt_object =datetime.fromtimestamp(statObj.st_mtime)
            res.append ( {  "Name: " : f[:f.find('.')],
                            "Size: " : statObj.st_size,
                            "Timestamp: " : dt_object.strftime('%Y-%m-%d %H:%M:%S'),
                            "File Format: ": f[f.find('.'):] 
                         } )


    data=json.dumps(res,indent=4)
    return(data)


    
    










