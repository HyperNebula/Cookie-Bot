import random
import asyncio
import account
import discord
import platform
from discord.ext import commands
from varibles import *


bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
bot.remove_command("help")


@bot.command()
async def bank(ctx, regi: str = None):
    if regi is None:
        if account.bal(ctx.message.author.id) is None:
            await ctx.send("Please register first using `/bank register`")
            return
        else:
            embed = discord.Embed(title="Bank Account info:", colour=discord.Colour(0xf5a623), description="Your balance is: `{}`".format(account.bal(ctx.message.author.id)))
            await ctx.send(embed=embed)
            return
    elif regi == "register":
        await ctx.send(account.register(ctx.message.author.id))
        return
    elif regi.startswith("<@!"):
        await ctx.send("That user is a bot and cannot have an account")
        return
    elif regi.startswith("<@"):
        print(regi.strip("<@>"))
        if account.bal(regi.strip("<@>")) is None:
            await ctx.send("That user does not exist or has not registered a bank account.")
            return
        else:
            user = await bot.fetch_user(int(regi.strip("<@>")))
            embed = discord.Embed(title="Bank Account info:", colour=discord.Colour(0xf5a623), description="{}'s balance is: `{}`".format(user.display_name, account.bal(regi.strip("<@>"))))
            await ctx.send(embed=embed)
            return


@bot.command()
async def top(ctx):
    leadboard = account.top()
    name1 = await bot.fetch_user(leadboard[0][0])
    name2 = await bot.fetch_user(leadboard[1][0])
    name3 = await bot.fetch_user(leadboard[2][0])
    name4 = await bot.fetch_user(leadboard[3][0])
    name5 = await bot.fetch_user(leadboard[4][0])

    fmt = '1.`{0.display_name}`: {1}2.`{2.display_name}`: {3}3.`{4.display_name}`: {5}4.`{6.display_name}`: {7}5.`{8.display_name}`: {9}'
    board = fmt.format(name1, leadboard[0][1] + '\n', name2, leadboard[1][1] + '\n', name3, leadboard[2][1] + '\n', name4, leadboard[3][1] + '\n', name5, leadboard[4][1])

    embed = discord.Embed(title="Leaderboard", colour=discord.Colour(0x724ded), description=board)
    await ctx.send(embed=embed)


@bot.command()
async def pay(ctx, user: str = None, amount=None):
    if user is None:
        await ctx.send("Please specify the target user using this format: `/pay @USERNAME AMOUNT`")
        return
    if amount is None:
        await ctx.send("Please specify the payment amount using this format: `/pay @USERNAME AMOUNT`")
        return
    try:
        amount = int(amount)
    except ValueError:
        await ctx.send("Please only use whole numbers")
        return
    if user.startswith("<@!"):
        await ctx.send("That user is a bot and cannot have an account")
        return
    await ctx.send(account.pay(ctx.message.author.id, user.strip("<@>"), amount))


@bot.command()
async def payday(ctx):
    await ctx.send(account.payday(ctx.message.author.id))


@bot.command()
async def numgame(ctx):
    if account.bal(ctx.message.author.id) is None:
        await ctx.send("Please register first using `/bank register`")
        return

    await ctx.send('Guess a number between 1 to 100')

    answer = random.randint(1, 100)
    guessnumber = 0

    def guess_check(m):
        return m.content.isdigit() and m.author == ctx.message.author
    while guessnumber < 6:
        guessnumber = guessnumber + 1

        try:
            guess = await bot.wait_for('message', check=guess_check, timeout=10.0)
        except asyncio.TimeoutError:
            fmt = 'Sorry, you took too long. It was {}.'
            await ctx.send(fmt.format(answer))
            break
        else:
            await ctx.send(account.numgame(ctx.message.author.id, int(guess.content), guessnumber, answer))

        if int(guess.content) == answer:
            break


@bot.command()
async def rob(ctx, ramount=None):
    if ramount is None:
        await ctx.send("Please supply the amount you are robbing with using this format: `/rob AMOUNT`")
        return
    try:
        ramount = int(ramount)
    except ValueError:
        await ctx.send("Please only use whole numbers")
        return
    await ctx.send(account.rob(ctx.message.author.id, ramount))


@bot.command()
async def srob(ctx):
    await ctx.send(account.rob(ctx.message.author.id, 300))


@bot.command()
async def roulette(ctx):

    answer = None
    while answer not in ('y', 'n'):
        await ctx.send('Are you sure you want to do this? If you loose, then all your money will be gone. (y or n)')

        def check(m):
            return m.author == ctx.message.author

        try:
            answer = (await bot.wait_for('message', timeout=10.0, check=check))
        except asyncio.TimeoutError:
            await ctx.send('Sorry, you took to long to answer')
            return

        answer = answer.content.lower()

        if answer == 'y':
            await ctx.send(account.roulette(ctx.message.author.id))
        elif answer == 'n':
            await ctx.send('That\'s ok, WIMP! :grin:')
        else:
            await ctx.send('Please only type "y" or "n"')
            await asyncio.sleep(0.5)


@bot.command()
async def definition(ctx, *, word: str = None):
    await ctx.send(account.definition(word))


@bot.command()
async def count(ctx):
    await ctx.send("There are {} users registered".format(account.count()))


@bot.command()
async def who(ctx):
    await ctx.send("You are **{}**!".format(ctx.message.author))


@bot.command()
async def messages(ctx):
    tmp = await ctx.send('Calculating messages...')
    counter = 0
    counter2 = 0
    async for log in ctx.history(limit=1000):
        counter2 += 1
        if log.author == ctx.message.author:
            counter += 1

    await tmp.edit(content='You have sent {} messages out of the last {}. This is roughly {}% of them'.format(counter, counter2, (counter * 100) // counter2))


@bot.command()
async def help(ctx):
    embed = discord.Embed(title="Cookie Bot Help", colour=discord.Colour(0xef41), description="This is a list of all the commands and their uses \n\n**Game Commands:**\n- `rob AMOUNT:` Bet an amount of Cocoa Beans and try and steal some more\n- `srob:` robs with 300 Cocoa Beans\n- `payday:` Recieve Cocoa Beans every 30 minutes\n- `numgame:` Starts a number guessing game\n- `roulette:` If you win, you double your Cocoa Beans\n\n**Currency Commands:**\n- `top:` Displays the users with the most amount of Cocoa Beans\n- `bank:` Displays curent balance of bank account\n- `bank register:` Registers a bank account\n- `bank @USERNAME:` Check the balance of anyone that you @mention\n- `pay @USERNAME AMOUNT:` Allows you to give money to users that you @mention\n\n**Utility Commands:**\n- `who:` Says who you are\n- `count:` Lists the number of users registered\n- `messages:` Lists the amount of messages you have sent\n- `definition WORD:` Finds the meaning of the word supplied \n\nCookie-bot made by HyperNebula\nVersion: v3.1")

    await ctx.message.author.send(embed=embed)


@bot.event
async def on_ready():
    print('Bot logged in as')
    print('Username: ' + bot.user.name)
    print('Id: ' + str(bot.user.id))
    print('--------')
    print(
        f'| Connected to {str(len(bot.guilds))} servers | Connected to {str(len(set(bot.get_all_members())))} users |')
    print(' Servers include:')
    for item in bot.guilds:
        print('  - {}'.format(item.name))
    print('--------')
    print(f'Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}')
    print('--------')
    print(f'Use this link to invite {bot.user.name}:')
    print(f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    print('--------')
    print('You are running CookieBot v3.1')
    print('Created by HyperNebula')
    return await bot.change_presence(activity=discord.Game(name='/help | The Waiting Game'))


bot.run(YourBotToken)
