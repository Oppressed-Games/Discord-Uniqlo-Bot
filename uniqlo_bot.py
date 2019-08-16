import asyncio
import discord
import config
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


@bot.command(pass_context=True)
async def pastebin(ctx):
    posts = get_paste()
    for post in posts:
        if post != " ":
            await ctx.send(post.text)


@bot.command(pass_context=True)
async def skormt(ctx):
    skirt = get_image()
    await ctx.send(skirt)


def get_paste():
    # testing browser
    driver.get("http://pastebin.com/LhX55TNJ")
    posts = driver.find_elements_by_class_name("de1")
    return posts


def get_image():
    # send to uniqlo
    driver.get("https://www.uniqlo.com/us/en/women-front-button-circular-skirt-417764.html")

    image = driver.find_elements_by_class_name("primary-image")
    imageSRC = image[0].get_attribute("src")
    return imageSRC

#bot token
bot.run(config.token, reconnect=True)
