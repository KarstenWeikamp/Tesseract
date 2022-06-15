# bot.py
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
import logging as log
import tesseract_bot.utils as utils

## Set globals and intents
load_dotenv()
TOKEN = os.getenv('TESSERACT_TOKEN')
version = "0.0.1"

utils.loggingSetup(log.INFO)


intents = discord.Intents.default()
intents.members = True
intents.guilds = True
intents.guild_reactions = True

snoezeldict = utils.openSnoezelDict()


bot = commands.Bot(command_prefix='+', intents=intents)



##Startup
@bot.event
async def on_ready():
    log.info("Starting Tesseract!")
    log.info("Logging in as {bot}!".format(bot=bot.user))
    log.info("We joined the following Servers:")
    async for guild in bot.fetch_guilds(limit=150):
        log.info("\t{0:<30} {1:<18}".format(guild.name, guild.id))

@bot.event
async def on_raw_reaction_add(payload):
    if payload.emoji.name == "➕":
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        if await utils.matchURL(msg.content):
            name = await utils.randintsr()
            snoezeldict[name] = msg.content
            await utils.saveSnoezeldict(snoezeldict)
            await  bot.get_channel(payload.channel_id).send("Added Image: {}".format(msg.content))



@bot.command()
async def version(ctx):
    await ctx.send("This is Tesseract version ** {0} ** created by Bloxx".format("0.0.1"))

##snoezel command group
@bot.group(invoke_winthout_command=True)
async def snoezel(ctx):
    snoezelpic = await utils.getRandomSnoezel(snoezeldict)
    await ctx.send(snoezelpic)

@snoezel.command()
async def add(ctx,name,url):
    if await utils.matchURL(url):
        log.debug("Added image to snozeldict")
        snoezeldict[name] = url
        await utils.saveSnoezeldict(snoezeldict)
        await ctx.send("Added {0} to snoezels! :tada:".format(name))
    else:
        await ctx.send("This doesn't seem to be a image url 😨")

@snoezel.command()
async def remove(ctx,name):
    if name in snoezeldict:
        del snoezeldict[name]
        ctx.send("Removed snoezel {name}, goodbye {name}!😭")

@snoezel.command()
async def invoke(ctx,name):
    if name in snoezeldict:
        ctx.send(snoezeldict[name])
    else:
        ctx.send("No such snoezel found! :anguished:")





bot.run(TOKEN)