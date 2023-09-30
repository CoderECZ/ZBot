import discord
from discord.ext import commands

class TicketSystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.LOG_CHANNEL_ID = 123456789012345678  # Replace with your log channel ID

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')

    @commands.command()
    async def openticket(self, ctx, assigned_user_id: int):
        assigned_user = self.bot.get_user(assigned_user_id)

        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="Tickets")
        if category is None:
            category = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            assigned_user: discord.PermissionOverwrite(read_messages=True),
        }

        ticket_channel = await category.create_text_channel(f"ticket-{ctx.author.name}", overwrites=overwrites)

        embed = discord.Embed(
            title="Ticket Information",
            description="Ticket has been opened.",
            color=0x00ff00
        )

        await ticket_channel.send(embed=embed)

        await assigned_user.send(f"You have been added to a new ticket: {ticket_channel.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.category and message.channel.category.name == "Tickets":
            self.log_message(message)
            await self.send_to_assigned_user(message)
            await self.send_to_log_channel(message)

        await self.bot.process_commands(message)

    async def send_to_assigned_user(self, message):
        assigned_user = None
        for overwrite in message.channel.overwrites:
            if overwrite[0].id != message.guild.id:
                assigned_user = message.guild.get_member(overwrite[0].id)
                break

        if assigned_user:
            await assigned_user.send(f"New message in your ticket ({message.channel.mention}): {message.content}")

    async def send_to_log_channel(self, message):
        log_channel = message.guild.get_channel(self.LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(f"{message.author.name}: {message.content}")

    def log_message(self, message):
        with open(f"{message.channel.name}_log.txt", "a", encoding="utf-8") as file:
            file.write(f"{message.author.name}: {message.content}\n")
