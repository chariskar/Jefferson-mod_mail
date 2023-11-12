import os
import disnake
import dotenv
from disnake.ext import commands
from disnake.ext.commands import InteractionBot
from dotenv import load_dotenv
load_dotenv()


bot: InteractionBot = commands.InteractionBot()

for file in os.listdir('cogs'):
    if file.endswith('py'):
        bot.load_extension(f'cogs.{file[:-3]}')


@bot.event
async def on_ready():

    await bot.change_presence(activity=disnake.Game(name=f"operating in {len(bot.guilds)} guilds"))

    print(f"Logged in as {bot.user}")
    print(f"Operating in {len(bot.guilds)} guild/s")
    print(f'Presence is playing : play.earthmc.net')


try:
    token: str = dotenv.get_key('TOKEN.env', 'TOKEN')
    bot.run(token)
except Exception as e:
    raise e
