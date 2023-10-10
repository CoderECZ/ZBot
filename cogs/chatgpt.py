import discord, json
from discord.ext import commands
import openai

with open('config.json', 'r') as f:
    config = json.load(f)

openai.api_key = config['openaiapi']

class ChatGPT(commands.Cog):
    '''Chat GPT commands.'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ask')
    async def ask_question(self, ctx, *, question):
        # Call OpenAI API to get response
        response = self.ask_gpt(question)

        # Send the response to the Discord channel
        await ctx.send(f'**Question:** {question}\n**Answer:** {response}')

    def ask_gpt(self, question):
        # Make a call to the OpenAI API to get a response
        prompt = f'User: {question}\nChatGPT:'
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            temperature=0.7,
            max_tokens=150,
            n=1,
            stop=None,
        )

        # Extract and return the model's reply from the API response
        reply = response['choices'][0]['text'].strip()
        return reply
