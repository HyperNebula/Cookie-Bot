import csv
import time
import random
import logging
import asyncio
import account
import discord
import datetime
import platform
import pandas as pd
from discord.ext import commands
from discord.ext.commands import Bot


bot = commands.Bot(command_prefix='/')
bot.remove_command("help")


@bot.command(pass_context=True)
async def bank(ctx, regi: str = None):
    if regi is None:
        await bot.say(account.bal(ctx.message.author.id))
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
async def help(ctx):

    embed = discord.Embed(title="Cookie Bot Help", colour=discord.Colour(0xef41), description="This is a list of all the commands and their uses \n\n**Game Commands:**\n- `numgame:` Starts a number guessing game\n- `rob:` Try and steal some Cocoa Beans\n- `srob:` robs with 300 Cocoa Beans\n- `payday:` Recieve Cocoa Beans every 30 minutes\n- `roulette:` If you win, you double your Cocoa Beans\n\n**Currency Commands:**\n- `bank:` Displays curent balance of bank account\n- `bank register:` Registers a bank account\n- `top:` Displays the users with the most amount of Cocoa Beans\n- `give:` Allows you to give money to registered users\n\n**Utility Commands:**\n- `who:` says who you are\n- `count:` Lists the number of users registered\n- `messages:` Lists the amount of messages you have sent\n\nCookie-bot made by The Nexus")

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
    print('You are running CookieBot v2.4')
    print('Created by The Nexus')
    return await bot.change_presence(game=discord.Game(name='/help | The Waiting Game'))


bot.run('bot_id')
