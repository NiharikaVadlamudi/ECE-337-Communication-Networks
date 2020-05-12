# Listen to server and print out the data recieved by server...
import json 
import socket 
import os 
import glob 
import sys 
import re 
import datetime
from os.path import getmtime
from datetime import datetime


UDP_PORT=1996
BUFFER_SIZE=4096

host= socket.gethostbyname(socket.gethostname())
if host.startswith('127.0.'):
    host= '0.0.0.0'

def is_json(myjson):
  try:
    json_object = json.loads(myjson)
  except:
    return False
  return True


#How to recive arguments - INFO or FILE only 2 modes .
# data itself.
def recieveInfo(client,data):
    if not data: 
        print('No Data recived..')
        print('Exiting..')
        client.close()
        sys.exit(0)
        return
    
    elif not is_json and data :
        print(data)
    
    else:
        data=json.loads(data)
        #Printing out data..
        for i in range(len(data)):
            for tmp in data[i]:
                print(tmp+" "+str(data[i][tmp]))
            print('\n')
    return

def recieveFile(client,fileName,destinationFolder,datatype='TCP'):
    
    os.chdir(destinationFolder)
    #Open an empty file.
    f = open(fileName, 'wb')
	
    if(datatype=='TCP'):
        while(True):
            packet=client.recv(BUFFER_SIZE)
            if not packet or not is_json(packet): 
                recieveInfo(client,packet)
                break
            else:
                f.write(packet)
            f.close()
        print('File downloaded..')
        return

    elif(datatype=='UDP'):
        data,addr = client.recvfrom(1024)
        while(data):
            try:
                f.write(data)
                client.settimeout(2)
                data,addr = client.recvfrom(BUFFER_SIZE)
            except socket.timeout:
                print('Data recieved..UDP')
                f.close()
                recieveInfo(client,data)
                client.close()
        return

    else:
        print('ERROR in TYPE OF CONNECTION..')
        print('Exiting..')
        client.close()
        sys.exit(0)
        return


# MY CLIENT 

port=int(input("Enter PORT number :"))
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)

try:
    client.connect((host,port))    
except:
    print('No Valid Server was found...')
    print('Exiting...')
    sys.exit(0)

#Else 
while(True):

    try:
        command=str(input('$'))
        client.send(str.encode(json.dumps(command)))

    except KeyboardInterrupt:
        print("KeyBoard Interrupt -> Exiting...")
        client.close()
        break

    inputs=command.split()

    data=client.recv(1024)
    print('Vachesindi...')
    if(inputs[0]=='indexGet'):
        data=json.loads(data)
        print('RECIEVED ON CLIENT')
        #recieveInfo(client,data)
        print(data)

    else:
        print('No data or EOT')
        client.close()
        sys.exit(0)
        break

client.close()

