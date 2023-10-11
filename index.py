import discord, json, sqlite3
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

conn = sqlite3.connect("data/coderz.db")
cursor = conn.cursor()

cursor.executescript('''
    BEGIN;
    CREATE TABLE IF NOT EXISTS developers (
        user_id INTEGER PRIMARY KEY,
        developer_name TEXT,
        developer_rank TEXT,
        status TEXT
    );
    CREATE TABLE IF NOT EXISTS certified_roles (
        developer_id INTEGER,
        role_name TEXT,
        FOREIGN KEY (developer_id) REFERENCES developers (user_id)
    );
    CREATE TABLE IF NOT EXISTS projects (
        project_id TEXT PRIMARY KEY,
        game TEXT,
        project_details TEXT,
        developer_payment REAL,
        deadline TEXT,
        status TEXT,
        assigned_to INTEGER,
        client INTEGER
    );
    CREATE TABLE IF NOT EXISTS completed_projects (
        developer_id INTEGER PRIMARY KEY,
        project_id TEXT,
        developer_payment REAL
    );
    COMMIT;
''')

conn.commit()

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
