from distutils.cmd import Command
import os
import random
from typing import Tuple
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule

bot = Bot(os.environ['API_KEY'])

@bot.on.message(text=['!help','!cmd']) #вызов списка доступных команд
async def command_list(message: Message):
    await message.answer("Список команд:\n !roll [от a до b] \n !echo [дублирует написанную фразу]")

@bot.on.message(CommandRule("roll",["!"],2,sep=" ")) #алгоритмы у вольво (теперь настраивается лол)
async def roller(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    rollstring = message.text[6:]
    rollstring = rollstring.strip()
    rollstring = rollstring.split()
    a = int(rollstring[0])
    b = int(rollstring[1])
    await message.answer("{}".format(users_info[0].first_name)+" rolls: "+"{}".format(random.randint(a,b)))

@bot.on.message(CommandRule("echo",["!"],1,sep="  ")) #дубликация ввода (костыльный)
async def echo_answer(message: Message):
    await message.answer(message.text[6:])

bot.run_forever()