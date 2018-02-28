import csv
import time
import random
import logging
import asyncio
import discord
import platform
import pandas as pd
# from discord.ext import commands
# from discord.ext.commands import Bot


client = discord.Client()
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='bot/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


# Functions:


def count():
    global rowcomp
    with open('bot/_Bal.csv', 'r') as balc:
        balReader = csv.reader(balc)
        rownum = -1

        for line in balReader:
            rownum += 1

        rowcomp = rownum


def cooldowncheck(x):
    global name
    global timer
    if x == 0:
        with open('bot/_robCooldown.csv', 'r') as coolr:
            coolReader = csv.reader(coolr)
            for row in coolReader:
                if row[0] == name:
                    timer = float(row[1])
                    timer = int(timer)
                    break
                else:
                    timer = float(time.time())
                    timer = int(timer)
    elif x == 1:
        with open('bot/_paydayCooldown.csv', 'r') as coolr:
            coolReader = csv.reader(coolr)
            for row in coolReader:
                if row[0] == name:
                    timer = float(row[1])
                    timer = int(timer)
                    break
                else:
                    timer = float(time.time())
                    timer = int(timer)
    elif x == 2:
        with open('bot/_rouletteCooldown.csv', 'r') as coolr:
            coolReader = csv.reader(coolr)
            for row in coolReader:
                if row[0] == name:
                    timer = float(row[1])
                    timer = int(timer)
                    break
                else:
                    timer = float(time.time())
                    timer = int(timer)


async def bal(x, message):
    global balance
    global name
    global money_in
    global rowcomp
    global timer
    with open('bot/_Bal.csv', 'r') as balc:
        balReader = csv.reader(balc)
        namenum = -1
        count()

        for line in balReader:
            namenum += 1

            if x == 0:
                if line[0] == name:
                    balance = line[1]
                    await client.send_message(message.channel, 'You have %s Cocoa Beans.' % balance)
                    break
                elif namenum == rowcomp:
                    await client.send_message(message.channel, 'Please register first using /bank register')
                    break
            elif x == 1:
                if line[0] == name:
                    await client.send_message(message.channel, 'You already registered :P')
                    break
                elif namenum == rowcomp:
                    with open('bot/_Bal.csv', 'a', newline='') as balc:
                        balWriter = csv.writer(balc)
                        balWriter.writerow([name, 0])
                    with open('bot/_robCooldown.csv', 'a', newline='') as balc:
                        balWriter = csv.writer(balc)
                        balWriter.writerow([name, 0])
                    with open('bot/_paydayCooldown.csv', 'a', newline='') as balc:
                        balWriter = csv.writer(balc)
                        balWriter.writerow([name, 0])
                    with open('bot/_rouletteCooldown.csv', 'a', newline='') as balc:
                        balWriter = csv.writer(balc)
                        balWriter.writerow([name, 0])
                    await client.send_message(message.channel, 'Bank Registered')
                    break
            elif x == 2:
                if line[0] == name:
                    df = pd.read_csv(
                        'bot/_Bal.csv')
                    df.loc[df["Username"] == name, "Amount"] += money_in
                    df.to_csv(
                        'bot/_Bal.csv', index=False)
                    break
                elif namenum == rowcomp:
                    await asyncio.sleep(0.1)
                    await client.send_message(message.channel, 'Please register first using /bank register')
                    break
            elif x == 3:
                if line[0] == name:
                    df = pd.read_csv(
                        'bot/_Bal.csv')
                    df.loc[df["Username"] == name, "Amount"] -= money_in
                    df.to_csv(
                        'bot/_Bal.csv', index=False)
                    break
                elif namenum == rowcomp:
                    await asyncio.sleep(0.1)
                    await client.send_message(message.channel, 'Please register first using /bank register')
                    break
            elif x == 4:
                if line[0] == name:
                    df = pd.read_csv(
                        'bot/_robCooldown.csv')
                    df.loc[df["Username"] == name, "Time"] = time.time()
                    df.to_csv(
                        'bot/_robCooldown.csv', index=False)
                    break
                elif namenum == rowcomp:
                    await asyncio.sleep(0.1)
                    await client.send_message(message.channel, 'Please register a bank account first using /bank register')
                    break
            elif x == 5:
                if line[0] == name:
                    df = pd.read_csv(
                        'bot/_paydayCooldown.csv')
                    df.loc[df["Username"] == name, "Time"] = time.time()
                    df.to_csv(
                        'bot/_paydayCooldown.csv', index=False)
                    break
                elif namenum == rowcomp:
                    await asyncio.sleep(0.1)
                    await client.send_message(message.channel, 'Please register a bank account first using /bank register')
                    break
            elif x == 6:
                if line[0] == name:
                    df = pd.read_csv(
                        'bot/_rouletteCooldown.csv')
                    df.loc[df["Username"] == name, "Time"] = time.time()
                    df.to_csv(
                        'bot/_rouletteCooldown.csv', index=False)
                    break
                elif namenum == rowcomp:
                    await asyncio.sleep(0.1)
                    await client.send_message(message.channel, 'Please register a bank account first using /bank register')
                    break
            elif x == 7:
                if line[0] == name:
                    balance = int(line[1])
                    break
                elif namenum == rowcomp:
                    balance = 0
                    break
            else:
                break


# Edit/Delete messages
channel = '408750927714058240'  # channel id for logs


@client.event
async def on_message_edit(before, after):
    if after.author == client.user:
        return

    fmt = '**{0.author}** edited their message:\n{1.content}'
    await client.send_message(discord.Object(id=channel), fmt.format(after, before))


@client.event
async def on_message_delete(message):
    if message.author == client.user:
        return

    fmt = '{0.author.name} has deleted the message:\n{0.content}'
    await client.send_message(discord.Object(id=channel), fmt.format(message))


@client.event  # commands
async def on_message(message):
    global name
    global money_in
    global balance
    global timer

    # await asyncio.sleep(0.2)
    if message.author == client.user:
        return

    name = message.author.name

    if message.content.startswith('/numgame'):
        await client.send_message(message.channel, 'Guess a number between 1 to 100')

        def guess_check(m):
            return m.content.isdigit()

        guess = 0
        answer = random.randint(1, 100)
        guessNum = 0

        while guessNum < 6:
            guess = await client.wait_for_message(timeout=10.0, author=message.author, check=guess_check)
            guessNum = guessNum + 1
            if guess is None:
                fmt = 'Sorry, you took too long. It was {}.'
                await client.send_message(message.channel, fmt.format(answer))
                return
            if int(guess.content) == answer:
                if guessNum == 1:
                    money_in = 1000
                if guessNum == 2:
                    money_in = 500
                if guessNum == 3:
                    money_in = 300
                if guessNum == 4:
                    money_in = 200
                if guessNum == 5:
                    money_in = 150
                if guessNum == 6:
                    money_in = 100

                fmt = "You are right! You guessed it in {} guesses. As a reward, you get {} Cocoa Beans"
                await client.send_message(message.channel, fmt.format(guessNum, money_in))

                await bal(2, message)

                return
            elif guessNum != 6:
                if int(guess.content) < answer:
                    await client.send_message(message.channel, 'The number is higher')
                if int(guess.content) > answer:
                    await client.send_message(message.channel, 'The number is lower')

            if guessNum == 6 and guess != answer:
                fmt = 'You did not guess the number in time. It was {}'
                await client.send_message(message.channel, fmt.format(answer))

    elif message.content.startswith('/rob'):

        cooldowncheck(0)

        if timer == int(float(time.time())):
            await client.send_message(message.channel, 'Please register first using /bank register')
            return

        timeleft = float(time.time() - timer)
        timeleft = int(timeleft)
        timeleft = 60 - timeleft

        if timeleft > 0:
            await client.send_message(message.channel, 'You still have to wait %s seconds!' % timeleft)
            return

        def guess_check(m):
            return m.content.isdigit()

        await client.send_message(message.channel, 'How much Cocoa Beans do you want to put into the robbery?')
        money_bet = await client.wait_for_message(timeout=10.0, author=message.author, check=guess_check)
        money_bet = int(money_bet.content)

        if money_bet > 300:
            await client.send_message(message.channel, 'The maximum amount of Cocoa Beans is 300')
        elif money_bet < 1:
            await client.send_message(message.channel, 'The minimum amount of Cocoa Beans is 1')
        else:
            if money_bet > 249:
                chance = 60
            elif money_bet > 200:
                chance = 55
            elif money_bet > 149:
                chance = 50
            elif money_bet > 100:
                chance = 45
            elif money_bet > 49:
                chance = 40
            elif money_bet > 0:
                chance = 30

        await bal(7, message)
        if balance < money_bet:
            await client.send_message(message.channel, 'You do not have enought Cocoa Beans. Use /bank to see your current balance')
            return

        chancenum = random.randint(0, 100)
        if chancenum <= chance:
            await client.send_message(message.channel, 'Congrats!, you doubled your %s Cocoa Beans' % money_bet)
            money_in = money_bet
            await bal(2, message)
            await bal(4, message)
        else:
            await client.send_message(message.channel, 'Sorry, you got caught. You lost %s Cocoa Beans' % money_bet)
            money_in = money_bet
            await bal(3, message)
            await bal(4, message)

    elif message.content.startswith('/srob'):
        cooldowncheck(0)

        if timer == int(float(time.time())):
            await client.send_message(message.channel, 'Please register first using /bank register')
            return

        timeleft = float(time.time() - timer)
        timeleft = int(timeleft)
        timeleft = 60 - timeleft

        if timeleft > 0:
            await client.send_message(message.channel, 'You still have to wait %s seconds!' % timeleft)
            return

        money_bet = 300
        await bal(7, message)
        if balance < money_bet:
            await client.send_message(message.channel, 'You do not have enought Cocoa Beans. Use /bank to see your current balance')
            return

        chance = 60
        chancenum = random.randint(0, 100)
        if chancenum <= chance:
            await client.send_message(message.channel, 'Congrats!, you doubled your %s Cocoa Beans' % money_bet)
            money_in = money_bet
            await bal(2, message)
            await bal(4, message)
        else:
            await client.send_message(message.channel, 'Sorry, you got caught. You lost %s Cocoa Beans' % money_bet)
            money_in = money_bet
            await bal(3, message)
            await bal(4, message)

    elif message.content.startswith('/payday'):
        cooldowncheck(1)

        if timer == int(float(time.time())):
            await client.send_message(message.channel, 'Please register first using /bank register')
            return

        timeleft = float(time.time() - timer)
        timeleft = int(timeleft)
        timeleft = 1800 - timeleft

        if timeleft > 0:
            typeT = 'seconds'
            if timeleft > 60:
                timeleft = timeleft // 60 + 1
                typeT = 'minutes'
                if timeleft > 60:
                    timeleft = timeleft // 60 + 1
                    typeT = 'hours'
            fmt = 'You still have to wait {} {}!'
            await client.send_message(message.channel, fmt.format(timeleft, typeT))
            return

        await client.send_message(message.channel, 'Payday! You just got 1000 Cocoa Beans!')
        money_in = 1000
        await bal(2, message)
        await bal(5, message)

    elif message.content.startswith('/bank register'):
        await bal(1, message)

    elif message.content.startswith('/bank'):
        await bal(0, message)

    elif message.content.startswith('/top'):
        df = pd.read_csv('bot/_Bal.csv')
        df = df.sort_values(by=["Amount"], ascending=[0])
        df.to_csv('bot/_Bal.csv', index=False)

        with open('bot/_Bal.csv', 'r') as reading:
            Reader = csv.reader(reading)
            counter = 0
            top = 0
            top2 = 0
            top3 = 0
            top4 = 0
            top5 = 0

            next(Reader)
            for row in Reader:
                if counter < 5:
                    counter += 1
                    if counter == 1:
                        top = row
                    elif counter == 2:
                        top2 = row
                    elif counter == 3:
                        top3 = row
                    elif counter == 4:
                        top4 = row
                    elif counter == 5:
                        top5 = row
            if top == 0:
                top = ['Wumpus', 0]
            if top2 == 0:
                top2 = ['Wumpus', 0]
            if top3 == 0:
                top3 = ['Wumpus', 0]
            if top4 == 0:
                top4 = ['Wumpus', 0]
            if top5 == 0:
                top5 = ['Wumpus', 0]

            topPrint = ''
            top2Print = ''
            top3Print = ''
            top4Print = ''
            top5Print = ''

            if top[0] != 'Wumpus':
                fmt = '\n1.{}: {}'
                topPrint = fmt.format(top[0], top[1])
            if top2[0] != 'Wumpus':
                fmt = '\n2.{}: {}'
                top2Print = fmt.format(top2[0], top2[1])
            if top3[0] != 'Wumpus':
                fmt = '\n3.{}: {}'
                top3Print = fmt.format(top3[0], top3[1])
            if top4[0] != 'Wumpus':
                fmt = '\n4.{}: {}'
                top4Print = fmt.format(top4[0], top4[1])
            if top5[0] != 'Wumpus':
                fmt = '\n5.{}: {}'
                top5Print = fmt.format(top5[0], top5[1])

            fmt = '```Leaderboard:{}{}{}{}{}```'
            await client.send_message(message.channel, fmt.format(topPrint, top2Print, top3Print, top4Print, top5Print))

    elif message.content.startswith('/roulette'):

        cooldowncheck(2)

        if timer == int(float(time.time())):
            await client.send_message(message.channel, 'Please register first using /bank register')
            return

        timeleft = float(time.time() - timer)
        timeleft = int(timeleft)
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
            await client.send_message(message.channel, fmt.format(timeleft, typeT))
            return

        await client.send_message(message.channel, 'Are you sure you want to do this? If you loose, then all your money will be gone.(y or n)')
        answer = await client.wait_for_message(timeout=10.0, author=message.author)
        answer = answer.content
        if answer == 'y':
            num = random.randint(1, 6)
            if num == 1:
                await client.send_message(message.channel, 'BOOM! You are dead. :(')
                await bal(7, message)
                money_in = balance
                await bal(3, message)
                await bal(6, message)
            elif num == 2:
                await client.send_message(message.channel, 'BOOM! You are dead. :(')
                await bal(7, message)
                money_in = balance
                await bal(3, message)
                await bal(6, message)
            elif num == 3:
                await client.send_message(message.channel, 'You are safe!')
                await bal(7, message)
                money_in = balance
                await bal(2, message)
                await bal(6, message)
            elif num == 4:
                await client.send_message(message.channel, 'You are safe!')
                await bal(7, message)
                money_in = balance
                await bal(2, message)
                await bal(6, message)
            elif num == 5:
                await client.send_message(message.channel, 'BOOM! You are dead. :(')
                await bal(7, message)
                money_in = balance
                await bal(3, message)
                await bal(6, message)
            else:
                await client.send_message(message.channel, 'BOOM! You are dead. :(')
                await bal(7, message)
                money_in = balance
                await bal(3, message)
                await bal(6, message)
        elif answer == 'n':
            await client.send_message(message.channel, 'That\'s ok, WIMP! :grin:')
        else:
            await client.send_message(message.channel, 'Please only type "y" or "n"')

    elif message.content.startswith('/count'):
        count()
        await client.send_message(message.channel, 'There are %s users registered.' % rowcomp)

    elif message.content.startswith('/who'):
        name = message.author.name
        await client.send_message(message.channel, 'You are %s!' % name)

    elif message.content.startswith('/messages'):
        counter = 0
        tmp = await client.send_message(message.channel, 'Calculating messages...')
        async for log in client.logs_from(message.channel, limit=1000):
            if log.author == message.author:
                counter += 1

        await client.edit_message(tmp, 'You have sent {} messages.'.format(counter))

    elif message.content.startswith('/reset'):
        if message.author.name == 'The Canadian\'s Friend':
            df = pd.read_csv(
                'bot/_paydayCooldown.csv')
            df.loc[df["Username"] == name, "Time"] = 0
            df.to_csv(
                'bot/_paydayCooldown.csv', index=False)
            df = pd.read_csv(
                'bot/_robCooldown.csv')
            df.loc[df["Username"] == name, "Time"] = 0
            df.to_csv(
                'bot/_robCooldown.csv', index=False)
            df = pd.read_csv(
                'bot/_rouletteCooldown.csv')
            df.loc[df["Username"] == name, "Time"] = 0
            df.to_csv(
                'bot/_rouletteCooldown.csv', index=False)
        else:
            await client.send_message(message.channel, 'For help and a list of commands, please use /help')

    elif message.content.startswith('/help'):
        await client.send_message(message.author, '```-----------Cookie-bot help-----------\n\nGame Commands:\n- numgame: Starts a number guessing game\n- rob: Try and steal some Cocoa Beans\n- srob: robs with 300 Cocoa Beans\n- payday: Recieve Cocoa Beans every 30 minutes\n- roulette: If you win, you double your Cocoa Beans\nCurrency Commands:\n- bank: Displays curent balance of bank account\n- bank register: Registers a bank account\n- top: Displays the users with the most amount of Cocoa Beans\nUtility Commands:\n- who: says who you are\n- count: Lists the number of users registered\n- messages: Lists the amount of messages you have sent\n\nCookie-bot made by The Canadian\'s Friend```')

    else:
        if message.content.startswith('/'):
            await client.send_message(message.channel, 'For help and a list of commands, please use /help')


@client.event
async def on_ready():
    print('Bot logged in as')
    print('Username: ' + client.user.name)
    print('Id: ' + client.user.id)
    print('--------')
    print('| Connected to '+str(len(client.servers))+' servers | Connected to ' +
          str(len(set(client.get_all_members())))+' users |')
    print('--------')
    # print('| Servers: ' + str(client.servers) + ' |')
    # print('| Users: ' + str(set(client.get_all_members())) + ' |')
    # print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(client.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(client.user.id))
    print('--------')
    print('You are running CookieBot v2.1')
    print('Created by The Canadian\'s friend')
    return await client.change_presence(game=discord.Game(name='/help | The Waiting Game'))


client.run('YourTokenHere')
