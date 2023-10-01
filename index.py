import discord, sqlite3
from discord.ext import commands

from cogs.ticket_system import TicketSystem 
from cogs.management_system import ManagementPanel
from cogs.statuses import Statuses
from cogs.project_management import ProjectManagement
from cogs.utilities import Utilites
from cogs.system import System
from cogs.invoice import Invoice

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)
conn = sqlite3.connect("data/developers.db")
cursor = conn.cursor()

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
            updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
            await schedule_message.edit(embed=updated_embed)
        except discord.NotFound:
            # The message doesn't exist; create a new one
            updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
            schedule_message = await schedule_channel.send(embed=updated_embed)
            schedule_message_id = schedule_message.id
    else:
        # Schedule message doesn't exist; create a new one
        updated_embed = create_schedule_embed()  # Replace with your updated embed creation logic
        schedule_message = await schedule_channel.send(embed=updated_embed)
        schedule_message_id = schedule_message.id

    # Start a background task to periodically update the embed
    update_schedule_embed.start()
    
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="CoderZ code!"))
    print(f'Logged in as {bot.user.name}')