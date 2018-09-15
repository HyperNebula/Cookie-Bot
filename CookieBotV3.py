import time
import random
import asyncio
import account
import discord
import datetime
import platform
from discord.ext import commands
from discord.ext.commands import Bot


bot = commands.Bot(command_prefix='/')
bot.remove_command("help")


@bot.command(pass_context=True)
async def bank(ctx, regi: str = None):
    if regi is None:
        await bot.say("Your balance is {}".format(account.bal(ctx.message.author.id)))
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


@bot.command(pass_context=True)
async def top(ctx):
    leadboard = account.top()
    name1 = await bot.get_user_info(leadboard[0][0])
    name2 = await bot.get_user_info(leadboard[1][0])
    name3 = await bot.get_user_info(leadboard[2][0])
    name4 = await bot.get_user_info(leadboard[3][0])
    name5 = await bot.get_user_info(leadboard[4][0])

    fmt = '1.`{0.display_name}`: {1}2.`{2.display_name}`: {3}3.`{4.display_name}`: {5}4.`{6.display_name}`: {7}5.`{8.display_name}`: {9}'
    board = fmt.format(name1, leadboard[0][1], name2, leadboard[1][1], name3, leadboard[2][1], name4, leadboard[3][1], name5, leadboard[4][1])

    embed = discord.Embed(title="Leaderboard", colour=discord.Colour(0x724ded), description=board)
    await bot.send_message(ctx.message.channel, embed=embed)


@bot.command(pass_context=True)
async def pay(ctx, user: str, amount: int):
    if user.startswith("<@!"):
        await bot.say("That user is a bot and cannot have an account")
        return
    await bot.say(account.pay(ctx.message.author.id, user.strip("<@>"), amount))


@bot.command(pass_context=True)
async def help(ctx):

    embed = discord.Embed(title="Cookie Bot Help", colour=discord.Colour(0xef41), description="This is a list of all the commands and their uses \n\n**Game Commands:**\n- `numgame:` Starts a number guessing game\n- `rob:` Try and steal some Cocoa Beans\n- `srob:` robs with 300 Cocoa Beans\n- `payday:` Recieve Cocoa Beans every 30 minutes\n- `roulette:` If you win, you double your Cocoa Beans\n\n**Currency Commands:**\n- `top:` Displays the users with the most amount of Cocoa Beans\n- `bank:` Displays curent balance of bank account\n- `bank register:` Registers a bank account\n- `bank @USERNAME:` check the balance of anyone that you @mention\n- `pay @USERNAME AMOUNT:` Allows you to give money to users that you @mention\n\n**Utility Commands:**\n- `who:` says who you are\n- `count:` Lists the number of users registered\n- `messages:` Lists the amount of messages you have sent\n\nCookie-bot made by The Nexus\nVersion: 3.0 Beta")

    await bot.send_message(ctx.message.author, embed=embed)

@bot.event
async def on_ready():
    print('Bot logged in as')
    print('Username: ' + bot.user.name)
    print('Id: ' + bot.user.id)
    print('--------')
    print(
        f'| Connected to {str(len(bot.servers))} servers | Connected to {str(len(set(bot.get_all_members())))} users |')
    print('--------')
    print(f'Current Discord.py Version: {discord.__version__} | Current Python Version: {platform.python_version()}')
    print('--------')
    print(f'Use this link to invite {bot.user.name}:')
    print(f'https://discordapp.com/oauth2/authorize?client_id={bot.user.id}&scope=bot&permissions=8')
    print('--------')
    print('You are running CookieBot v3.0 Beta')
    print('Created by The Nexus')
    return await bot.change_presence(game=discord.Game(name='/help | The Waiting Game'))


bot.run('YourTokenHere')
