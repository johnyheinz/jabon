import os
import random
import game
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules.base import CommandRule
from vkbottle.dispatch.rules import ABCRule
from vkbottle import BaseMiddleware
from typing import Union

bot = Bot(os.environ['API_KEY'])

class NoBotMiddleware(BaseMiddleware[Message]): #проверка на ботов
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("bots are not allowed")

class ErrorMiddleware(BaseMiddleware[Message]):
    async def post(self):
        if (not self.handlers and self.event.text.startswith("!echo")):
            await self.event.answer("!echo [дублирует написанную фразу]")
        if (not self.handlers and self.event.text.startswith("!roll")):
            await self.event.answer("!roll [от a] [до b]")
        if (not self.handlers and self.event.text.startswith("!ssp")):
            await self.event.answer("!ssp [оружие: камень, ножницы, бумага|сложность: нормально, невозможно]")
        if (not self.handlers and self.event.text.startswith("!id")):
            await self.event.answer("!id [выдаёт ваш id]")
        if (not self.handlers and (self.event.text.startswith("!cmd") or self.event.text.startswith("!help"))):
            await self.event.answer("Список команд:\n !roll [от a] [до b] \n !echo [дублирует написанную фразу] \n !ssp [оружие: камень, ножницы, бумага|сложность: нормально, невозможно] \n !дайжабу [даёт 1 жабу] \n !id [выдаёт ваш id]")
        

class MyCommandRule(ABCRule[Message]):
    def __init__(
        self,
        command_text: str,
        args_count: int = 0,
        sep: str = " ",
    ):
        self.command_text = command_text if isinstance(command_text, str) else command_text[0]
        self.args_count = args_count if isinstance(command_text, str) else command_text[1]
        self.sep = sep

    async def check(self, event: Message) -> Union[dict, bool]:
            prefix = "!"
            if self.args_count == 0 and event.text == prefix + self.command_text: #команда без аргументов = true всегда
                return True
            if self.args_count > 0 and event.text.startswith(prefix + self.command_text + " "):
                args = event.text[len(prefix + self.command_text) + 1 :].split(self.sep)
                if len(args) != self.args_count:
                    return False
                elif any(len(arg) == 0 for arg in args):
                    return False
                return {"args": tuple(args)}

@bot.on.message(MyCommandRule("help")) #вызов списка доступных команд
async def command_list(message: Message):
    await message.answer("Список команд:\n !roll [от a] [до b] \n !echo [дублирует написанную фразу] \n !ssp [оружие: камень, ножницы, бумага|сложность: нормально, невозможно] \n !дайжабу [даёт 1 жабу] \n !id [выдаёт ваш id]")

@bot.on.message(MyCommandRule("roll",2,sep=" ")) #алгоритмы у вольво (теперь настраивается лол)
async def roller(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    rollstring = message.text[6:]
    rollstring = rollstring.strip()
    rollstring = rollstring.split()
    if ((type(rollstring[0]) is int) and (type(rollstring[1]) is int)): await message.answer("{}".format(users_info[0].first_name)+" rolls: "+"{}".format(random.randint(rollstring[0],rollstring[1])))
    else: await message.answer("!roll [от a] [до b]")

@bot.on.message(MyCommandRule("echo",1,sep="  ")) #дубликация ввода (костыльный)
async def echo_answer(message: Message):
    if (len(message.text)>4): await message.answer(message.text[6:])
    else: message.answer("!echo [дублирует написанную фразу]")
        
@bot.on.message(MyCommandRule("ssp",2,sep=" ")) #первая типа игра или что-то такое, скорее тест подключаемых модулей
async def sspgame(message: Message):
    sspstring = message.text[5:]
    sspstring = sspstring.strip()
    sspstring = sspstring.split()
    sspweapon = sspstring[0]
    sspdiffculty = sspstring[1]
    print(f"\n {sspweapon} \n")
    print(f"\n {sspdiffculty} \n")
    await message.answer(game.ssp(sspweapon,sspdiffculty))

@bot.on.message(MyCommandRule("дайжабу"))
async def give_jaba(message: Message):
    await message.answer(attachment="photo-206500138_457239019") 

@bot.on.message(MyCommandRule("id"))
async def getmyid(message: Message):
    await message.answer("Ваш id: "+"{}".format(message.from_id)) 

@bot.on.message(MyCommandRule("test"))
async def getmyid(message: Message):
    if ("{}".format(message.from_id) == "107329243"): await message.answer("вы еблан")
    else: await message.answer("вы не еблан")

bot.labeler.message_view.register_middleware(ErrorMiddleware)
bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.run_forever()