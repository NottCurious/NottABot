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
import numberformat

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
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = sbstalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	names = ['**Combat**', '**Foraging**', '**Farming**', '**Enchanting**', '**Alchemy**', '**Mining**', '**Fishing**']
	levels, expremaining, exptoup = sbstalk.getSkills(mcuuid)
	print('\nReceived Skills')

	skill_avg = sbstalk.findSkillAverage(mcuuid)
	print('\nFound Skill Average')

	embedVar = discord.Embed(title='Skill Details', description='', color=0x00ff00) # Make this Look Better In the Future
	embedVar.add_field(name='**Skill Average**', value=skill_avg, inline=False)	
	print('Embed Created')

	for i in range(len(levels)):
		embedVar.add_field(name=names[i], value='Level: %d \n Progress Percent: %d' % (levels[i], round(expremaining[i]*100/exptoup[i], 2)) + f'%' + '\n %s / %s' % (numberformat.human_format(expremaining[i]), numberformat.human_format(exptoup[i])), inline=True)
	print('Embed Fields Added')

	await ctx.send(embed=embedVar)
	print('Embed Sent')
	print('\n')

# Execute Commands
client.run(BOTTOKEN)
