import discord
from discord.ext import commands
import subprocess as sp
import time

class System(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(name="restart", hidden=True)  # Hidden to prevent users from accidentally triggering it
    @commands.is_owner()  # Only allow the bot owner to use this command
    async def restart(self, bot, ctx):
        await ctx.send("Restarting...")  # Send a message to indicate the restart

        # Change the bot's status to "Restarting"
        await bot.change_presence(status=discord.Status.dnd, activity=discord.Game("Restarting..."))

        await bot.close()  # Gracefully close the bot
        
        time.sleep(10) # Time for commands to stop

        # Use sys.executable to restart the bot using the same Python executable
        com = ["python3", "index.py"]
        sp.run(com)