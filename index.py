import discord, json
import mysql.connector as mysql
from discord.ext import commands
# Cogs
from cogs.ticket_system import TicketSystem
from cogs.management_system import ManagementPanel
from cogs.statuses import Statuses
from cogs.project_management import ProjectManagement
from cogs.utilities import Utilites
from cogs.system import System
from cogs.invoice import Invoice
from cogs.logging import Logging
from cogs.welcome import Welcome
from cogs.reaction_roles import ReactionRoles
from cogs.chatgpt import ChatGPT

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

with open('config.json', 'r') as f:
    config = json.load(f)
    db_config = {
        'host': config['database']['host'],
        'user': config['database']['user'],
        'password': config['database']['password'],
        'database': config['database']['database'],
    }

@bot.event
async def on_ready():
    await bot.add_cog(TicketSystem(bot))
    await bot.add_cog(ManagementPanel(bot))
    await bot.add_cog(Statuses(bot))
    await bot.add_cog(ProjectManagement(bot))
    await bot.add_cog(Utilites(bot))
    await bot.add_cog(System(bot))
    await bot.add_cog(Invoice(bot))
    await bot.add_cog(Logging(bot))
    await bot.add_cog(Welcome(bot))
    await bot.add_cog(ReactionRoles(bot))
    await bot.add_cog(ChatGPT(bot))

    Statuses.update_schedule_embed.start()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CoderZ code!"))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

with open('config.json', 'r+') as f:
    config = json.load(f)
    if config['botkey'] == "":
        config['botkey'] = input("Please enter your bot key: ")
        bot.run(config['botkey'])
        with open('config.json', 'w+') as f:
            json.dump(config, f, indent=4)
    else:
        bot.run(config['botkey'])
