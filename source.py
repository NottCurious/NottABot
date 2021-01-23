# Importing Libraries
import discord
import requests
import os
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv
import return_wood_prices
import hypixel_stalking
import sbstalk

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")
BOTTOKEN = os.getenv("BOT_TOKEN")

# Setting Up Bot
client = commands.Bot(command_prefix = '>>')

# Printing String When Bot Is Ready To Be Used
@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(ctx):
	await ctx.send('o/ I\'m Currently Developed and Maintained By NottCurious#4351')

@client.command()
async def wood(ctx):
	print("%s requests Wood Prices" % (ctx.author))
	prices = []
	prices = return_wood_prices.get_wood_prices()
	
	oak = prices[0]
	birch = prices[1]
	spruce = prices[2]
	jungle = prices[3]
	dark_oak = prices[4]
	acacia = prices[5]

	embedVar = discord.Embed(title="Wood Prices", description="Current Enchanted Wood Prices In Skyblock To Help You Choose Which One To Farm!",color=0x00ff00)
	embedVar.set_thumbnail(url = 'https://imgur.com/a/YfMufUJ')
	embedVar.add_field(name="E Oak: ", value=oak, inline=True)
	embedVar.add_field(name="E Birch: ", value=birch, inline=True)
	embedVar.add_field(name="E Spruce: ", value=spruce, inline=True)
	embedVar.add_field(name="E Dark Oak: ", value=dark_oak, inline=True)
	embedVar.add_field(name="E Acacia: ", value=acacia, inline=True)
	embedVar.add_field(name="E Jungle: ", value=jungle, inline=True)
	print("Embed Created...")

	await ctx.send(embed=embedVar)
	print("Embed Sent...")
	print("Exiting Function.\n")

@client.command()
async def hystalk(ctx, username=''):
	if username == '':
		await ctx.send('Enter a Username and Try Again')
		return

	# await ctx.send('Stalking Player.')

	print('%s asks to stalk %s' % (ctx.author, username))
	details = hypixel_stalking.stalkPerson(username)

	if details[0] == 'no':
		await ctx.send('Player Doesn\'t Exist')
		return

	# details = [username, p_rank, p_status, p_guild, p_karma]
	username = details[0]
	p_rank = details[1]
	p_status = details[2]
	p_guild = details[3]
	p_karma = details[4]

	print('Creating Embed')
	embedVar = discord.Embed(title='%s\'s Player Details' % (username), description='', color=0x00ffff)
	embedVar.add_field(name='Username: ', value=username, inline=False)
	embedVar.add_field(name='Rank: ', value=p_rank, inline=True)
	embedVar.add_field(name='Guild: ', value=p_guild, inline=True)
	embedVar.add_field(name='Karma: ', value=p_karma, inline=True)
	embedVar.add_field(name='Current Status: ', value=p_status, inline=False)
	print('Embed Created')

	print('Sending Embed\n')
	await ctx.send(embed=embedVar)

@client.command()
async def skillstalk(ctx, username=''):	
	if username == '':
		await ctx.send('Enter a Username and Try Again')
		return

	# await ctx.send('Stalking Player.')

	print('%s asks to stalk skills of %s' % (ctx.author, username))
	# details = hypixel_stalking.stalkPerson(username)

	uuid = sbstalk.getUUID(username)

	if uuid == 'no':
		await ctx.send('Player Doesn\'t Exist')
		return

	skills = sbstalk.getSkills(uuid)

	combat = skills[0]
	foraging = skills[1]
	farming = skills[2]
	enchanting = skills[3]
	alchemy = skills[4]
	mining = skills[5]
	fishing = skills[6]

	embedVar = discord.Embed(title='Skills of %s' % (username), description='', color=0x00ff00)
	embedVar.add_field(name='Combat', value=combat, inline=False)
	embedVar.add_field(name='Foraging', value=foraging, inline=False)
	embedVar.add_field(name='Farming', value=farming, inline=False)
	embedVar.add_field(name='Enchanting', value=enchanting, inline=False)
	embedVar.add_field(name='Alchemy', value=alchemy, inline=False)
	embedVar.add_field(name='Mining', value=mining, inline=False)
	embedVar.add_field(name='Fishing', value=fishing, inline=False)

	await ctx.send(embed=embedVar)

# Execute Commands
client.run(BOTTOKEN)
