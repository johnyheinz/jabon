import os
import random
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle import BaseMiddleware
import game

bot = Bot(os.environ['API_KEY'])

class LogMiddleware(BaseMiddleware[Message]):
    async def post(self):
        if not self.handlers:
            return
        print("\n"+f"{self.handle_responses}"+"\n")

@bot.on.message(text=['!help','!cmd']) #вызов списка доступных команд
async def command_list(message: Message):
    await message.answer("Список команд:\n !roll [от a до b] \n !echo [дублирует написанную фразу] \n !ssp [оружие: камень, ножницы, бумага|сложность: нормально, невозможно]")

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

@bot.on.message(CommandRule("ssp",["!"],2,sep=" ")) #первая типа игра или что-то такое, скорее тест подключаемых модулей
async def sspgame(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    sspstring = message.text[5:]
    sspstring = sspstring.strip()
    sspstring = sspstring.split()
    sspweapon = sspstring[0]
    sspdiffculty = sspstring[1]
    print(f"\n {sspweapon} \n")
    print(f"\n {sspdiffculty} \n")
    await message.answer(game.ssp(sspweapon,sspdiffculty))

bot.labeler.message_view.register_middleware(LogMiddleware)
bot.run_forever()
