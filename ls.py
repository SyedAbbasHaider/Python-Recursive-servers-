import socket as mysoc


# DNS entry class
import sys
import time

TIMEOUT_SECONDS = 3.0
# creates a basic socket
def create_sock():
    try:
        sock = mysoc.socket(mysoc.AF_INET, mysoc.SOCK_STREAM)
        return sock
    except mysoc.error as err:
        print('{} \n'.format("socket open error ", err))

# get command parameters
listen_port = int(sys.argv[1])
ts1_hostname = sys.argv[2]
ts1_port = int(sys.argv[3])
ts2_hostname = sys.argv[4]
ts2_port = int(sys.argv[5])

# create necessary ports
ss = create_sock()
ts1 = create_sock()
ts2 = create_sock()

# connect server with its port and listen for client
host = mysoc.gethostname()
server_binding = ('', listen_port)
ss.bind(server_binding)
ss.listen(1)
# connect to ts1
ip_address = mysoc.gethostbyname(ts1_hostname)
server_binding = (ip_address, ts1_port)
ts1.settimeout(TIMEOUT_SECONDS)
ts1.connect(server_binding)
# connect to ts2
ip_address = mysoc.gethostbyname(ts2_hostname)
server_binding = (ip_address, ts2_port)
ts2.settimeout(TIMEOUT_SECONDS)
ts2.connect(server_binding)

print("[S]: Server host name is: " , host)
localhost_ip = (mysoc.gethostbyname(host))
print("[S]: Server IP address is  " , localhost_ip)
csockid, addr = ss.accept()
print("[S]: Got a connection request from a client at " , addr)

done = False

while not done:
    received_msg = csockid.recv(300)
    # handles the case in which the client sent no messages to the server
    if len(received_msg) > 0:
        if received_msg == "quit":
            ts1.send("disconnecting")
            ts2.send("disconnecting")
            break
        else:
            ts1.send(received_msg)
            ts2.send(received_msg)

            ts1_response = None
            ts2_response = None

            try:
                ts1_response = ts1.recv(1024)
            except mysoc.timeout:  # ts1 timed out; try ts2 now
                try:  # try ts2 with the hostname
                    ts2_response = ts2.recv(1024)
                except mysoc.timeout:  # ts2 also timed out, no results found
                    csockid.send(received_msg + " - Error:HOST NOT FOUND ")

            if ts1_response != None:
                csockid.send(ts1_response)
            if ts2_response != None:
                csockid.send(ts2_response)

# Close the server socket
ss.close()
exit()
