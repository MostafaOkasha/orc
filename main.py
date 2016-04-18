#!/bin/bash

# Notes:
#    layout  - <pretext>:<data>?<2arg>
#    pretext - contains only 3 char lowercase
#    data    - Used for Data like game moves etc
#    SecArg  - Used for additonal info, like password hash


# !/usr/bin/env python

from socket import *
import threading
import time

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

    # First connection, requestUID & PWHash
    clientsocket.send("UID")

    while True:
        data = clientsocket.recv(BUFF)

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
    # todo auth against Server - right now I'll assume everything is kosher chicken
    # 3rd try lock out.
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
        clientsock, addr = Serversock.accept()
        print(' ... Connected from: ' + str(addr))
        threading.start_new_thread(handler, (clientsock, addr))

