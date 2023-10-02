import discord, sqlite3, string
from discord.ext import commands

conn = sqlite3.connect("data/developers.db")
cursor = conn.cursor()

class Utilites(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    SERVICE_TYPES = {
        'a': 'Web Development',
        'b': 'Server Configuration',
        'c': 'Mod Configuration',
        'd': 'JSON',
        'e': 'Map Development',
        'f': '3D Modelling/Texturing',
        'g': 'Bot Development',
        'h': 'Scripting',
        'i': 'Catalog/Pre-made',
        'x': 'Other',
    }

    GAMES = {
        'a': 'DayZ',
        'b': 'Arma',
        'c': 'Discord',
        'x': 'Other',
    }
    
    
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
    
    async def rolesF(self, server):
        '''A list of all of the ranks, certifications and statuses within the server.'''
        rF = {
            "ranks": {
                "Chief Executive Officer": discord.utils.get(server.roles, name="Chief Executive Officer"),
                "Chief Operations Officer": discord.utils.get(server.roles, name="Chief Operations Officer"),
                "Account Executive": discord.utils.get(server.roles, name="Account Executive"),
                "Developer": discord.utils.get(server.roles, name="Developer"),
                "Staff": discord.utils.get(server.roles, name="Staff"),
                "Sales Representative": discord.utils.get(server.roles, name="Sales Representative"),
            },
            "certs": {
                "JSON Creator": discord.utils.get(server.roles, name="JSON Creator"),
                "Server Configuration": discord.utils.get(server.roles, name="Server Configuration"),
                "Script Developer": discord.utils.get(server.roles, name="Script Developer"),
                "3D Modelling Engineer": discord.utils.get(server.roles, name="3D Modelling Engineer"),
                "Web Developer": discord.utils.get(server.roles, name="Web Developer"),
                "Bot Developer": discord.utils.get(server.roles, name="Bot Developer"),
                "Social Media Engineer": discord.utils.get(server.roles, name="Social Media Engineer"),
                "Map Developer": discord.utils.get(server.roles, name="Map Developer"), 
                "Mod Technician": discord.utils.get(server.roles, name="Mod Technician"),
                "Technical Administrator": discord.utils.get(server.roles, name="Technical Administrator")
            },
            "statuses": {
                "Available": discord.utils.get(server.roles, name="Available"),
                "Unavailable": discord.utils.get(server.roles, name="Unavailable"),
                "onBreak": discord.utils.get(server.roles, name="On Break"),
                "Busy": discord.utils.get(server.roles, name="Busy"),
            },
        }

        return rF
    
    @classmethod
    def generate_project_number(self, base_number, index):
        '''Generates a project number with a alphabetical number for multi-project orders.'''
        alphabet = string.ascii_lowercase
        suffix = alphabet[index % len(alphabet)]
        return f"{base_number:04d}{suffix}"
    
    @classmethod
    def encode(self, service_type, discord_id, game, deadline, invoice_no):
        '''Encodes a reference number for use in an invoice/project.'''
        
        service_encode = self.SERVICE_TYPES.get(service_type)
        game_encode = self.GAMES.get(game[0])
        
        return f'{service_encode}{discord_id}{game_encode}{deadline}{invoice_no}'

    @classmethod
    def decode(self, reference_number):
        '''Decodes a reference number into a dictionary of values: Service Type, Discord ID, Game, Deadline and Invoice/Project Number.'''
        if len(reference_number) != 21:
            return None  # Invalid reference number length

        service_type = self.SERVICE_TYPES.get(reference_number[0])
        discord_id = reference_number[1:19]
        game = self.GAMES.get(reference_number[19])
        deadline = reference_number[20:28]
        invoice_no = reference_number[28:]

        if not service_type or not game:
            return None  # Invalid service type or game code

        return {
            'Service Type': service_type,
            'Discord ID': discord_id,
            'Game': game,
            'Deadline': deadline,
            'Invoice No': invoice_no,
        }
        
    @commands.command(name="ref")
    async def ref(self, ctx):
        '''Builds a reference number using Utilities.encode()'''
        def check(message):
            return message.author == ctx.author and isinstance(message.channel, discord.DMChannel)

        await ctx.author.send("What is the service type?\n\n> 1 | Web Development\n> 2 | Server Configuration\n> 3 | Mod Configuration\n> 4 | JSON\n> 5 | Map Development\n> 6 | 3D Modelling (Texturing, Rigging, Animations...)\n> 7 | Bot Development\n> 8 | Scripting\n> 9 | Catalog\n> 10 | Other")

        def validate_service_type(message):
            return check(message) and message.content.isdigit() and 1 <= int(message.content) <= 10

        t = await self.bot.wait_for("message", timeout=120, check=validate_service_type)

        await ctx.author.send("What is the user's Discord ID?\n[How to get a user's Discord ID](https://support.discord.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-)")

        def validate_user_id(message):
            return check(message) and message.content.isdigit()  # You can add more specific validation if needed

        u = await self.bot.wait_for("message", timeout=120, check=validate_user_id)

        await ctx.author.send("What game is it for?\n\n> 1 | DayZ\n> 2 | Arma\n> 3 | Discord\n> 4 | Other")

        def validate_game(message):
            return check(message) and message.content.isdigit() and 1 <= int(message.content) <= 4

        g = await self.bot.wait_for("message", timeout=120, check=validate_game)

        await ctx.author.send("What is the deadline for the project?\n\nIn this format specifically: DDMMYYYY")

        def validate_deadline(message):
            return check(message) and len(message.content) == 8 and message.content.isdigit()

        d = await self.bot.wait_for("message", timeout=120, check=validate_deadline)

        await ctx.author.send("What is the invoice number?")

        def validate_invoice_number(message):
            return check(message) and message.content.isdigit()  # You can add more specific validation if needed

        i = await self.bot.wait_for("message", timeout=120, check=validate_invoice_number)
        
        service_type = t.content
        user_id = u.content
        game = g.content
        deadline = d.content
        invoice_number = i.content

        reference_number = self.encode(service_type, user_id, game, deadline, invoice_number)
        await ctx.author.send(f"Reference Number: {reference_number}")
