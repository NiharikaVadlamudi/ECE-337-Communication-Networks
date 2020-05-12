import os 
import glob 
import sys 
import re 
import datetime
import hashlib
import json
from os.path import basename
from os.path import getmtime
from datetime import datetime

'''
Foot Notes : 
1. md5 hash function is a lil in depth stuff , it works on chunks and internal mechanisms . 
2 . Reading through it.
3.hash()->handles large files too .
4.Need to check both 

# Everthing works fine , need to add assertions & error handling stuff.

'''


def hash(file,chunk=1024):
    md5_hash=hashlib.md5()
    with open(file,'rb') as f:
        for byte_block in iter(lambda:f.read(chunk),b""):
            md5_hash.update(byte_block)
    return(md5_hash.hexdigest())

# /home/niharika/Desktop/CN Project

def fileHash(flagType,fileName=None,dirPath=None):

    if(flagType=='verify'):
        filePath=dirPath+'/'+str(fileName)

    res=[]
    fileNames=[]

    if(dirPath!=None and flagType=="checkall"):
        fileNames=glob.glob(dirPath+'/'+'*')
 
    if(flagType=='verify'):
        hashval=hash(filePath)
        res.append({"File Hash : ":hashval,"Modified Timestamp : ":datetime.fromtimestamp(os.path.getmtime(filePath)).strftime("%m/%d/%Y, %H:%M:%S")})

    if(flagType=='checkall'):
        os.chdir(dirPath)
        for file in fileNames:
            if(os.path.isfile(file)):
                hashmap=hash(file)
                res.append({"File Name : ":basename(file),"File Hash : ":hashmap,"Modified Timestamp : ":datetime.fromtimestamp(os.path.getmtime(file)).strftime("%m/%d/%Y, %H:%M:%S")})

    #Dump into json file .
    data=json.dumps(res,indent=4)
    return(data)

# # #Main function
# def main():
#     print("Testing function ..")
#     #Calling the function 
#     dirpath="/home/niharika/Desktop/CN Project"
#     filename=''
#     m=fileHash('checkall',filename,dirpath)
#     data=json.loads(m)
#     print(data)
#     for it in range(len(data)):
#         print(it + 1)
#         for tmp in data[it]:
#             print(tmp + " " + str(data[it][tmp]))

    

# if __name__ == "__main__":
#     main()
