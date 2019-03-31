#!/usr/bin/python3
#https://github.com/FooSoft/anki-connect
from urllib.parse import urlencode
import requests
import json
import random
import re
import io
from wand.color import Color
from wand.image import Image
from wand.image import Font
import subprocess

anki_address = '192.168.0.115'

TAG_RE = re.compile(r'<[^>]+>')
def remove_tags(text):
    return TAG_RE.sub('', text)

url = 'http://' + anki_address  + ':8765/'
events=""
subject=""
result=""

image_width = 264
image_height = 176

# get deck names and ids
params = {
    "action": "deckNamesAndIds",
    "version": 6
}
response = requests.get(url, data=json.dumps(params))
#print(json.dumps(response.json(), indent=4, sort_keys=True))

deckNames = []
for name in response.json()['result']:
    deckNames.append(name)

#deckIds = []
#for deckId in deckNames:
#    deckIds.append(str(response.json()['result'][deckId]))

#deckIds.remove("1")
deckNames.remove("Default")

randomChoice = str(random.choice(deckNames))
#print("Deck Choice: " + randomChoice)
# select from a random deck
params = {
    "action": "findCards",
    "version": 6,
    "params": {
        "query": ["deck:" + randomChoice]
    }
}
response = requests.get(url, data=json.dumps(params))
#print(json.dumps(response.json(), indent=4, sort_keys=True))

cardList = []
cardCount = 0
# get only card id's from 
for cardId in response.json()['result']:
    cardList.append(cardId)
    cardCount += 1

# select a specific card
getCardId = random.choice(cardList)
#print("Card ID: " + str(getCardId))
params = {
    "action": "cardsInfo",
    "version": 6,
    "params": {
        "cards": [getCardId]
    }
}
response = requests.get(url, data=json.dumps(params))
#print(json.dumps(response.json(), indent=4, sort_keys=True))

front = ''
back = ''
for field in response.json()['result']:
    back = field['fields']['Back']['value']
    front = field['fields']['Front']['value']

font_size = 36

front = remove_tags(front)
back = remove_tags(back)

char_count = len(front) + len(back)

if char_count > 50:
    font_size = 22

text_file = io.open('/run/user/1000/latest.txt', 'w', encoding='utf-8')
text_file.write(str(getCardId))
text_file.close()
text_file = io.open('/run/user/1000/front.txt', 'w', encoding='utf-8')
text_file.write(front)
text_file.close()
text_file = io.open('/run/user/1000/back.txt', 'w', encoding='utf-8')
text_file.write(back)
text_file.close()

def create_image_caption(widthsize,heightsize,backgroundcolor,image_caption,text_color,font_size):
    with Image(width=widthsize,height=heightsize,background=Color(backgroundcolor)) as image:
        font=Font(path='/usr/share/fonts/truetype/unfonts-core/UnBatang.ttf',size=font_size,color=Color(text_color))
        image.caption(image_caption,left=0,top=0,width=widthsize-10,height=heightsize-5,font=font)
        image.save(filename="/run/user/1000/tmpimage.jpg")
# set the caption text
caption_text = front+"\n"+back
# create the image
create_image_caption(image_width,image_height,'white',caption_text,'black',20)
subprocess.Popen(['/home/pi/papirus/papirus-draw', '/run/user/1000/tmpimage.jpg'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

