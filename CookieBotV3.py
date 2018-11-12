import random
import asyncio
import account
import discord
import platform
from discord.ext import commands
from varibles import *


bot = commands.Bot(command_prefix=commands.when_mentioned_or(prefix))
bot.remove_command("help")


@bot.command(pass_context=True)
async def bank(ctx, regi: str = None):
    if regi is None:
        if account.bal(ctx.message.author.id) == "Please register first using `/bank register`":
            await bot.say("Please register first using `/bank register`")
            return
        else:
            embed = discord.Embed(title="Bank Account info:", colour=discord.Colour(0xf5a623), description="Your balance is: `{}`".format(account.bal(ctx.message.author.id)))
            await bot.say(embed=embed)
            return
    elif regi == "register":
        await bot.say(account.register(ctx.message.author.id))
        return
    elif regi.startswith("<@!"):
        await bot.say("That user is a bot and cannot have an account")
        return
    elif regi.startswith("<@"):
        await bot.say(account.obal(regi.strip("<@>")))
        return


@bot.command()
async def top():
    leadboard = account.top()
    name1 = await bot.get_user_info(leadboard[0][0])
    name2 = await bot.get_user_info(leadboard[1][0])
    name3 = await bot.get_user_info(leadboard[2][0])
    name4 = await bot.get_user_info(leadboard[3][0])
    name5 = await bot.get_user_info(leadboard[4][0])

    fmt = '1.`{0.display_name}`: {1}2.`{2.display_name}`: {3}3.`{4.display_name}`: {5}4.`{6.display_name}`: {7}5.`{8.display_name}`: {9}'
    board = fmt.format(name1, leadboard[0][1] + '\n', name2, leadboard[1][1] + '\n', name3, leadboard[2][1] + '\n', name4, leadboard[3][1] + '\n', name5, leadboard[4][1])

    embed = discord.Embed(title="Leaderboard", colour=discord.Colour(0x724ded), description=board)
    await bot.say(embed=embed)


@bot.command(pass_context=True)
async def pay(ctx, user: str = None, amount=None):
    if user is None:
        await bot.say("Please specify the target user using this format: `/pay @USERNAME AMOUNT`")
        return
    if amount is None:
        await bot.say("Please specify the payment amount using this format: `/pay @USERNAME AMOUNT`")
        return
    try:
        amount = int(amount)
    except ValueError:
        await bot.say("Please only use whole numbers")
        return
    if user.startswith("<@!"):
        await bot.say("That user is a bot and cannot have an account")
        return
    await bot.say(account.pay(ctx.message.author.id, user.strip("<@>"), amount))


@bot.command(pass_context=True)
async def payday(ctx):
    await bot.say(account.payday(ctx.message.author.id))


@bot.command(pass_context=True)
async def numgame(ctx):
    if account.bal(ctx.message.author.id) == "Please register first using `/bank register`":
        await bot.say("Please register first using `/bank register`")
        return

    await bot.say('Guess a number between 1 to 100')

    answer = random.randint(1, 100)
    guessnumber = 0

    def guess_check(m):
        return m.content.isdigit()
    while guessnumber < 6:
        guess = await bot.wait_for_message(timeout=10.0, author=ctx.message.author, check=guess_check)
        guessnumber = guessnumber + 1

        if guess is None:
            fmt = 'Sorry, you took too long. It was {}.'
            await bot.say(fmt.format(answer))
            break
        await bot.say(account.numgame(ctx.message.author.id, int(guess.content), guessnumber, answer))

        if int(guess.content) == answer:
            break


@bot.command(pass_context=True)
async def rob(ctx, ramount=None):
    if ramount is None:
        await bot.say("Please supply the amount you are robbing with using this format: `/rob AMOUNT`")
        return
    try:
        ramount = int(ramount)
    except ValueError:
        await bot.say("Please only use whole numbers")
        return
    await bot.say(account.rob(ctx.message.author.id, ramount))


@bot.command(pass_context=True)
async def srob(ctx):
    await bot.say(account.rob(ctx.message.author.id, 300))


@bot.command()
async def definition(*, word: str = None):
    await bot.say(account.definition(word))


@bot.command(pass_context=True)
async def help(ctx):
    embed = discord.Embed(title="Cookie Bot Help", colour=discord.Colour(0xef41), description="This is a list of all the commands and their uses \n\n**Game Commands:**\n- `rob AMOUNT:` Bet an amount of Cocoa Beans and try and steal some more\n- `srob:` robs with 300 Cocoa Beans\n- `payday:` Recieve Cocoa Beans every 30 minutes\n- `numgame:` Starts a number guessing game\n- `roulette:` If you win, you double your Cocoa Beans\n\n**Currency Commands:**\n- `top:` Displays the users with the most amount of Cocoa Beans\n- `bank:` Displays curent balance of bank account\n- `bank register:` Registers a bank account\n- `bank @USERNAME:` Check the balance of anyone that you @mention\n- `pay @USERNAME AMOUNT:` Allows you to give money to users that you @mention\n\n**Utility Commands:**\n- `who:` Says who you are\n- `count:` Lists the number of users registered\n- `messages:` Lists the amount of messages you have sent\n- `definition WORD:` Finds the meaning of the word supplied \n\nCookie-bot made by The Nexus\nVersion: 3.2 Beta")

    await bot.send_message(ctx.message.author, embed=embed)


@bot.event
async def on_ready():
    print('Bot logged in as')
    print('Username: ' + bot.user.name)
    print('Id: ' + bot.user.id)
    print('--------')
    print(
        f'| Connected to {str(len(bot.servers))} servers | Connected to {str(len(set(bot.get_all_members())))} users |')
    print(' Servers include:')
    for item in bot.servers:
        print('  - {}'.format(item.name))
    print('--------')
    print(f'Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}')
    print('--------')
    print(f'Use this link to invite {bot.user.name}:')
    print(f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    print('--------')
    print('You are running CookieBot v3.0 Beta.2')
    print('Created by HyperNebula')
    return await bot.change_presence(game=discord.Game(name='/help | The Waiting Game'))


bot.run(YourBotToken)
