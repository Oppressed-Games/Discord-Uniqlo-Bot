import asyncio
import discord
import config
import os
from discord.ext import commands

bot = commands.Bot(command_prefix="$")


async def setup_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send('You do not have permission to use this command.')
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please enter the name of the cog as an argument.')
    else:
        await ctx.send(error)


async def setup_complete(ctx, setup_action, extension):
    await ctx.send(f'Successfully {setup_action}ed {extension} cog.')


@bot.event
async def on_ready():
    print("am here")


@bot.command()
@commands.has_permissions(administrator=True)
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')
    await setup_complete(ctx, 'load', extension)


@load.error
async def load_error(ctx, error):
    await setup_error(ctx, error)


@bot.command()
@commands.has_permissions(administrator=True)
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    await setup_complete(ctx, 'unload', extension)


@unload.error
async def unload_error(ctx, error):
    await setup_error(ctx, error)


@bot.command()
@commands.has_permissions(administrator=True)
async def reload(ctx, extension):
    bot.reload_extension(f'cogs.{extension}')
    await setup_complete(ctx, 'reload', extension)


@reload.error
async def reload_error(ctx, error):
    await setup_error(ctx, error)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')  # splice off last 3 chars '.py'


#bot token
bot.run(config.token, reconnect=True)
