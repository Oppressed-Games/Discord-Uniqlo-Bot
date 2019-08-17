import discord
from discord.ext import commands


class Uniqlo(commands.Cog):

    def __init__(self, client):
        self.client = client

    # Events

    # self must be passed in for Cog on_ready
    # self must be first parameter inside class
    @commands.Cog.listener()
    async def on_ready(self):
        print('Uniqlo cog am here')

    # Commands


def setup(client):
    client.add_cog(Uniqlo(client))
