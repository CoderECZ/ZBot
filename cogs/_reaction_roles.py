import discord
from discord.ext import commands

from cogs.logging import Logging

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.server_id = 1088951646886842498 
        self.server = bot.get_guild(self.server_id)
        
        reactionRoles = {
            "<:Swift:1159231251748769943>": discord.utils.get(self.server.roles, name="Swift"),
            "<:PHP:1159231250201063454>": discord.utils.get(self.server.roles, name="PHP"),
            "<:Net:1159231247663513692>": discord.utils.get(self.server.roles, name=".NET"),
            "<:Golang:1159231246371651686>": discord.utils.get(self.server.roles, name="Golang"),
            "<:Java:1159231242768748587>": discord.utils.get(self.server.roles, name="Java"),
            "<:Clang:1159231240654819408>": discord.utils.get(self.server.roles, name="Clang"),
            "<:Blender:1159231237676863569>": discord.utils.get(self.server.roles, name="Blender"),
            "<:VisualStudio:1159231208916521000>": discord.utils.get(self.server.roles, name="Visual Studio"),
            "<:JavaScript:1159231203124183151>": discord.utils.get(self.server.roles, name="JavaScript"),
            "<:Python:1159231201765240892>": discord.utils.get(self.server.roles, name="Python"),
            "<:HTML:1159231198774702091>": discord.utils.get(self.server.roles, name="HTML"),
            "<:CPP:1159231197059227809>": discord.utils.get(self.server.roles, name="CPP"),
            "<:CS:1159231195712847962>": discord.utils.get(self.server.roles, name="CS"),
            "<:VSC:1159231193359863898>": discord.utils.get(self.server.roles, name="Visual Studio Code"),
            "<:CSS:1159231142633943203>": discord.utils.get(self.server.roles, name="CSS"),
            "<:Lua:1159231140377411624>": discord.utils.get(self.server.roles, name="Lua"),
            "<:SQL:1159231136392818718>": discord.utils.get(self.server.roles, name="SQL"),
            "<:GitHub:1159249963331637401>": discord.utils.get(self.server.roles, name="Git/GitHub"),
            }
        
        self.bot = bot
        self.reactions = reactionRoles
        self.reactionKeys = self.reactions.keys()
        
    @commands.command(name="admin_roles")
    @commands.has_permissions(manage_messages=True)
    async def admin_roles(self, ctx):
        embedLanguages = discord.Embed(
            title="Coding Roles",
            description="Please react for the roles you wish to obtain below.\n\n",
            colour=0x1e90ff
        )

        for key in self.reactionKeys:
            emoji = key
            nameKey = key.split(':')[1]

            # Use custom emoji representation in the name field
            embedLanguages.add_field(name=f"{emoji} - {nameKey}", value="")

        embedLanguages.set_footer(
            icon_url='https://cdn.discordapp.com/attachments/1114686704658423848/1157276152642146365/Picsart_23-09-17_19-07-53-355-removebg-preview.png?ex=651df3a7&is=651ca227&hm=ba913fbfa95aded5a1ef249cd7795d77e9f2087629b8dc9d3656736f065b6932&',
            text="CoderZ"
        )
        message = await ctx.send(embed=embedLanguages)

        for key in self.reactionKeys:
            try:
                await message.add_reaction(key)
            except discord.HTTPException as e:
                await ctx.send(f"Could not add reactions: {e}")

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction: discord.Reaction, user: discord.Member):
        if user.bot:  # Ignore reactions from bots
            return

        if str(reaction.emoji) in self.reactions:
            role = self.reactions[str(reaction.emoji)]

            try:
                if role in user.roles:
                    await user.remove_roles(role)
                    print(f"Removed role {role.name} from {user.display_name}")
                else:
                    await user.add_roles(role)
                    print(f"Added role {role.name} to {user.display_name}")
            except discord.HTTPException as e:
                print(f"Failed to manage roles: {e}")

    @commands.Cog.listener()
    async def on_reaction_remove(self, reaction: discord.Reaction, user: discord.Member):
        if user.bot:  # Ignore reactions from bots
            return

        if str(reaction.emoji) in self.reactions:
            role = self.reactions[str(reaction.emoji)]

            try:
                if role in user.roles:
                    await user.remove_roles(role)
                    print(f"Removed role {role.name} from {user.display_name}")
            except discord.HTTPException as e:
                print(f"Failed to manage roles: {e}")
