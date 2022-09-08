import json
import io
import os
import random
from urllib import response
import requests

api_key = os.environ['API_KEY_TENOR']
ckey = 'jabon gifs'
img_url = 'https://c.tenor.com/RBf5874ArDoAAAAC/frog.gif'
lmt = 25

def get_gif(tag = 'amogus'):
    response = requests.get(
    "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (tag, api_key, ckey,  lmt))

    if response.status_code == 200:
        data_json = json.loads(response.content)
        gif_get = requests.get(data_json['results'][random.randint(0,lmt-1)]['media_formats']['gif']['url'])
        with open('debug.gif','wb') as file:
            file.write(gif_get.content)
        with io.BytesIO() as gif_buff:
          gif_buff.write(gif_get.content)
          gif_buff.seek(0)
          return gif_buff.read()
    else:
        print("не удалось найти gif")
        print(f'код ошибки: {response.status_code}')



        


