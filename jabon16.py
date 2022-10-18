import os
import random
import time
import game
import json
import tenorgif
import jabwiki
import jabondb_m
from datetime import timedelta
from typing import List
from vkbottle.bot import Bot, Message
from vkbottle.dispatch.rules import ABCRule
from vkbottle import BaseMiddleware, Keyboard, KeyboardButtonColor, Text, GroupEventType, GroupTypes, Bot, VKAPIError
from vkbottle.tools import template_gen, TemplateElement
from vkbottle.tools import DocMessagesUploader

bot = Bot(os.environ['API_KEY'])
servtoken = (os.environ['API_SERVICE_KEY'])

async def loadinfo():
    seek_id = 1
    while True:
        try:
            chatinfo = await bot.api.messages.get_conversation_members(peer_id=2000000000+seek_id)
            chatinfostr = chatinfo.json()
            chatinfojson = json.loads(chatinfostr)
            try:
                for profile in chatinfojson['profiles']:
                    getname = profile['first_name']
                    getid = profile['id']
                    getprivate = profile['is_closed']
                    try:
                        userget = await bot.api.users.get(getid, 'city')
                        getcity = userget[0].city.title
                    except: getcity = 'Не указано'
                    tupleinfo = (int(getid), str(getname), str(getcity), str(getprivate))
                    await jabondb_m.refreshdb(tupleinfo)
                seek_id += 1
            except Exception as e:
                print(f'\nОшибка загрузки в БД: {e}\n')
                seek_id += 1
        except VKAPIError[10]:
            print(f'\nКоличество бесед: {seek_id+1}\n')
            break
        except VKAPIError[917]:
            print('\nНе выданы права админа в чате\n')
            seek_id += 1

    if (time.localtime(0).tm_hour == 0): logtime = time.time()+10800
    else: logtime = time.time()
    gmlogtime = time.gmtime(logtime)
    if (gmlogtime.tm_min < 10): logmin = '0' + str(gmlogtime.tm_min)
    else: logmin = gmlogtime.tm_min
    if (gmlogtime.tm_sec < 10): logsec = '0' + str(gmlogtime.tm_sec)
    else: logsec = gmlogtime.tm_sec
    await bot.api.messages.send(chat_id='5', message=f'[{gmlogtime.tm_hour}:{logmin}:{logsec}]\n'+'JABON запущен', random_id=0) #просто по приколу =)

keyboard = Keyboard(one_time=False, inline=False)
keyboard.add(Text(label="!помощь"), color=KeyboardButtonColor.PRIMARY)
keyboard.row()
keyboard.add(Text("!дайжабу"), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text("!гиф жаба"), color=KeyboardButtonColor.SECONDARY)
keyboard.row()
keyboard.add(Text("!монетка"), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text("!ролл"), color=KeyboardButtonColor.SECONDARY)
keyboard.add(Text("!профиль"), color=KeyboardButtonColor.SECONDARY)
keyboard = keyboard.get_json()


class NoBotMiddleware(BaseMiddleware[Message]): #проверка на ботов
    async def pre(self):
        if self.event.from_id < 0:
            self.stop("bots are not allowed")

class ErrorMiddleware(BaseMiddleware[Message]):
    async def post(self):
        if (not self.handlers and self.event.text.startswith("!эхо")):
            await self.event.answer("!эхо [дублирует написанную фразу]")
        if (not self.handlers and self.event.text.startswith("!кнб")):
            await self.event.answer("!кнб [оружие: камень, ножницы, бумага|сложность: нормально, невозможно]")
        if (not self.handlers and self.event.text.startswith("!профиль добавить город")):
            await self.event.answer("Введите город")
        if (not self.handlers and self.event.text.startswith("!гиф")):
            await self.event.answer("!гиф [тег] (отправляет гифку по заданному тегу)")
        if (not self.handlers and self.event.text.startswith(['!вики','!Вики','!wiki'])):
            await self.event.answer("Пустой запрос")
        if (not self.handlers and self.event.text.startswith(['concept','idea','идея','хочудобавить','хочу','report','репорт','предложение'])):
            await self.event.answer("молодец =)\n а теперь напиши что-нибудь существенное")

class LogMiddleware(BaseMiddleware[Message]): #типа логи команд...
    async def post(self):
        if (self.event.text.startswith('!')):
            if (time.localtime(0).tm_hour == 0): logtime = time.localtime(self.event.date+10800)
            else: logtime = time.localtime(self.event.date)
            if (logtime.tm_min < 10): logmin = '0' + str(logtime.tm_min)
            else: logmin = logtime.tm_min
            if (logtime.tm_sec < 10): logsec = '0' + str(logtime.tm_sec)
            else: logsec = logtime.tm_sec
            userinfo = await bot.api.users.get(self.event.from_id)
            if (userinfo[0].id == 107329243):
                if (not self.handlers):
                    await bot.api.messages.send(
                    chat_id = '5', 
                    message=f'[{logtime.tm_hour}:{logmin}:{logsec}]\n'+
                    f'Chat ID: {self.event.chat_id}\n'+
                    f'Ты не смог исполнить команду:\n{self.event.text}',
                    random_id=0)
                else:
                    await bot.api.messages.send(
                    chat_id = '5', 
                    message=f'[{logtime.tm_hour}:{logmin}:{logsec}]\n'+
                    f'Chat ID: {self.event.chat_id}\n'+
                    f'Ты исполнил команду:\n{self.event.text}',
                    random_id=0)
            else:
                if (not self.handlers):
                    await bot.api.messages.send(
                    chat_id = '5', 
                    message=f'[{logtime.tm_hour}:{logmin}:{logsec}]\n'+
                    f'Chat ID: {self.event.chat_id}\n'+
                    f'@id{userinfo[0].id} ({userinfo[0].first_name}  {userinfo[0].last_name}) ({userinfo[0].id}) не смог исполнить команду:\n{self.event.text}',
                    random_id=0)
                else:
                    await bot.api.messages.send(
                    chat_id = '5', 
                    message=f'[{logtime.tm_hour}:{logmin}:{logsec}]\n'+
                    f'Chat ID: {self.event.chat_id}\n'+
                    f'@id{userinfo[0].id} ({userinfo[0].first_name}  {userinfo[0].last_name}) ({userinfo[0].id}) исполнил команду:\n{self.event.text}',
                    random_id=0)

class MyCommandRule(ABCRule[Message]):
    def __init__(
        self,
        command_text: List[str],
        args_count: int = 0,
        sep: str = " ",
    ):
        self.command_text = command_text if isinstance(command_text, list) else command_text.split(sep=None, maxsplit=-1)
        self.args_count = args_count
        self.sep = sep

    async def check(self, event: Message) -> bool:
        prefix = '!'
        cmd_text = self.command_text[0]

        if (len(self.command_text) == 1):
            cmd_text = self.command_text[0]
        else:
            for x in self.command_text:
                if ((x == event.text[1:event.text.find(' ')]) or (x == event.text[1:])): cmd_text = x

        if self.args_count == 0 and event.text == prefix + cmd_text:
                return True
        if self.args_count > 0 and event.text.startswith(prefix + cmd_text + " "):
            args = event.text[len(prefix + cmd_text) + 1 :].split(self.sep)
            if len(args) != self.args_count:
                    return False
            elif any(len(arg) == 0 for arg in args):
                    return False
            return {"args": tuple(args)}

with open('cmd.txt', encoding="utf8") as file:
    cmd_str = file.read()
    file.close()

@bot.on.raw_event(GroupEventType.WALL_POST_NEW, dataclass=GroupTypes.WallPostNew) #суперсырая пересылка
async def repost_konfa(event: GroupTypes.WallPostNew):
        wallinfo = await bot.api.wall.get(access_token = servtoken, owner_id='-206500138', count = 2)
        wallinfostr = wallinfo.json()
        wallinfojson = json.loads(wallinfostr)
        postid = wallinfojson['items'][1]['id']
        await bot.api.messages.send(chat_id='4', attachment=(f'wall-206500138_{postid}'), random_id=0)
        await bot.api.messages.send(chat_id='7', attachment=(f'wall-206500138_{postid}'), random_id=0)


@bot.on.message(MyCommandRule(['помощь','команды','cmd','help'])) #вызов списка доступных команд
async def command_list(message: Message):
    await message.answer(cmd_str)

@bot.on.message(MyCommandRule(['roll','ролл','random','рандом'])) #алгоритмы у вольво (теперь настраивается лол)
async def roller_no_arg(message: Message):
   users_info = await bot.api.users.get(message.from_id)
   await message.reply("{}".format(users_info[0].first_name)+" роллит: "+"{}".format(random.randint(0,100)))

@bot.on.message(MyCommandRule(['concept','idea','идея','хочудобавить','хочу','report','репорт','предложение'],1,sep='  ')) #продолжаем пиздить у вольво
async def reporto(message: Message):
    await message.reply('Предложение добавлено')
    userinfo = await bot.api.users.get(message.from_id)
    report_text = message.text
    await bot.api.messages.send(chat_id='6', message=f'@id{userinfo[0].id} ({userinfo[0].first_name}) предложил: '+report_text[report_text.find(' ')+1:], random_id=0)

@bot.on.message(MyCommandRule(['roll','ролл','random','рандом'],2)) 
async def roller(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    rollstring = message.text[6:]
    rollstring = rollstring.strip()
    rollstring = rollstring.split()
    if (rollstring[0].lstrip('-').isdigit() and rollstring[1].lstrip('-').isdigit()): await message.reply("{}".format(users_info[0].first_name)+" роллит: "+"{}".format(random.randint(int(rollstring[0]),int(rollstring[1]))))
    else: await message.reply("{}".format(users_info[0].first_name)+" роллит: "+"{}".format(random.randint(0,100)))

@bot.on.message(MyCommandRule("эхо",1,'  ')) #дубликация ввода
async def echo_answer(message: Message):
    if (len(message.text)>4): await message.answer(message.text[5:])
    else: message.answer("!эхо [дублирует написанную фразу]")
        
@bot.on.message(MyCommandRule("кнб",2,sep=" ")) #первая типа игра или что-то такое, скорее тест подключаемых модулей
async def sspgame(message: Message):
    sspstring = message.text[5:]
    sspstring = sspstring.strip()
    sspstring = sspstring.split()
    sspweapon = sspstring[0]
    sspdiffculty = sspstring[1]
    await message.answer(game.ssp(sspweapon,sspdiffculty))

@bot.on.message(MyCommandRule("дайжабу")) #даёт 1 жабу
async def give_jaba(message: Message):
    await message.reply(attachment="photo-206500138_457239019") 

@bot.on.message(MyCommandRule("дайкарусельжаб")) #даёт вроде как целую карусель жаб
async def give_megajaba(message: Message):
    my_template = template_gen(TemplateElement(title="жаба.png",description="да это реально жаба",photo_id="photo-206500138_457239019",action="None",buttons="жабы"))
    await message.answer("К А Р У С Е Л Ь  Ж А Б", template=my_template)

@bot.on.private_message(MyCommandRule(['start','старт','клава']))
async def send_keyboard(message: Message):
   await message.answer("Клавиатура выдана", keyboard=keyboard)

@bot.on.message(MyCommandRule(['gif','гиф'],1,'  ')) #парс гифок с тенора
async def gif_dealer(message: Message):
    if ('|' in message.text): 
        user_tag_gif = message.text[5:message.text.find('|')]
        accuracy = message.text[message.text.find('|')+1:]
    else: 
        user_tag_gif = message.text[5:]
        accuracy = 10
    doc = await DocMessagesUploader(bot.api).upload(file_source=tenorgif.get_gif(user_tag_gif, accuracy), title=f"{user_tag_gif}"+'.gif', peer_id=message.peer_id)
    await message.reply(attachment=doc)

@bot.on.message(text=['иди нахуй','Иди нахуй','пошёл нахуй','Пошёл нахуй']) #искусственный интеллект
async def reflection(message: Message):
    await message.reply('ты такие вещи прекращай говорить да')

@bot.on.message(MyCommandRule(['монетка','flip','флип'])) #кек
async def flipmacoin(message: Message):
    if (random.randint(0,1) == 1): await message.reply('решка')
    else: await message.reply('орёл')

@bot.on.message(MyCommandRule(['Вики','вики','wiki'],1,'  ')) #вики
async def wikimodule(message: Message):
    if ('|' in message.text): 
        wiki_tag = message.text[6:message.text.find('|')]
        language = message.text[message.text.find('|')+1:]
    else: 
        wiki_tag = message.text[6:]
        language = 'ru'
    await message.reply(jabwiki.findpage(wiki_tag,language))

@bot.on.message(MyCommandRule('профиль'))
async def defprofile(message: Message):
        userprofile = await jabondb_m.giveinfodb(message.from_id)
        if (userprofile[3] == 'True'): isclosed = 'Закрытый'
        else: isclosed = 'Открытый'
        usertextprofile = f'\nID: {userprofile[0]}\n Город: {userprofile[2]}\n Профиль: {isclosed}'
        await message.reply(usertextprofile)

@bot.on.message(MyCommandRule('профиль',1,'  '))
async def defprofileexp(message: Message):
    if ('!профиль добавить город' in message.text):
        getcity = message.text[message.text.find('город ')+6:]
        citytuple = (message.from_id, getcity)
        await jabondb_m.updatecity(citytuple)
        await message.reply('Профиль обновлён')

@bot.on.message(MyCommandRule("test"))
async def test_handler(message: Message):
    if ("{}".format(message.from_id) == "107329243"): 
        users_info = await bot.api.users.get('207191498','city')
        await message.answer(f'{users_info[0].first_name} {users_info[0].last_name}: {users_info[0].city.title}')
    else: await message.answer("вы не еблан чтобы это делать")

bot.labeler.message_view.register_middleware(ErrorMiddleware)
bot.labeler.message_view.register_middleware(NoBotMiddleware)
bot.labeler.message_view.register_middleware(LogMiddleware)
bot.loop_wrapper.add_task(loadinfo())
bot.run_forever()