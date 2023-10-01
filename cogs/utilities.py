import discord, sqlite3
from discord.ext import commands

conn = sqlite3.connect("data/developers.db")
cursor = conn.cursor()

class Utilites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @classmethod
    def user_nickname(self, user_id: int, guild: discord.Guild):
        '''
        Get the nickname of a user based of their User ID.
        '''
        # Iterate through the members of the specified guild to find the user with the given ID
        for member in guild.members:
            if member.id == user_id:
                nickname = member.nick if member.nick else member.name
                return nickname
        # If the user is not found in the specified guild, return None or an appropriate message
        return None

    # Define a function to add certified roles to a developer
    # developer_id is the user's ID, and role_name is the name of the certified role
    @classmethod
    def add_certified_role(self, developer_id, role_name):
        '''
        Adds a certified role to a user based of their User ID (Developer ID) and the certification name (Discord Certification Role name.)
        '''
        cursor.execute('''
            INSERT INTO certified_roles (developer_id, role_name)
            VALUES (?, ?)
        ''', (developer_id, role_name))
        conn.commit()

    # Define a function to get the certified roles for a developer
    # developer_id is the user's ID for whom you want to retrieve certified roles
    @classmethod
    def get_certified_roles(self, developer_id):
        '''
        Gets all of the users certified roles from the database based of their User ID (Developer ID).
        '''
        cursor.execute('''
            SELECT role_name
            FROM certified_roles
            WHERE developer_id = ?
        ''', (developer_id,))
        return [row[0] for row in cursor.fetchall()]
    
    @classmethod
    def remove_certified_role(self, developer_id, role_name):
        '''
        Removes a certified role from a user based of their User ID (Developer ID) and the certification name (Discord Certification Role name.)
        '''
        developerRoles = self.get_certified_roles(developer_id=developer_id)
        # Check if the role_name exists in lowercase
        lowercase_role_name = role_name.lower()
        if lowercase_role_name in [cert.lower() for cert in developerRoles]:
            # Remove the role_name from the database
            cursor.execute('''
                DELETE FROM certified_roles
                WHERE developer_id = ? AND LOWER(role_name) = ?
            ''', (developer_id, lowercase_role_name))
            conn.commit()
    
    @classmethod
    async def rolesF(self):
        rF = [
            {
                "ranks": {
                    "Chief Executive Officer": lambda server: discord.utils.get(server.roles, name="Chief Executive Officer"),
                    "Chief Operations Officer": lambda server: discord.utils.get(server.roles, name="Chief Operations Officer"),
                    "Account Executive": lambda server: discord.utils.get(server.roles, name="Account Executive"),
                    "Developer": lambda server: discord.utils.get(server.roles, name="Developer"),
                    "Staff": lambda server: discord.utils.get(server.roles, name="Staff"),
                    "Sales Representative": lambda server: discord.utils.get(server.roles, name="Sales Representative"),
                },
            },
            {
                "certs": {
                    "JSON Creator": lambda server: discord.utils.get(server.roles, name="JSON Creator"),
                    "Server Configuration": lambda server: discord.utils.get(server.roles, name="Server Configuration"),
                    "Script Developer": lambda server: discord.utils.get(server.roles, name="Script Developer"),
                    "3D Modelling Engineer": lambda server: discord.utils.get(server.roles, name="3D Modelling Engineer"),
                    "Web Developer": lambda server: discord.utils.get(server.roles, name="Web Developer"),
                    "Bot Developer": lambda server: discord.utils.get(server.roles, name="Bot Developer"),
                    "Social Media Engineer": lambda server: discord.utils.get(server.roles, name="Social Media Engineer"),
                    "Map Developer": lambda server: discord.utils.get(server.roles, name="Map Developer"), 
                    "Mod Technician": lambda server: discord.utils.get(server.roles, name="Mod Technician"),
                    "Technical Administrator": lambda server: discord.utils.get(server.roles, name="Technical Administrator")
                },
            },
            {
                "statuses": {
                    "Available": lambda server: discord.utils.get(server.roles, name="Available"),
                    "Unavailable": lambda server: discord.utils.get(server.roles, name="Unavailable"),
                    "onBreak": lambda server: discord.utils.get(server.roles, name="On Break"),
                    "Busy": lambda server: discord.utils.get(server.roles, name="Busy"),
                },
            },
        ]
        
        return rF
