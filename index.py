import discord
from discord.ext import commands
import sqlite3
import json

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

from cogs.ticket_system import TicketSystem
from cogs.management_system import ManagementPanel
from cogs.statuses import Statuses
from cogs.project_management import ProjectManagement
from cogs.utilities import Utilites
from cogs.system import System
from cogs.invoice import Invoice
from cogs.logging import Logging

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
async def setup():
    ticket_system = TicketSystem(bot)
    management_panel = ManagementPanel(bot)
    statuses = Statuses(bot)
    project_management = ProjectManagement(bot)
    utilites = Utilites(bot)
    system = System(bot)
    invoice = Invoice(bot)
    logging = Logging(bot)

    await bot.add_cog(ticket_system)
    await bot.add_cog(management_panel)
    await bot.add_cog(statuses)
    await bot.add_cog(project_management)
    await bot.add_cog(utilites)
    await bot.add_cog(system)
    await bot.add_cog(invoice)
    await bot.add_cog(logging)

    statuses.update_schedule_embed.start()

    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CoderZ code!"))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

with open('config.json', 'r') as f:
    config = json.load(f)

bot.run(config['botkey'])
