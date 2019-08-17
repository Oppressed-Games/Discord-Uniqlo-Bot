import asyncio
import discord
import config
import re
import os
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#driver stuff ; find chromedriver.exe path
#chrome_path = r"C:..."
driver = webdriver.Chrome()
bot = commands.Bot(command_prefix="$")


@bot.event
async def on_ready():
    print("am here")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')  # splice off last 3 chars '.py'


#@bot.command(pass_context=True)
#async def foo(ctx, url):
#    if re.match('^https?://(www.)?uniqlo.com/.*$', url) is not None:
#        print("wow")
#    else:
#        print("not wow")


@bot.command(pass_context=True)
async def skormt(ctx):
    skirt = get_image()
    await ctx.send(skirt)


@bot.command(pass_context=True)
async def test(ctx, cmd):
    print(cmd)
    if cmd == "@everyone":
        await ctx.send("no")
    await ctx.send(cmd)


@bot.command(pass_context=True)
async def check(ctx, url):
    await ctx.send(get_stock(url))


def get_image():
    # send to uniqlo
    driver.get("https://www.uniqlo.com/us/en/women-front-button-circular-skirt-417764.html")
    image = driver.find_elements_by_class_name("primary-image")
    imageSRC = image[0].get_attribute("src")
    return imageSRC


def get_stock(url):
    result = ""
    driver.get(url)
    if re.match('^https?://(www.)?uniqlo.com/.*$', url) is not None:
        if len(driver.find_elements_by_class_name("outofstockbadge")) > 0:
            result = "Out of stock"
            return result
        else:
            result = "In stock"
            return result
    else:
        result = "that's not uniqlo"
        return result


#bot token
bot.run(config.token, reconnect=True)
