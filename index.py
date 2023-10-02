import discord, sqlite3, json, tqdm
from discord.ext import commands

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

from cogs.ticket_system import TicketSystem 
from cogs.management_system import ManagementPanel
from cogs.statuses import Statuses
from cogs.project_management import ProjectManagement
from cogs.utilities import Utilites
from cogs.system import System
from cogs.invoice import Invoice

ticket_system = TicketSystem(bot)
management_panel = ManagementPanel(bot)
statuses = Statuses(bot)
project_management = ProjectManagement(bot)
utilites = Utilites(bot)
system = System(bot)
invoice = Invoice(bot)

bot.add_cog(ticket_system/management_panel/statuses/project_management/utilites/system/invoice)

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
    global server  # Make server a global variable
    server_id = 1088951646886842498 # Replace with your server ID
    server = bot.get_guild(server_id)  # Retrieve the server here
    
    global schedule_message_id
    schedule_channel_id = 1154179596682543125  # Replace with the actual channel ID
    schedule_channel = bot.get_channel(schedule_channel_id)
    
    # Check if the schedule message exists
    if schedule_message_id:
        try:
            # Fetch the message using the stored message ID
            schedule_message = await schedule_channel.fetch_message(schedule_message_id)
            # Update the embed with the latest information
            updated_embed = statuses.create_schedule_embed() # Replace with your updated embed creation logic
            await schedule_message.edit(embed=updated_embed)
        except discord.NotFound:
            # The message doesn't exist; create a new one
            updated_embed = statuses.create_schedule_embed()  # Replace with your updated embed creation logic
            schedule_message = await schedule_channel.send(embed=updated_embed)
            schedule_message_id = schedule_message.id
    else:
        # Schedule message doesn't exist; create a new one
        updated_embed = statuses.create_schedule_embed()  # Replace with your updated embed creation logic
        schedule_message = await schedule_channel.send(embed=updated_embed)
        schedule_message_id = schedule_message.id

    # Start a background task to periodically update the embed
    statuses.update_schedule_embed.start()
    
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CoderZ code!"))
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    await bot.process_commands(message)

with open('config.json', 'r') as f:
    config = json.load(f)

bot.run(config['botkey'])