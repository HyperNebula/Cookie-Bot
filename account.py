import csv
import time
import random
import pandas as pd
from varibles import *
try:
    import wikipedia
except ImportError:
    WikiWork = False
else:
    WikiWork = True


def count():
    df = pd.read_csv('accounts.csv')
    return len(df.index)


def register(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        return "You already registered :P"
    else:
        with open('accounts.csv', 'a', newline='') as fd:
            fdw = csv.writer(fd)
            fdw.writerow([name, 0, 0, 0, 0])
        return "Bank Registered"


def bal(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        return int(df.loc[df["UserId"] == int(name), "Balance"])
    else:
        return None


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
    if balnum is None:
        return "Please register first using `/bank register`"
    if amount > int(balnum):
        return 'You do not have enough Cocoa Beans. Use /bank to see your current balance'

    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(enduser)).any():
        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(enduser), "Balance"] += amount
        df.to_csv('accounts.csv', index=False)

        df = pd.read_csv('accounts.csv')
        df.loc[df["UserId"] == int(startuser), "Balance"] -= amount
        df.to_csv('accounts.csv', index=False)

        return 'Payment successful!'
    else:
        return "That user does not exist or has not registered a bank account."


def payday(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        timer = int(df.loc[df["UserId"] == int(name), "Payday"])

        timeleft = int(time.time() - timer)
        timeleft = 3600 - timeleft
        if timeleft > 0:
            typeT = 'seconds'
            if timeleft > 60:
                timeleft = timeleft // 60
                typeT = 'minutes'

            fmt = 'You still have to wait {} {}!'
            return fmt.format(timeleft, typeT)

        df.loc[df["UserId"] == int(name), "Balance"] += 1000
        df.loc[df["UserId"] == int(name), "Payday"] = time.time()
        df.to_csv('accounts.csv', index=False)
    else:
        return "Please register first using `/bank register`"

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

    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        timer = int(df.loc[df["UserId"] == int(name), "Rob"])
        balrob = int(df.loc[df["UserId"] == int(name), "Balance"])
    else:
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
        return 'You do not have enough Cocoa Beans. Use /bank to see your current balance'
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


def definition(word):
    if WikiWork:
        if word is None:
            return "Please supply the word you are defining using this format: `/definition WORD`"
        try:
            wp = wikipedia.summary(word, sentences=2)
            return wp
        except wikipedia.DisambiguationError:
            return "Please be more specific. That word is too ambiguous"
    else:
        return 'The bot owner has not installed the Wikipedia package.'


def roulette(name):
    df = pd.read_csv('accounts.csv')

    if (df["UserId"] == int(name)).any():
        timer = int(df.loc[df["UserId"] == int(name), "Roulette"])
    else:
        return "Please register first using `/bank register`"

    timeleft = int(time.time() - timer)
    timeleft = 86400 - timeleft

    if timeleft > 0:
        typeT = 'seconds'
        if timeleft > 60:
            timeleft = timeleft // 60 + 1
            typeT = 'minutes'
            if timeleft > 60:
                timeleft = timeleft // 60
                typeT = 'hours'

        fmt = 'You still have to wait {} {}!'
        return fmt.format(timeleft, typeT)

    num = random.randint(1, 6)
    if num == 1:
        df.loc[df["UserId"] == int(name), "Balance"] = (bal(name) * 2)
        df.loc[df["UserId"] == int(name), "Roulette"] = time.time()
        df.to_csv('accounts.csv', index=False)
        return 'You are safe! Your balance has doubled!'
    else:
        df.loc[df["UserId"] == int(name), "Balance"] = 0
        df.loc[df["UserId"] == int(name), "Roulette"] = time.time()
        df.to_csv('accounts.csv', index=False)
        return 'BOOM! You are dead. :('
