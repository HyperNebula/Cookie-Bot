import csv
import time
import pandas as pd
import datetime


bot_id = "bot_id"


def count():
    with open('accounts.csv', 'r') as acnts:
        acntReader = csv.reader(acnts)
        rownum = -1

        for line in acntReader:
            rownum += 1

        return rownum


def register(name):
    name = str(name)
    with open("accounts.csv", "r") as acnts:
        acntReader = csv.reader(acnts)
        namenum = -1

        for line in acntReader:
            namenum += 1
            if line[0] == name:
                return "You already registered :P"
            elif namenum == count():
                with open("accounts.csv", "a") as acnts:
                    acntWriter = csv.writer(acnts)
                    acntWriter.writerow([name, 0])
                    return "Bank Registered"


def bal(name):
    name = str(name)
    with open("accounts.csv", "r") as acnts:
        acntReader = csv.reader(acnts)
        namenum = -1

        for line in acntReader:
            namenum += 1
            if line[0] == name:
                balance = line[1]
                return "Your balance is {}".format(balance)
            elif namenum == count():
                return "Please register first using `/bank register`"


def obal(name):
    name = str(name)
    with open("accounts.csv", "r") as acnts:
        acntReader = csv.reader(acnts)
        namenum = -1

        for line in acntReader:
            namenum += 1
            if line[0] == name:
                balance = line[1]
                return "The user's balance is {}".format(balance)
            elif namenum == count():
                return "That user does not exist or has not registered a bank account."


def top():
    global top, top2, top3, top4, top5
    df = pd.read_csv('accounts.csv')
    df = df.sort_values(by=["Balance"], ascending=[0])
    df.to_csv('accounts.csv', index=False)

    with open('accounts.csv', 'r') as readin:
        topReader = csv.reader(readin)
        counter = 0
        leaderboard = []

        next(readin)
        for row in readin:
            counter += 1
            if counter <= 5:
                leaderboard.append(row.split(','))

        if len(leaderboard) < 5:
            while len(leaderboard) < 5:
                leaderboard.append([bot_id, '0\n'])

        return leaderboard

