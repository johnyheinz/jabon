import requests
import os
import random
import asyncio
from vkbottle.bot import Bot, Message

bot = Bot(os.environ['API_KEY'])

@bot.on.message(text=["!help","!cmd"]) #вызов списка доступных команд
async def hi_handler(message: Message):
    await message.answer("Список команд:\n !roll [ролл с доты]")


@bot.on.message(text=["!roll"]) #спизжено у вольво
async def roller(message: Message):
    users_info = await bot.api.users.get(message.from_id)
    await message.answer("{}".format(users_info[0].first_name)+" rolls: "+"{}".format(random.randint(0,100)))



bot.run_forever()