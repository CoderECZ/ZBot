import discord
from discord.ext import commands

class Welcome(commands.Cog):
    '''Welcome command and functions.'''
    def __init__(self, bot):
        self.bot = bot
        self.welcome_channel_id = 1158811277813108817
    
    def get_welcome_channel(self):
        return self.bot.get_channel(self.welcome_channel_id)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = self.get_welcome_channel()

        if welcome_channel:
            embed = discord.Embed(
                title=f"Welcome to CoderZ, {member.name}!",
                description=f"If you are here regarding your order, please wait while the bot processes it.\n"
                            f"If you are here to speak with a member of our team, please join the waiting room.\n\n"
                            f"We hope you enjoy your stay! Make sure to follow the rules, {member.mention}!",
                color=0x00ff00  # You can customize the color
            )

            embed.set_thumbnail(url=member.avatar_url)
            embed.set_image(url='https://cdn.discordapp.com/attachments/1114686704658423848/1157276152642146365/Picsart_23-09-17_19-07-53-355-removebg-preview.png?ex=651d4ae7&is=651bf967&hm=bd25b56a7eebb99968650aaf2fe19bb0b204b29d5eed211e7766b65d198cd36c&')

            await welcome_channel.send(embed=embed)
        else:
            pass
