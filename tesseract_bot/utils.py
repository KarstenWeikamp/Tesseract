import logging as log
import random
import json
import datetime
import re

def loggingSetup(logLevel):
    log.basicConfig(
        level=logLevel,
        format='[%(asctime)s]-[%(levelname)s]:%(message)s',
        datefmt='%d-%m %H:%M:%S',
        handlers=[
            log.FileHandler("tesseract.log"),
            log.StreamHandler()
            ]
        )

async def get_user_from_ctx(ctx):
    for i in ctx.guild:
        if i.userid == ctx.author.id:
            return i

async def getRandomSnoezel(snoezeldict):
    try:
        randomSnoezelkey = random.choice(list(snoezeldict.keys()))
        randomSnoezel = snoezeldict[randomSnoezelkey]
    except:
        log.error("Can't select random snoezel")
        randomSnoezel = 'bloxx.Tesseract.NoRandomSnoezelErr'
    return randomSnoezel

async def matchURL(imstring):
    return re.search("(http(s?):)([/|.|\w|\s|-])*\.(?:jpg|gif|png)",imstring)

def openSnoezelDict():
    try:
        with open('snoezel.json','r') as file:
            snoezeldict = json.load(file)
    except IOError:
        log.info("No snoezel.json found initializing empty dict")
        snoezeldict = {}
    return snoezeldict

async def saveSnoezeldict(snoezeldict):
    try:
        with open('snoezel.json','w') as file:
            json.dump(snoezeldict,file,sort_keys=True,indent=4)
    except:
        log.error("Snoezeldict couldn't be saved!")

async def randintsr():
    return str(random.randrange(0,99999))

async def startsWithLetter(text):
    return re.search("^[a-zA-Z\u00c4\u00e4\u00d6\u00f6\u00dc\u00fc].*",text)
