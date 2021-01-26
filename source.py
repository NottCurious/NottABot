# Importing Libraries
import discord
import os
from discord.ext import commands
from pathlib import Path
from dotenv import load_dotenv

# Files
import zReturnWoodPrices
import zHypixelStalking
import zSBStalk
import zSBDetails
import zNumberFormat
import zSlayerDetails
import zAllSBStats
import zMissingTalismans
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
	  # # Loki Server - General Chat
  	# await client.get_channel(791559545519734795).send('Bot has Been Updated to v1.4 (Added 3 New Functions and Multiple Changes Improving Speed)')
  	
  	# # Private Server
  	# await client.get_channel(802841895536951306).send ('Bot has Been Updated to v1.4 (Added 3 New Functions and Multiple Changes Improving Speed)')
  	
  	# # Loki Server - Bot Chat
  	# await client.get_channel(784965489687658530).send('Bot has Been Updated to v1.4 (Added 3 New Functions and Multiple Changes Improving Speed)')

  	print('Logged in as {0.user}'.format(client))

@client.command()
async def helpme(ctx):
	print('Help Command Used By %s' % (ctx.author))
	embedVar = discord.Embed(title='Temporary Help Page', description='', color=0x00ff00)
	embedVar.add_field(name='=wood', value='Displays Current Enchanted Wood Prices to Help You Choose Which To Farm!', inline=False)
	embedVar.add_field(name='=hystalk \{username\}', value='Displays Simple Information About a Player', inline=False)
	embedVar.add_field(name='=skills \{username\}', value='Displays Current Skill Level of a Player', inline=False)
	embedVar.add_field(name='=revenant \{username\}', value='Displays Zombie Slayer Details', inline=True)
	embedVar.add_field(name='=tarantula \{username\}', value='Displays Spider Slayer Details', inline=True)
	embedVar.add_field(name='=sven \{username\}', value='Displays Wolf Slayer Details', inline=True)
	embedVar.add_field(name='=slayers \{username\}', value='Displays All Slayer Details of the Given Username', inline=False)
	embedVar.add_field(name='=bank \{username\}', value='Displays Current Bank and Purse Balance', inline=False)
	embedVar.add_field(name='=armor \{username\}', value='Displays Current Armor for a Person', inline=True)
	embedVar.add_field(name='=allStats \{username\}', value='Displays SB Stats of A Person', inline=True)
	embedVar.add_field(name='=mt \{username\}', value='Displays Missing Talismans of A Person', inline=False)
	await ctx.send(embed=embedVar)
	print('Help Embed Sent')
	# Wood, hystalk, skillstalk, dungeonstalk, alchemy level, 

@client.command()
async def wood(ctx):
	print("%s requests Wood Prices" % (ctx.author))
	prices = []
	prices = zReturnWoodPrices.get_wood_prices()

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
	details = zHypixelStalking.stalkPerson(username)

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
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSBStalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	names = ['**Combat**', '**Foraging**', '**Farming**', '**Enchanting**', '**Alchemy**', '**Mining**', '**Fishing**']
	levels, expremaining, exptoup = zSBStalk.getSkills(mcuuid)
	print('\nReceived Skills')

	skill_avg = zSBStalk.findSkillAverage(mcuuid)
	print('\nFound Skill Average')

	embedVar = discord.Embed(title='Skill Details', description='', color=0x00ff00) # Make this Look Better In the Future
	embedVar.add_field(name='**Skill Average**', value=skill_avg, inline=False)	
	print('Embed Created')

	for i in range(len(levels)):
		embedVar.add_field(name=names[i], value='Level: %d \n Progress Percent: %d' % (levels[i], round(expremaining[i]*100/exptoup[i], 2)) + f'%' + '\n %s / %s' % (zNumberFormat.human_format(expremaining[i]), zNumberFormat.human_format(exptoup[i])), inline=True)
	print('Embed Fields Added')

	await ctx.send(embed=embedVar)
	print('Embed Sent')
	print('\n')

@client.command()
async def revenant(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSlayerDetails.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	details = zSlayerDetails.getZombieSlayerData(mcuuid)

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

	exptoup = zSlayerDetails.getExpToUp(current_level)

	embedVar = discord.Embed(title='Revenant Slayer Details', description='', color=0x00ff00)

	# embedVar.add_field(name='**Tier Kills: **', value='Tier I Kills: %d\nTier II Kills: %d\nTier III Kills: %d\nTier IV Kills: %d' % (t1k, t2k, t3k, t4k), inline=False)
	# embedVar.add_field(name='**Current Exp and Level: **', value='Current Exp: %s\n Current Level: %d\n Percentage to Next Level: %s' % ("{:,}".format(current_exp), current_level, percentage_completion), inline=True)
	# embedVar.add_field(name='**Money Spent: **', value=money_spent, inline=True)
	# embedVar.add_field(name='**To Next Wolf Slayer Level: **', value='Exp Required: %s\n T4s Required: %d\n Money Required: %s\n' % ("{:,}".format(req_exp), t4r, money_req))
	embedVar.add_field(name='**Revenant Slayer**', value='```ini\n[ == Level %s == ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(zNumberFormat.comma(current_level)), str(zNumberFormat.comma(current_exp)), str(zNumberFormat.comma(exptoup)), str(percentage_completion), str(t1k), str(t2k), str(t3k), str(t4k), str(money_spent), str(t4r), str(money_req)), inline=True)
	await ctx.send(embed=embedVar)

@client.command()
async def tarantula(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSlayerDetails.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	details = zSlayerDetails.getSpiderSlayerData(mcuuid)

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

	exptoup = zSlayerDetails.getExpToUp(current_level)

	embedVar = discord.Embed(title='Tarantula Slayer Details', description='', color=0x00ff00)

	# embedVar.add_field(name='**Tier Kills: **', value='Tier I Kills: %d\nTier II Kills: %d\nTier III Kills: %d\nTier IV Kills: %d' % (t1k, t2k, t3k, t4k), inline=False)
	# embedVar.add_field(name='**Current Exp and Level: **', value='Current Exp: %s\n Current Level: %d\n Percentage to Next Level: %s' % ("{:,}".format(current_exp), current_level, percentage_completion), inline=True)
	# embedVar.add_field(name='**Money Spent: **', value=money_spent, inline=True)
	# embedVar.add_field(name='**To Next Wolf Slayer Level: **', value='Exp Required: %s\n T4s Required: %d\n Money Required: %s\n' % ("{:,}".format(req_exp), t4r, money_req))
	embedVar.add_field(name='**Tarantula Slayer**', value='```ini\n[ == Level %s == ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(zNumberFormat.comma(current_level)), str(zNumberFormat.comma(current_exp)), str(zNumberFormat.comma(exptoup)), str(percentage_completion), str(t1k), str(t2k), str(t3k), str(t4k), str(money_spent), str(t4r), str(money_req)), inline=True)
	await ctx.send(embed=embedVar)

@client.command()
async def sven(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSlayerDetails.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	details = zSlayerDetails.getWolfSlayerData(mcuuid)

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

	exptoup = zSlayerDetails.getExpToUp(current_level)

	embedVar = discord.Embed(title='Sven Slayer Details', description='', color=0x00ff00)

	embedVar.add_field(name='**Sven Slayer**', value='```ini\n[ == Level %s == ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(zNumberFormat.comma(current_level)), str(zNumberFormat.comma(current_exp)), str(zNumberFormat.comma(exptoup)), str(percentage_completion), str(t1k), str(t2k), str(t3k), str(t4k), str(money_spent), str(t4r), str(money_req)), inline=True)
	await ctx.send(embed=embedVar)

@client.command()
async def slayers(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSlayerDetails.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	zdetails = zSlayerDetails.getZombieSlayerData(mcuuid)
	tdetails = zSlayerDetails.getSpiderSlayerData(mcuuid)
	wdetails = zSlayerDetails.getWolfSlayerData(mcuuid)

	zt1k = zdetails[0]
	zt2k = zdetails[1]
	zt3k = zdetails[2]
	zt4k = zdetails[3]
	zcurrent_exp = zdetails[4]
	zcurrent_level = zdetails[5]
	zmoney_spent = zdetails[6]
	zpercentage_completion = str(zdetails[7]) + f'%'
	zt4r = zdetails[8]
	zreq_exp = zdetails[9]
	zmoney_req = zdetails[10]

	tt1k = tdetails[0]
	tt2k = tdetails[1]
	tt3k = tdetails[2]
	tt4k = tdetails[3]
	tcurrent_exp = tdetails[4]
	tcurrent_level = tdetails[5]
	tmoney_spent = tdetails[6]
	tpercentage_completion = str(tdetails[7]) + f'%'
	tt4r = tdetails[8]
	treq_exp = tdetails[9]
	tmoney_req = tdetails[10]

	wt1k = wdetails[0]
	wt2k = wdetails[1]
	wt3k = wdetails[2]
	wt4k = wdetails[3]
	wcurrent_exp = wdetails[4]
	wcurrent_level = wdetails[5]
	wmoney_spent = wdetails[6]
	wpercentage_completion = str(wdetails[7]) + f'%'
	wt4r = wdetails[8]
	wreq_exp = wdetails[9]
	wmoney_req = wdetails[10]

	zexptoup = zSBStalk.getExpToUp(zcurrent_level)
	texptoup = zSBStalk.getExpToUp(tcurrent_level)
	wexptoup = zSBStalk.getExpToUp(wcurrent_level)


	embedVar = discord.Embed(title='Slayer Details', description='', color=0x00ff00)

	embedVar.add_field(name='**Revenant Slayer**', value='```ini\n[ === Level %s === ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```\n' % (str(zNumberFormat.comma(zcurrent_level)), str(zNumberFormat.comma(zcurrent_exp)), str(zNumberFormat.comma(zexptoup)), str(zpercentage_completion), str(zt1k), str(zt2k), str(zt3k), str(zt4k), str(zNumberFormat.comma(zmoney_spent)), str(zt4r), str(zmoney_req)), inline=False)
	embedVar.add_field(name='**Tarantula Slayer**', value='```ini\n[ === Level %s === ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```\n' % (str(zNumberFormat.comma(tcurrent_level)), str(zNumberFormat.comma(tcurrent_exp)), str(zNumberFormat.comma(texptoup)), str(tpercentage_completion), str(tt1k), str(tt2k), str(tt3k), str(tt4k), str(zNumberFormat.comma(tmoney_spent)), str(tt4r), str(tmoney_req)), inline=False)
	embedVar.add_field(name='**Sven Slayer**', value='```ini\n[ === Level %s === ]\n%s / %s\nCompleted Percentage: %s\n\n[ Tier Kills ]\nTier I    : %s\nTier II   : %s\nTier III  : %s\nTier IV   : %s\n\nTotal Money Spent : %s\n\n[ Next Tier ]\nTier IVs Required : %s\nMoney Required : %s\n```' % (str(zNumberFormat.comma(wcurrent_level)), str(zNumberFormat.comma(wcurrent_exp)), str(zNumberFormat.comma(wexptoup)), str(wpercentage_completion), str(wt1k), str(wt2k), str(wt3k), str(wt4k), str(zNumberFormat.comma(wmoney_spent)), str(wt4r), str(wmoney_req)), inline=False)

	total_money_spent = zmoney_spent + tmoney_spent + wmoney_spent

	embedVar.add_field(name='**Total Money Spent**', value='```%s```' % (str(zNumberFormat.comma(total_money_spent))))

	await ctx.send(embed=embedVar)

@client.command()
async def bank(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSBStalk.getUUID(username)

	if mcuuid == 'no':
		print('Exiting Function, Player Doesn\'t Exist')
		await ctx.send('Enter a Valid Username and Try Again...')
		return

	bank_balance, purse_balance = zSBStalk.getBankBalance(mcuuid)

	if bank_balance == 'no':
		await ctx.send('Bank API is Switched Off for this Player')
		return

	embedVar = discord.Embed(title='Bank Details', description='', color=0x00ff00)
	embedVar.add_field(name='Bank Balance: ', value='$%s' % ("{:,}".format(bank_balance)), inline=True)
	embedVar.add_field(name='Purse Balance: ', value='$%s' % ("{:,}".format(purse_balance)), inline=True)

	await ctx.send(embed=embedVar)

@client.command()
async def profiles(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSBStalk.getUUID(username)

	profs = zSBStalk.getProfileCuteNames(mcuuid)

	embedVar = discord.Embed(title='Profiles', description='', color=0x00ff00)

	for i in range(len(profs)):
		embedVar.add_field(name='Profile %d' % (i + 1), value=profs[i], inline=False)

	await ctx.send(embed=embedVar)

@client.command()
async def armor(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSBStalk.getUUID(username)

	if mcuuid == 'no':
		await ctx.send('No Person Exists With That Username')
		return

	current_armor = zSBDetails.getCurrentArmor(username)

	embedVar = discord.Embed(title='Current Armor', description='', color=0x00ff00)

	boots = current_armor[0]
	leggings = current_armor[1]
	chestplate = current_armor[2]
	helmet = current_armor[3]

	embedVar.add_field(name='**Current Armor: **', value='**Helmet: **%s\n**Chestplate: **%s\n**Leggings: **%s\n**Boots: **%s' % (helmet, chestplate, leggings, boots), inline=False)

	await ctx.send(embed=embedVar)

@client.command()
async def allStats(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSBStalk.getUUID(username)

	if mcuuid == 'no':
		await ctx.send('No Person Exists With That Username')
		return


	stats = zAllSBStats.maincommand(username)

	# [health, defence, effective_health, strength, speed, intelligence, sea_creature_chance, magic_find, pet_luck, ferocity, ability_damage, mining_speed, mining_fortune, farming_fortune, foraging_fortune]
	health = stats[0]
	defence = stats[1]
	effective_health = stats[2]
	strength = stats[3]
	speed = stats[4]
	intelligence = stats[5]
	sea_creature_chance = stats[6]
	magic_find = stats[7]
	pet_luck = stats[8]
	ferocity = stats[9]
	ability_damage = stats[10]
	mining_speed = stats[11]
	mining_fortune = stats[12]
	farming_fortune = stats[13]
	foraging_fortune = stats[14]

	collected = stats[15]
	completed = stats[16]
	percentage = stats[17]

	embedVar = discord.Embed(title='Stats', description='', color=0x00ff00)

	embedVar.add_field(name=':shield: **Main Stats**', value='```\nHealth: %s\nDefence: %s\nEffective Health: %s\nStrength: %s\nSpeed: %s\nIntelligence: %s\nSea Creature Chance: %s\nMagic Find: %s\nPet Luck: %s\nFerocity: %s\nAbility Damage: %s\nMining Speed: %s\nMining Fortune: %s\nFarming Fortune: %s\nForaging Fortune: %s\n```' % (health, defence, effective_health, strength, speed, intelligence, sea_creature_chance, magic_find, pet_luck, ferocity, ability_damage, mining_speed, mining_fortune, farming_fortune, foraging_fortune), inline=False)
	embedVar.add_field(name=':crossed_swords: **Fairy Souls**', value='```\nCollected: %s\nTotal: %s\nProgress: %s\n```' % (collected, completed, percentage), inline=False)

	await ctx.send(embed=embedVar)

@client.command()
async def mt(ctx, username=''):
	if username == '':
		print('Exiting Function, Invalid Username')
		await ctx.send('Enter a Username and Try Again...')
		return

	mcuuid = zSBStalk.getUUID(username)

	if mcuuid == 'no':
		await ctx.send('No Person Exists With That Username')
		return

	mtali = zMissingTalismans.getMissingTalismans(username)

	embedVar = discord.Embed(title='Missing Talismans', description='', color=0x00ff00)

	mtalis = ''

	for i in range(len(mtali)):
		mtalis = mtalis + mtali[i] + '\n'

	embedVar.add_field(name='**Missing Talismans**', value=mtalis, inline=False)
	
	await ctx.send(embed=embedVar)

@client.command()
async def explain(ctx):
	if str(ctx.author) != 'NottCurious#4351':
		return

	await ctx.send('Top 10 Mysteries Science Still Can\t Answer')
	await ctx.send('1. Is Expired Quitting Skyblock?')
	await ctx.send('2. Is Expired a Professional TF2 Player?')
	await ctx.send('3. What the fuck is Market Gardening?')

# Execute Commands
client.run(BOTTOKEN)
