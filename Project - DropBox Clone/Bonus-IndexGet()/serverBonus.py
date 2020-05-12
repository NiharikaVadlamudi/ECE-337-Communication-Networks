import os 
import glob 
import sys 
import re 
import datetime
import hashlib
import json
import socket
from os.path import basename
from os.path import getmtime
from datetime import datetime

# else:
#     print('Some Error in function..')
#     print('Exiting...')
#     client.close()
#     sys.exit(0)  


# '/home/niharika/Desktop/CN Project'

#Functions in various file - Make sure you are in the same dirctory ..
from indexgetF import check,indexGet


#Global variables...
BUFFER_SIZE=1024
CLIENTS=10

host= socket.gethostbyname(socket.gethostname())
if host.startswith('127.0.'):
    host= '0.0.0.0'


def socketCreation():
    folder=input('Absolute Shared Folder Path:')
    port=int(input('Port Number:'))

    #Check if the folder has permissions -here
    try:
        assert(os.path.exists(folder))
    except:
        print('Invalid Path to Folder / No Access to the folder')
        print('Exiting..')
        sys.exit(0)

    try:
        server=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    except:
        print('Socket Creation Error')
        print('Exiting..')
        sys.exit(0)

    print('Socket Created..')

    try:
        server.bind((host,port))
        server.listen(10)
    except:
        print('Error while listening...')


    # Client got connected
    while(True):
        client,ipAdd=server.accept()
        print('Connection made to',str(ipAdd))
        while(True):
            try:
                args=client.recv(1024)
                args=args.decode('utf-8')
                print('Recieved argument..')
            except:
                print('Waiting for command..')
                continue
            
            print(args)
            cmd=args.strip('"').split(' ')
            print(cmd)

            print('Processing the query..')
            if(len(cmd)==0 or cmd[0]=='quit'):
                print('Client Connection is closing down..')
                client.close()

            else:
                if(cmd[0]=='indexGet'):
                    flagtype=cmd[1]
                    if(flagtype=='shortlist'):
                        if(len(cmd)>=6):
                            starttime=cmd[2]+' '+cmd[3]
                            endtime=cmd[4]+' '+cmd[5]
                            if(len(cmd)>6):
                                bonus=cmd[6]
                            else:
                                bonus=None
                            #Calling the actual funciton.
                            jdata=indexGet('shortlist',startTime=starttime,endTime=endtime,dataPath=folder,bonus=bonus)
                            if not jdata:
                                print('Function not working - checkall')
                            client.send(jdata.encode()) 

                    elif(flagtype=='longlist'):
                        if(len(cmd)>2):
                            bonus='.txt'
                            jdata=indexGet('longlist',startTime=0,endTime=0,dataPath=folder,bonus=bonus)
                        else:
                            jdata=indexGet('longlist',startTime=0,endTime=0,dataPath=folder,bonus=None)
                        
                        if not jdata:
                            print('NOPE FUNCTION NOT WORKING')

                        client.send(jdata.encode())
                    else:
                        print('Invalid Arguments..')
                        print('Exiting..')
                        client.close()
                        sys.exit(0)    
                else:
                    print('Invalid Functional Arguments.')    
                    client.close()
                    break
                                
    print('Closing ..')
    client.close()




print('Index Get File Checked..')

def main():
    print('Testing starts..')
    socketCreation()
    print('Testing completed..')
    
if __name__ == "__main__":
   main()

