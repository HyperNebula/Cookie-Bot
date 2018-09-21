import csv
import time
import random
import pandas as pd


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
                with open("accounts.csv", "a", newline='') as acnts:
                    acntWriter = csv.writer(acnts)
                    acntWriter.writerow([name, 0, 0, 0])
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


def numgame(name, guess, guessnum, answer):
    if guess == answer:
        if guessnum == 1:
            money_in = 1000
        if guessnum == 2:
            money_in = 900
        if guessnum == 3:
            money_in = 750
        if guessnum == 4:
            money_in = 600
        if guessnum == 5:
            money_in = 450
        if guessnum == 6:
            money_in = 300

        fmt = "You are right! You guessed it in {} guesses. As a reward, you get {} Cocoa Beans"

        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(name), "Balance"] += money_in
        df.to_csv('accounts.csv', index=False)

        return fmt.format(guessnum, money_in)

    elif guessnum != 6:
        if guess < answer:
            return 'The number is higher'
        if guess > answer:
            return 'The number is lower'

    if guessnum == 6 and guess != answer:
            fmt = 'You did not guess the number in time. It was {}'
            return fmt.format(answer)


def rob(name, ramount):
    name = str(name)
    with open("accounts.csv", "r") as acntl:
        coolReader = csv.reader(acntl)
        namenum = -1

        for row in coolReader:
            namenum += 1
            if row[0] == name:
                timer = float(row[3])
                timer = int(timer)
                balrob = int(row[1])
            elif namenum == count():
                return "Please register first using `/bank register`"

    timeleft = int(time.time()-timer)
    timeleft = 60 - timeleft
    if timeleft > 0:
        fmt = 'You still have to wait {} seconds!'
        return fmt.format(timeleft)

    if ramount > 300:
        return 'The maximum amount of Cocoa Beans is 300'
    elif ramount < 1:
        return 'The minimum amount of Cocoa Beans is 1'
    elif balrob < ramount:
        return 'You do not have enought Cocoa Beans. Use /bank to see your current balance'
    else:
        if ramount > 249:
            chance = 65
        elif ramount > 200:
            chance = 60
        elif ramount > 149:
            chance = 55
        elif ramount > 100:
            chance = 50
        elif ramount > 0:
            chance = 45

    chancenum = random.randint(0, 100)
    if chancenum <= chance:
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(name), "Balance"] += ramount
        df.loc[df["UserId"] == int(name), "Rob"] = time.time()
        df.to_csv('accounts.csv', index=False)
        return 'Congrats!, you doubled your {} Cocoa Beans'.format(ramount)
    else:
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(name), "Balance"] -= ramount
        df.loc[df["UserId"] == int(name), "Rob"] = time.time()
        df.to_csv('accounts.csv', index=False)
        return 'Sorry, you got caught. You lost {} Cocoa Beans'.format(ramount)

