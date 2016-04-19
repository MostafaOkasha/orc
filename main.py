#!/usr/bin/python

# Notes:
#    layout  - <pretext>:<data>?<2arg>
#    pretext - contains only 3 char lowercase
#    data    - Used for Data like game moves etc
#    SecArg  - Used for additonal info, like password hash


# !/usr/bin/env python

from socket import *

import database     # bring in the database module
import threading
import time
import MySQLdb      #MySQL connector

database.Firstsetup()

PROGNAME = "ORC - Open Raspberry (Pi) Chess"
HOST = "127.0.0.1"
PORT = 4004
BUFF = 1024
ConnectionLimit = 10            # Max number of connections
Debbuging = 1                   # Debug Messages

# php connection details
# username='orcserver'
# dbpass='Qrw8XW9JNDHc4P7n'



def response(key):
    return'ServerResponse: ' + key

class clientId(object):


    def __init__(self, userid, address):
        self.UserID = userid
        self.Addr = address
        self.InGame = 0
        self.LastConnection = time.time()


def handler(clientsocket, address):
    global BUFF
    print('address: '), address

    # First connection, request UID & PWHash
    clientsocket.send(str.encode("UID"))

    while True:
        data = clientsocket.recv(BUFF)
        data = data.decode('utf-8')
        debug(data)

        # data validation
        data = data.rstrip()

        if data == "":
            break

        if data == "close":
            clientsocket.close()

            # todo update server DB they have disconnected

            print(clientDetails.UserID)
            print(clientDetails.Addr)

            print("client closed the connection")
            break

        # Search for pretext and split apart UserID and Hash
        pretext = data.split(":")[0]
        pretext = pretext.lower()

        data = data.split(":")[1]

        if pretext == "uid":
            hash = ""
            userid = data.split("?")[0]
            hash = data.split("?")[1]

        if authuser(userid, hash) == False:
            debug("auth failed for " + userid)
            userid = ""
            hash = ""
            clientsocket.send("UID")

        # clear the hash var as we don't need to keep it saved
        hash = ""

        debug("authed User " + userid)

        # Client Obect Class
        clientDetails = clientId(userid, address)


def authuser(userid, hash):
    database.authUser(userid,hash)
    return True

def debug(message):
    global Debbuging
    if Debbuging == 1:
        print(message)

if __name__ == '__main__':
    ADDR = (HOST, PORT)
    Serversock = socket(AF_INET, SOCK_STREAM)
    Serversock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    Serversock.bind(ADDR)
    Serversock.listen(ConnectionLimit)

    while True:
        debug("Waiting for connection ... Listening on port " + str(PORT))
        (clientsock, addr) = Serversock.accept()
        print(' ... Connected from: ' + str(addr))
        t = threading.Thread(target = handler(clientsock,addr))
        t.daemon = True
        t.start()

        # threading._start_new_thread(addr, clientsock)

