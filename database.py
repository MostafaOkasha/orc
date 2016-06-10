#!/usr/bin/python
import sqlite3
import datetime

# TODO catch DB errors

# Setup sql Instructions
'''
    To setup sqlite3 to make it more readable when running queries run the following
    .header on
    .mode column
    .timer on

    To setup the databases

    USER TABLE
    CREATE TABLE IF NOT EXISTS `users` (
      `id` float NOT NULL,
      `name` varchar(30) NOT NULL,
      `pw_hash` varchar(60) NOT NULL,
      `bad_pw_count` varchar(60) NOT NULL,
      `game_wins` int(11) NOT NULL,
      `game_total` int(11) NOT NULL,
      `game_inprogress` tinyint(1) NOT NULL,
      `date_joined` date NOT NULL,
      `last_connected` date NOT NULL,
      `account_locked` tinyint(1) NOT NULL,
      `locked_date` date NOT NULL,
      `require_pw_change` tinyint(1) NOT NULL,
      PRIMARY KEY (`id`)
    );

    GAME TABLE
    CREATE TABLE IF NOT EXISTS `game` (
      `id` float NOT NULL,
      `player_1` float NOT NULL,
      `player_2` float NOT NULL,
      `date_started` date NOT NULL,
      `date_ended` date NOT NULL,
      `player_move` float NOT NULL,
      `game_winner` float NOT NULL,
      PRIMARY KEY (`id`,`date_started`)
    );

    MOVES TABLE
    CREATE TABLE IF NOT EXISTS `moves` (
      `move_id` int(11) NOT NULL,
      `id` int(11) NOT NULL,
      `from` int(11) NOT NULL,
      `to` int(11) NOT NULL,
      `date` int(11) NOT NULL,
      `time` int(11) NOT NULL,
      PRIMARY KEY (`move_id`)
    );

    INSERT DATA into Users table
    INSERT INTO `users` (`id`, `name`, `pw_hash`,`bad_pw_count`, `game_wins`, `game_total`, `game_inprogress`, `date_joined`, `last_connected`, `account_locked`, `locked_date`,`require_pw_change`) VALUES
    (1, 'shane', '1',0, 0, 0, 0, '2016-04-11', '2016-04-11', 0, 0, 0),
    (2, '2', 'c4ca4238a0b9',0, 0, 0, 0, '2016-04-18', '2016-04-18', 0, 0, 0);
'''

# To use SQLLite Instructions
'''
    .tables             -   Will list out the tables
    .schema [tablename] -   Will show the CREATE statement(s) for a table or tables
'''


def authuser(uname, pw):
    print("authing user")

    toreturn = False
    sql = 'SELECT * from users where name = "'+uname+'" AND pw_hash = "'+pw+'";'

    data = (runquery(sql))

    if len(data) != 0:
        if data[9] != 1:  # account not locked?

            sql = "UPDATE users SET last_connected = " + '"' + datetime.datetime.now().strftime("%Y-%m-%d") + '"' + ' WHERE name = "' + uname + '";'
            updatedatabase(sql)
            toreturn = True
        else:
            toreturn = "Account locked"

    if toreturn != True:
        print("Username/Pasword didn't match - looking for username")
        sql = 'SELECT * from users where name = "' + uname + '";'
        data = (runquery(sql))

        if len(data) != 0:  # Found username
            print("found username")

            badpwcount = int(data[3]) + 1
            if badpwcount <= 5:
                sql = "UPDATE users SET bad_pw_count = " + str(badpwcount) + ' WHERE name = "' + str(uname) + ";"
                toreturn = "Incorrect username password combination"
            else:
                sql = "UPDATE users SET account_locked = 1, locked_date = " + '"' + datetime.datetime.now().strftime("%Y-%m-%d") + '"' + ' WHERE name = "' + str(uname) +'";'
                toreturn = "Account locked"

            updatedatabase(sql)

    return toreturn


def updatedatabase(sqlstatement):

    try:
        con = sqlite3.connect('orc.db')
        cur = con.cursor()
        cur.execute(sqlstatement)
        con.commit()

    except sqlite3.Error:
        if con:
            con.rollback()

    finally:
        if con:
            con.close


def runquery(sqlstatement):
    con = sqlite3.connect('orc.db')
    cur = con.cursor()
    cur.execute(sqlstatement)
    data = cur.fetchall()
    if len(data) != 0:
        data = data[0]  # convert to a Tuple
    else:
        data = ""
    con.close()

    return data
