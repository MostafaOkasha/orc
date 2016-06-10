#!/usr/bin/python

# Notes:
#    layout  - <pretext>:<data>?<2arg>
#    pretext - contains only 3 char lowercase
#    data    - Used for Data like game moves etc
#    SecArg  - Used for additonal info, like password hash


# !/usr/bin/env python

from socket import *

import database     # bring in the database module
import time
import threading


PROGNAME = "ORC - Open Raspberry-Pi Chess"
HOST = "192.168.20.105"
PORT = 4004
BUFF = 1024
ConnectionLimit = 10            # Max number of connections
Debbuging = 1                   # Debug Messages
DebugFile = "debug.log"


def response(key):
    return'ServerResponse: ' + key


class ClientId(object):

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

            # todo update server DB  when they have disconnected

            print("client closed the connection")
            break

        # Search for pretext and split apart UserID and Hash
        #  TODO need to make this much more robust
        pretext = data.split(":")[0]
        pretext = pretext.lower()

        data = data.split(":")[1]

        if pretext == "uid":
            userhash = ""
            userid = data.split("?")[0]
            userhash = data.split("?")[1]

            result = database.authuser(userid, userhash)

            if result != True:
                print("auth failed for " + userid + " - " + result)
                userid = ""
                userhash = ""
                data = "UID" + ":" + result

                clientsocket.send(data.encode())
            else:
                debug("authed User " + userid)
                clientDetails = ClientId(userid, address)

        # clear the hash var as we don't need to keep it saved
        userhash = ""
        userid = ""


def debug(message):
    global Debbuging
    if Debbuging == 1:
        print(message)


def main():
    ReadSettings()


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

def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def ReadSettings():
    CurrentSetting = ""
    print("Reading settings")
    try:
        settings = open("settings/settings.inf", "r")

        for LineData in nonblank_lines(settings):
            CurrentSetting = LineData
            if LineData[:1] != "[":
                setting = LineData.split("=")[0]
                settingArgument = LineData.split("=")[1]
                setting = setting.lower()

                if setting == "name":
                    global PROGNAME
                    PROGNAME = settingArgument
                    continue

                if setting == "port":
                    if settingArgument.isnumeric() == True:
                        global PORT
                        PORT = int(settingArgument)
                        continue

                if setting == "maxconnections":
                    if settingArgument.isnumeric() == True:
                        global ConnectionLimit
                        ConnectionLimit = int(settingArgument)
                        continue

                if setting == "debuglevel":
                    if settingArgument.isnumeric() == True:
                        global Debbuging
                        Debbuging = int(settingArgument)
                        continue

                if settings == "DebugFile":
                    global DebugFile
                    DebugFile = settingArgument
                    continue

    except:
        print("Error in Reading the Setting files")
        print(CurrentSetting)


    finally:
        settings.close()


if __name__ == '__main__':
    main()