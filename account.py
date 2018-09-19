import csv
import time
import pandas as pd


bot_id = "408378922384883722"


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
                    acntWriter.writerow([name,0,0])
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
                return balance
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
        counter = 0
        leaderboard = []

        next(readin)
        for row in readin:
            counter += 1
            if counter <= 5:
                leaderboard.append(row.split(','))

        if len(leaderboard) < 5:
            while len(leaderboard) < 5:
                leaderboard.append([bot_id, '0'])

        return leaderboard


def pay(startuser, enduser, amount):
    if amount < 1:
        return 'The minimum amount of Cocoa Beans is 1'
    balnum = bal(startuser)
    if balnum == "Please register first using `/bank register`":
        return "Please register first using `/bank register`"
    if amount > int(balnum):
        return 'You do not have enough Cocoa Beans. Use /bank to see your current balance'

    with open('accounts.csv', 'r') as userl:
        userReader = csv.reader(userl)
        namenum = -1

        for line in userReader:
            namenum += 1
            if line[0] == enduser:
                df = pd.read_csv('accounts.csv')
                df.loc[df["UserId"] == int(enduser), "Balance"] += amount
                df.to_csv('accounts.csv', index=False)

                df = pd.read_csv('accounts.csv')
                df.loc[df["UserId"] == int(startuser), "Balance"] -= amount
                df.to_csv('accounts.csv', index=False)

                return 'Payment successful!'
            elif namenum == count():
                return "That user does not exist or has not registered a bank account."


def payday(name):
    name = str(name)
    with open("accounts.csv", "r") as acnts:
        coolReader = csv.reader(acnts)
        namenum = -1

        for row in coolReader:
            namenum += 1
            if row[0] == name:
                timer = float(row[2])
                timer = int(timer)
            elif namenum == count():
                return "Please register first using `/bank register`"

    timeleft = int(time.time()-timer)
    timeleft = 1800 - timeleft
    if timeleft > 0:
        typeT = 'seconds'
        if timeleft > 60:
            timeleft = timeleft // 60
            typeT = 'minutes'

        fmt = 'You still have to wait {} {}!'
        return fmt.format(timeleft, typeT)

    with open('accounts.csv', 'r') as cooll:
        coollReader = csv.reader(cooll)

        for line in coollReader:
            if line[0] == name:
                df = pd.read_csv('accounts.csv')
                df.loc[df["UserId"] == int(name), "Balance"] += 1000
                df.loc[df["UserId"] == int(name), "Payday"] = time.time()
                df.to_csv('accounts.csv', index=False)
    return 'Payday! You just got 1000 Cocoa Beans!'
