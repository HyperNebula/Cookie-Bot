import csv
import time
import random
import logging
import asyncio
import discord
import platform
import pandas as pd
from discord.ext import commands
from discord.ext.commands import Bot


description = '''Cookie-bot made by The Nexus'''

bot = commands.Bot(command_prefix='/', description=description)
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

channel = 'Channel_Id'  # channel id for logs


@bot.event
async def on_message_edit(before, after):
    if after.author == bot.user:
        return

    fmt = '**{0.author}** edited their message:\n{1.content}'
    await bot.send_message(discord.Object(id=channel), fmt.format(after, before))


@bot.event
async def on_message_delete(message):
    if message.author == bot.user:
        return

    fmt = '{0.author.name} has deleted the message:\n{0.content}'
    await bot.send_message(discord.Object(id=channel), fmt.format(message))




@bot.event
async def on_ready():
    print('Bot logged in as')
    print('Username: ' + bot.user.name)
    print('Id: ' + bot.user.id)
    print('--------')
    print('| Connected to ' + str(len(bot.servers)) + ' servers | Connected to ' +
          str(len(set(bot.get_all_members()))) + ' users |')
    print('--------')
    # print('| Servers: ' + str(bot.servers) + ' |')
    # print('| Users: ' + str(set(bot.get_all_members())) + ' |')
    # print('--------')
    print('Current Discord.py Version: {} | Current Python Version: {}'.format(
        discord.__version__, platform.python_version()))
    print('--------')
    print('Use this link to invite {}:'.format(bot.user.name))
    print('https://discordapp.com/oauth2/authorize?client_id={}&scope=bot&permissions=8'.format(bot.user.id))
    print('--------')
    print('You are running CookieBot v2.4')
    print('Created by The Canadian\'s friend')
    return await bot.change_presence(game=discord.Game(name='/help | The Waiting Game'))
