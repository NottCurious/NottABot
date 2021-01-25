# Importing Libraries
import discord
import os
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv

# Files
import return_wood_prices
import hypixel_stalking
import sbstalk
import numberformat
import keep_alive

keep_alive.keep_alive()

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")
BOTTOKEN = os.getenv("BOT_TOKEN")

# Setting Up Bot
client = commands.Bot(command_prefix = '=')

# Printing String When Bot Is Ready To Be Used
@client.event
async def on_ready():
  # await client.get_channel(791559545519734795).send('Bot has Been Updated to v1.2 (remade slayer functions, please check =helpme for new command)')
  # await client.get_channel(802841895536951306).send ('Bot has Been Updated to v1.2 (remade slayer functions, please check =helpme for new command)')
  # await client.get_channel(784965489687658530).send('Bot has Been Updated to v1.2 (remade slayer functions, please check =helpme for new command)')

  print('Logged in as {0.user}'.format(client))

@client.event
async def on_guild_join(ctx):
	await ctx.send('o/ I\'m Currently Developed and Maintained By NottCurious#4351')

@client.command()
async def helpme(ctx):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')

	if str(ctx.message.author) == 'NottCurious#4351':
		await ctx.send('Yes m\'lord Curious')

	if str(ctx.message.author) == 'RegrettingLifeChoices#4684':
		await ctx.send('#GoombaLivesMatter')

	print('Help Command Used')
	embedVar = discord.Embed(title='Temporary Help Page', description='', color=0x00ff00)
	embedVar.add_field(name='=wood', value='Displays Current Enchanted Wood Prices to Help You Choose Which To Farm!', inline=False)
	embedVar.add_field(name='=hystalk \{username\}', value='Displays Simple Information About a Player', inline=False)
	embedVar.add_field(name='=skills \{username\}', value='Displays Current Skill Level of a Player', inline=False)
	embedVar.add_field(name='=revenant \{username\}', value='Displays Zombie Slayer Details', inline=True)
	embedVar.add_field(name='=tarantula \{username\}', value='Displays Spider Slayer Details', inline=True)
	embedVar.add_field(name='=sven \{username\}', value='Displays Wolf Slayer Details', inline=True)
	embedVar.add_field(name='=bank \{username\}', value='Displays Current Bank and Purse Balance', inline=False)
	await ctx.send(embed=embedVar)
	# Wood, hystalk, skillstalk, dungeonstalk, alchemy level, 

@client.command()
async def wood(ctx):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')

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
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')


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
async def skills(ctx, username=''):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')


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

@client.command()
async def revenant(ctx, username=''):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')


	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = sbstalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	details = sbstalk.getZombieSlayerData(mcuuid)

	t1k = details[0]
	t2k = details[1]
	t3k = details[2]
	t4k = details[3]

	current_exp = details[4]
	current_level = details[5]

	money_spent = details[6]
	percentage_completion = str(details[7]) + f'%'

	t4r = details[8]
	req_exp = details[9]
	money_req = details[10]

	exptoup = sbstalk.getExpToUp(current_level)

	embedVar = discord.Embed(title='Revenant Slayer Details', description='', color=0x00ff00)

	# embedVar.add_field(name='**Tier Kills: **', value='Tier I Kills: %d\nTier II Kills: %d\nTier III Kills: %d\nTier IV Kills: %d' % (t1k, t2k, t3k, t4k), inline=False)
	# embedVar.add_field(name='**Current Exp and Level: **', value='Current Exp: %s\n Current Level: %d\n Percentage to Next Level: %s' % ("{:,}".format(current_exp), current_level, percentage_completion), inline=True)
	# embedVar.add_field(name='**Money Spent: **', value=money_spent, inline=True)
	# embedVar.add_field(name='**To Next Wolf Slayer Level: **', value='Exp Required: %s\n T4s Required: %d\n Money Required: %s\n' % ("{:,}".format(req_exp), t4r, money_req))
	embedVar.add_field(name='**Revenant Slayer**', value='```ini\n[ == Level %s == ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(numberformat.comma(current_level)), str(numberformat.comma(current_exp)), str(numberformat.comma(exptoup)), str(percentage_completion), str(t1k), str(t2k), str(t3k), str(t4k), str(money_spent), str(t4r), str(money_req)), inline=True)
	await ctx.send(embed=embedVar)

@client.command()
async def tarantula(ctx, username=''):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')


	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = sbstalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	details = sbstalk.getSpiderSlayerData(mcuuid)

	t1k = details[0]
	t2k = details[1]
	t3k = details[2]
	t4k = details[3]

	current_exp = details[4]
	current_level = details[5]

	money_spent = details[6]
	percentage_completion = str(details[7]) + f'%'

	t4r = details[8]
	req_exp = details[9]
	money_req = details[10]

	exptoup = sbstalk.getExpToUp(current_level)

	embedVar = discord.Embed(title='Tarantula Slayer Details', description='', color=0x00ff00)

	# embedVar.add_field(name='**Tier Kills: **', value='Tier I Kills: %d\nTier II Kills: %d\nTier III Kills: %d\nTier IV Kills: %d' % (t1k, t2k, t3k, t4k), inline=False)
	# embedVar.add_field(name='**Current Exp and Level: **', value='Current Exp: %s\n Current Level: %d\n Percentage to Next Level: %s' % ("{:,}".format(current_exp), current_level, percentage_completion), inline=True)
	# embedVar.add_field(name='**Money Spent: **', value=money_spent, inline=True)
	# embedVar.add_field(name='**To Next Wolf Slayer Level: **', value='Exp Required: %s\n T4s Required: %d\n Money Required: %s\n' % ("{:,}".format(req_exp), t4r, money_req))
	embedVar.add_field(name='**Tarantula Slayer**', value='```ini\n[ == Level %s == ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(numberformat.comma(current_level)), str(numberformat.comma(current_exp)), str(numberformat.comma(exptoup)), str(percentage_completion), str(t1k), str(t2k), str(t3k), str(t4k), str(money_spent), str(t4r), str(money_req)), inline=True)
	await ctx.send(embed=embedVar)


@client.command()
async def sven(ctx, username=''):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')


	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = sbstalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	details = sbstalk.getWolfSlayerData(mcuuid)

	t1k = details[0]
	t2k = details[1]
	t3k = details[2]
	t4k = details[3]

	current_exp = details[4]
	current_level = details[5]

	money_spent = details[6]
	percentage_completion = str(details[7]) + f'%'

	t4r = details[8]
	req_exp = details[9]
	money_req = details[10]

	exptoup = sbstalk.getExpToUp(current_level)

	embedVar = discord.Embed(title='Sven Slayer Details', description='', color=0x00ff00)

	# embedVar.add_field(name='**Tier Kills: **', value='Tier I Kills: %d\nTier II Kills: %d\nTier III Kills: %d\nTier IV Kills: %d' % (t1k, t2k, t3k, t4k), inline=False)
	# embedVar.add_field(name='**Current Exp and Level: **', value='Current Exp: %s\n Current Level: %d\n Percentage to Next Level: %s' % ("{:,}".format(current_exp), current_level, percentage_completion), inline=True)
	# embedVar.add_field(name='**Money Spent: **', value=money_spent, inline=True)
	# embedVar.add_field(name='**To Next Wolf Slayer Level: **', value='Exp Required: %s\n T4s Required: %d\n Money Required: %s\n' % ("{:,}".format(req_exp), t4r, money_req))
	embedVar.add_field(name='**Sven Slayer**', value='```ini\n[ == Level %s == ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(numberformat.comma(current_level)), str(numberformat.comma(current_exp)), str(numberformat.comma(exptoup)), str(percentage_completion), str(t1k), str(t2k), str(t3k), str(t4k), str(money_spent), str(t4r), str(money_req)), inline=True)
	await ctx.send(embed=embedVar)


@client.command()
async def bank(ctx, username=''):
	if str(ctx.message.author) == 'LokiLok#6861':
		await ctx.send('Please Wait While I Search Master Loki')


	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = sbstalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	bank_balance, purse_balance = sbstalk.getBankBalance(mcuuid)

	embedVar = discord.Embed(title='Bank Details', description='', color=0x00ff00)
	embedVar.add_field(name='Bank Balance: ', value='$%s' % ("{:,}".format(bank_balance)), inline=True)
	embedVar.add_field(name='Purse Balance: ', value='$%s' % ("{:,}".format(purse_balance)), inline=True)

	await ctx.send(embed=embedVar)

# Execute Commands
client.run(BOTTOKEN)
