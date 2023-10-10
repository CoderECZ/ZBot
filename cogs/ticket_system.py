import discord, sqlite3
from discord.ext import commands

class TicketSystem(commands.Cog):
    '''Commands for managing project tickets.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f'Logged in as {self.bot.user.name}')
    
    async def add_developer(self, ctx, developer_id: int):
        '''Adds a developer to a project ticket.'''
        guild = ctx.guild
        assigned_user_id = None

        # Get the assigned user ID from channel overwrites
        for overwrite in ctx.channel.overwrites:
            if overwrite[0].id != ctx.guild.id:
                assigned_user_id = overwrite[0].id
                break

        if assigned_user_id:
            assigned_user = guild.get_member(assigned_user_id)
            developer = guild.get_member(developer_id)

            if developer and assigned_user:
                # Update channel overwrites to allow only the assigned user and the added developer to read messages
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(read_messages=False),
                    guild.me: discord.PermissionOverwrite(read_messages=True),
                    assigned_user: discord.PermissionOverwrite(read_messages=True),
                    developer: discord.PermissionOverwrite(read_messages=True),
                }

                await ctx.channel.edit(overwrites=overwrites)

                # Send an embed indicating the developer has been added
                embed = discord.Embed(
                    title="Developer Assigned!",
                    description=f"{developer.mention} has been added to your ticket!\n\n"
                                f"They will help get your project complete in no time!\n"
                                f"Please let them know any information they request regarding your project, this helps them get it done super quick!",
                    color=0x00ff00
                )
                await ctx.channel.send(embed=embed)

            else:
                await ctx.send("Invalid developer or assigned user.")
        else:
            await ctx.send("Assigned user not found.")
    
    @classmethod
    @commands.command(name="close_ticket")
    async def close_ticket(self, ctx, channel_name: str = None):
        '''Closes the current project ticket.'''
        if channel_name == None:
            if ctx.channel.category and ctx.channel.category.name.lower() == "project tickets":
                await ctx.channel.delete()
                await ctx.send("Ticket closed successfully.")
        elif channel_name is not None:
            # Try to get the channel by name
            channel_to_close = discord.utils.get(ctx.guild.channels, name=channel_name)
            
            if channel_to_close and channel_to_close.category.name.lower() == "project tickets":
                await channel_to_close.delete()
                await ctx.send(f"Ticket '{channel_name}' closed successfully.")
            else:
                await ctx.send(f"Channel '{channel_name}' not found or not in 'Project Tickets' category.")
        else:
            await ctx.send("This command can only be used in a ticket channel.")

    async def create_ticket(self, ctx, pNo, pDesc, pDeadline, pClient: int):
        '''Creates a ticket for projects when they have been initiated.'''
        assigned_user = self.bot.get_user(pClient)

        guild = ctx.guild
        category = discord.utils.get(guild.categories, name="project tickets")
        if category is None:
            category = await guild.create_category("project tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            ctx.author: discord.PermissionOverwrite(read_messages=True),
            assigned_user: discord.PermissionOverwrite(read_messages=True),
        }

        ticket_channel = await category.create_text_channel(f"ticket-{pNo}", overwrites=overwrites)

        embed = discord.Embed(
            title=f"Project {pNo}",
            description=f"This is the beginning of your project with CoderZ!\n"
                        f"Please send all information regarding your project here!\n"
                        f"Our VCs are also open for project discussion!\n\n"
                        f"**Project Description**: {pDesc}"
                        f"**Project Deadline:** {pDeadline}",
            color=0x00ff00
        )

        await ticket_channel.send(embed=embed)

        await assigned_user.send(f"You have been added to a new ticket: {ticket_channel.mention}")

    @commands.Cog.listener()
    async def on_message(self, message):
        if isinstance(message.channel, discord.DMChannel):
            pass
        elif message.channel.category and message.channel.category.name.lower() == "project tickets":
            self.log_message(message)
        else:
            pass

    def log_message(self, message):
        with open(f"tickets/{message.channel.name}_log.txt", "a", encoding="utf-8") as file:
            file.write(f"{message.author.name}: {message.content}\n")