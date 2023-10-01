import discord, sqlite3
from discord.ext import commands

conn = sqlite3.connect("data/developers.db")
cursor = conn.cursor()

class Utilites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    def user_nickname(self, user_id: int, guild: discord.Guild):
        # Iterate through the members of the specified guild to find the user with the given ID
        for member in guild.members:
            if member.id == user_id:
                nickname = member.nick if member.nick else member.name
                return nickname
        # If the user is not found in the specified guild, return None or an appropriate message
        return None

    # Define a function to add certified roles to a developer
    # developer_id is the user's ID, and role_name is the name of the certified role
    def add_certified_role(self, developer_id, role_name):
        cursor.execute('''
            INSERT INTO certified_roles (developer_id, role_name)
            VALUES (?, ?)
        ''', (developer_id, role_name))
        conn.commit()

    # Define a function to get the certified roles for a developer
    # developer_id is the user's ID for whom you want to retrieve certified roles
    def get_certified_roles(self, developer_id):
        cursor.execute('''
            SELECT role_name
            FROM certified_roles
            WHERE developer_id = ?
        ''', (developer_id,))
        return [row[0] for row in cursor.fetchall()]

    def remove_certified_role(self, developer_id, role_name):
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