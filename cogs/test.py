import discord
import re
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

#driver stuff ; find chromedriver.exe path
#chrome_path = r"C:..."
driver = webdriver.Chrome()


def get_image():
    # send to uniqlo
    driver.get("https://www.uniqlo.com/us/en/women-front-button-circular-skirt-417764.html")
    image = driver.find_elements_by_class_name("primary-image")
    image_src = image[0].get_attribute("src")
    return image_src


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


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # self must be passed in for Cog on_ready
    # self must be first parameter inside class
    @commands.Cog.listener()
    async def on_ready(self):
        print('Testing cog am here')

    # Commands

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! {round(self.client.latency * 1000)}ms');

    @commands.command()
    async def skormt(self):
        skirt = get_image()
        await self.send(skirt)

    @commands.command()
    async def test(self, cmd):
        print(cmd)
        if cmd == "@everyone":
            await self.send("no")
        await self.send(cmd)

    @commands.command()
    async def check(self, url):
        await self.send(get_stock(url))

    @commands.command()
    async def foo(self, url):
        if re.match('^https?://(www.)?uniqlo.com/.*$', url) is not None:
            print("wow")
        else:
            print("not wow")


def setup(client):
    client.add_cog(Test(client))
