import socket as mysoc
import argparse
import pdb


parser = argparse.ArgumentParser()
parser.add_argument('tsListenPort', type=int, help='tsListenPort')
args = parser.parse_args()
port_number = args.tsListenPort
sender_name = "TS1"

dnst1 = {}


def createDict():
    fin = open("PROJ2-DNSTS1.txt", "r")  # Open the file and insert all data into the dictionary
    flines = fin.readlines()
    for x in flines:
        splitStr = x.split()
        orginalHostname = splitStr[0]
        dnst1[splitStr[0].lower()] = [splitStr[1], splitStr[2], orginalHostname] # splitStr is the original hostname
        # Use hostname as key and assign flag and IP.


def lookUp(hostname):
    hostname = hostname.lower()
    if hostname in dnst1:
    #only matching the hostname not A/NS
    #if hostname is matched in dns, send whole thing back to ls
        return dnst1[hostname][2] + " " + dnst1[hostname][0] + " " + dnst1[hostname][1]
    else:
        #if there is no match, do nothing
        return None


def server():
    try:
        ss = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        print("[TS]: Server socket created")
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))
    server_binding = ('', port_number)
    ss.bind(server_binding)
    ss.listen(10)
    host = mysoc.gethostname()
    print("[TS]: Server host name is: ", host)
    localhost_ip = mysoc.gethostbyname(host)
    print("[TS]: Server IP address is  ", localhost_ip)
    csockid, addr = ss.accept()
    print("[TS]: Got a connection request from a ls at", addr)

    # Continuous loop which receives data from the ls
    while 1:
        data_from_ls = csockid.recv(1024)  # Receive data from ls
        msg = data_from_ls
        print("[TS]: Data Received: ", msg)

        if(msg.strip() == "disconnecting"):  # If disconnecting, break out of the loop
            ss.close()
            exit()
        else:
            data = lookUp(msg)  # Look up data sent in dictionary table
            if data is not None:
                csockid.send(sender_name + ": " + data)  # data is sent back as a whole string



    # Close the server socket
    ss.close()
    exit()


createDict()
server()
