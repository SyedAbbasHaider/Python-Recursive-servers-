import socket as mysoc
import sys
import time

# Global Variables
ts_connect = False


# writes given string to the output file
def write_to_file(msg):
    with open("RESOLVED.txt", "a+") as text_file:
        text_file.write(msg + "\n")
    # close file pointers
    text_file.close()


# creates a basic socket
def create_sock():
    try:
        sock = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        return sock
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))


# reset RESOLVED.txt to be a fresh new file
open("RESOLVED.txt", "w").close()

# Initialize variables with command line values
rsHostname = sys.argv[1]
rsListenPort = int(sys.argv[2])

#  populate host names from txt file
hostnames = []
with open("PROJ2-HNS.txt") as f:
    lines = [line.rstrip() for line in f]
    for line in lines:
        hostnames.append(line)
f.close()


# ls will represent the RS connection
ls = create_sock()
# connect RS hostname to cs
ip_address = mysoc.gethostbyname(rsHostname)
server_binding = (ip_address, rsListenPort)
ls.connect(server_binding)

for hostname in hostnames:
    # send it to root DNS
    ls.send(hostname)
    print("send:" + hostname)
    received = ls.recv(204)
    write_to_file(received)

# command connected DNS sockets to close
ls.send("quit")

ls.close()
