import csv
import time
import pandas as pd
import datetime


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
                with open("accounts.csv", "a", newline='') as acnts:
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
