import time

print('Hello. This is where you will setup your Cookie-Bot')
time.sleep(1.5)
print('If you need help with this, look at the github page: https://github.com/HyperNebula/Cookie-Bot')
time.sleep(1.5)
print('What is your bot\'s token?')
token = input(' ')
print('What is your bot\'s user id?')
bot_id = input(' ')
print('What do you want the command prefix to be?')
prefix = input(' ')

fmt1 = 'YourBotToken = \'{}\'\n'
fmt2 = 'bot_it = \'{}\'\n'
fmt3 = 'prefix = \'{}\'\n'

lines = [fmt1.format(token), fmt2.format(bot_id), fmt3.format(prefix)]

with open('varibles.py', 'w') as file1:
    file1.writelines(lines)

