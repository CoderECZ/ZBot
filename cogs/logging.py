import discord
from discord.ext import commands
import logging
from datetime import datetime

class Logging(commands.Cog):
    '''Logging commands and error detection commands.'''
    def __init__(self, bot):
        self.bot = bot
        self.setup_logging()

    def setup_logging(self):
        # Create a logging object
        self.logger = logging.getLogger('command_logger')
        self.logger.setLevel(logging.INFO)

        # Create a file handler and set the formatter
        log_file = '/home/breath/repos/ZBot/logs/command_logs.log'
        file_handler = logging.FileHandler(log_file)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        self.logger.addHandler(file_handler)
        
    @commands.command(name="get_logs", hidden=True)
    async def get_logs(self, ctx):
        """
        Get the logs from the command logger.
        """
        with open('/home/breath/repos/ZBot/logs/command_logs.log', 'r') as f:
            await ctx.send(f"```\n{f.read()}\n```")

    async def log_command(self, ctx, error=None):
        """
        Log information about a command.
        """
        command_name = ctx.command.name
        author_name = ctx.author.name
        guild_name = ctx.guild.name if ctx.guild else "Direct Message"
        channel_name = ctx.channel.name if ctx.guild else "Direct Message"
        timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')

        log_message = f"{timestamp} - Command '{command_name}' invoked by {author_name} in {guild_name}#{channel_name}"

        if error:
            log_message += f" - Error: {error}"

        # Log to the file
        self.logger.info(log_message)

    @commands.Cog.listener()
    async def on_command(self, ctx):
        """
        Event triggered whenever a command is invoked.
        """
        await self.log_command(ctx)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """
        Event triggered when a command encounters an error.
        """
        await self.log_command(ctx, error)
