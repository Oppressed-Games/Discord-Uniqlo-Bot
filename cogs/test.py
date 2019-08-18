import discord
import re
import bs4
import lxml
from timeit import default_timer as timer
import requests
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Test(commands.Cog):

    def __init__(self, client):
        self.client = client
        # driver stuff ; find chromedriver.exe path
        # chrome_path = r"C:..."
        self.driver = webdriver.Chrome()
        print('Opened web driver.')

    def cog_unload(self):
        if hasattr(self, 'driver'):
            self.driver.quit()
            print('Closed web driver.')

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
    async def skormt(self, ctx):
        skirt = await self.get_image(self, ctx)
        await ctx.send(skirt)

    @commands.command()
    async def skormt_bs4(self, ctx):
        skirt = await self.get_image_bs4(self, ctx)
        await ctx.send(skirt)

    @commands.command()
    async def test(self, ctx, cmd):
        print(cmd)
        if cmd == "@everyone":
            await ctx.send("no")
        await ctx.send(cmd)

    @commands.command()
    async def check(self, ctx, url):
        await ctx.send(self.get_stock(self, url))

    @commands.command()
    async def foo(self, ctx, url):
        if re.match('^https?://(www.)?uniqlo.com/.*$', url) is not None:
            ctx.send("wow")
        else:
            ctx.send("not wow")

    # Helpers

    @staticmethod
    async def get_image(self, ctx):
        # send to uniqlo
        start = timer()
        self.driver.get("https://www.uniqlo.com/us/en/women-front-button-circular-skirt-417764.html")
        image = self.driver.find_elements_by_class_name("primary-image")
        image_src = image[0].get_attribute("src")
        end = timer()
        await ctx.send(end - start)
        return image_src

    @staticmethod
    async def get_image_bs4(ctx):
        # send to uniqlo
        start = timer()
        res = requests.get("https://www.uniqlo.com/us/en/women-front-button-circular-skirt-417764.html")
        res.raise_for_status()
        soup = bs4.BeautifulSoup(res.text, "lxml")
        image = soup.select('img[class="primary-image"]')
        image_src = image[0].get('src')
        end = timer()
        await ctx.send(end - start)
        return image_src

    @staticmethod
    def get_stock(self, url):
        result = ""
        self.driver.get(url)
        if re.match('^https?://(www.)?uniqlo.com/.*$', url) is not None:
            if len(self.driver.find_elements_by_class_name("outofstockbadge")) > 0:
                result = "Out of stock"
                return result
            else:
                result = "In stock"
                return result
        else:
            result = "that's not uniqlo"
            return result


def setup(client):
    client.add_cog(Test(client))
