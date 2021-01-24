# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv
import numberformat

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

# username = 'NottCurious'

# Getting UUID Using Mojang API
def getUUID(username):
	print("sbstalk - getUUID: Receiving Mojang Player Data")
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
	
		uuid = playerdata_mojang["id"]
		print("sbstalk - getUUID: UUID Received")

		return uuid
	except:
		return 'no'

def getProfiles(uuid):
	profs = []
	playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()
	print('sbstalk - getProfiles: API Receieved')
	for i in playerdata['player']['stats']['SkyBlock']['profiles']:
		profs.append(i)

	print('sbstalk - getProfiles: Returning Profiles')
	return profs

def getLatestProfile(uuid):
	# uuid = getUUID(username)

	playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()
	print('sbstalk - getLatestProfile: Received Data')

	j = 1
	latest_profile = []

	for i in playerdata['player']['stats']['SkyBlock']['profiles']:
		if j == 1:
			latest_profile = playerdata['player']['stats']['SkyBlock']['profiles'][i]['cute_name']
			latest_profile_id = playerdata['player']['stats']['SkyBlock']['profiles'][i]['profile_id']
			j += 1
	
	print('sbstalk - getLatestProfile: Returning Latest Profile Name and ID')
	return latest_profile, latest_profile_id


def getBankBalance(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()

	print('sbstalk - getBankBalance: Received SBData')

	bank_money = sbdata['profile']['banking']['balance']
	purse = sbdata['profile']['members'][uuid]['coin_purse']

	print('sbstalk - getBankBalance: Returning Data')
	return round(bank_money, 2), round(purse, 2)

def formatExp(exp):
	exptoup = [0, 50, 125, 200, 300, 500, 750, 1000, 1500, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1500000, 1600000, 1700000, 1800000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2750000, 2900000, 3100000, 3400000, 3700000, 4000000, 4300000, 4600000, 4900000, 5200000, 5500000, 5800000, 6100000, 6400000, 6700000, 7000000] 

	i = 0

	while exp >= exptoup[i] and i in range(len(exptoup) - 1):
		exp -= exptoup[i]
		i += 1

	print('sbstalk - formatExp: Skills Formatted, Returning Values')
	return (i if i == 60 else i - 1), exp, exptoup[i]

def getSkills(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()

	print('sbstalk - getSkills: Received Data')

	datap = sbdata['profile']['members'][uuid]

	combat, combatexp, combattoup = formatExp(round(datap['experience_skill_combat'], 2))
	foraging, foragingexp, foragingtoup = formatExp(round(datap['experience_skill_foraging'], 2))
	farming, farmingexp, farmingtoup = formatExp(round(datap['experience_skill_farming'], 2))
	enchanting, enchantingexp, enchantingtoup = formatExp(round(datap['experience_skill_enchanting'], 2))
	alchemy, alchemyexp, alchemytoup = formatExp(round(datap['experience_skill_alchemy'], 2))
	mining, miningexp, miningtoup = formatExp(round(datap['experience_skill_mining'], 2))
	fishing, fishingexp, fishingtoup = formatExp(round(datap['experience_skill_fishing'], 2))

	print('sbstalk - getSkills: Returning Requested Data')
	return [combat, foraging, farming, enchanting, alchemy, mining, fishing], [combatexp, foragingexp, farmingexp, enchantingexp, alchemyexp, miningexp, fishingexp], [combattoup, foragingtoup, farmingtoup, enchantingtoup, alchemytoup, miningtoup, fishingtoup]

def findSkillAverage(uuid):
	p, c, d= getSkills(uuid)

	sum = 0

	for i in p:
		sum += i

	print('sbstalk - findSkillAverage: Skill Average Found')
	return round(sum / 7, 2)

def getAuctionData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()

	print('sbstalk - getAuctionData: API Data Received')

	datap = sbdata['profile']['members'][uuid]

	stats = datap['stats']
	
	auction_bids = stats['auctions_bids']
	auction_highest_bid = int(stats['auctions_highest_bid'])
	auctions_won = stats['auctions_won']
	gold_spent_auctions = int(stats['auctions_gold_spent']) + 1
	gold_earnt_auctions = int(stats['auctions_gold_earned']) + 1
	completed_auctions = stats['auctions_completed']

def findSlayerCost(a, b, c, d):
	return a*100 + b*1000 + c*10000 + d*50000

def findSlayerLevel(exp):
	if exp > 1000000:
		return 9
	elif exp > 400000:
		return 8
	elif exp > 100000:
		return 7
	elif exp > 20000:
		return 6
	elif exp > 5000:
		return 5
	elif exp > 1000:
		return 4
	elif exp > 200:
		return 3
	elif exp > 15:
		return 2
	elif exp > 5:
		return 1
	else:
		return 0

def findCostToNextLevel(exp):
	clevel = findSlayerLevel(exp)

	if clevel == 9:
		return [0, 0, 0]

	levelreq = [0, 5, 15, 200, 1000, 5000, 20000, 100000, 400000, 1000000]

	req_exp = levelreq[clevel + 1] - exp

	t4r = req_exp / 500

	return [t4r, req_exp, t4r*50000]

def getZombieSlayerData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	full_data = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()
	zombie_data = full_data['profile']['members'][uuid]['slayer_bosses']['zombie']

	t1_kills = zombie_data['boss_kills_tier_0']
	t2_kills = zombie_data['boss_kills_tier_1']
	t3_kills = zombie_data['boss_kills_tier_2']
	t4_kills = zombie_data['boss_kills_tier_3']
	print('sbstalk - getZombieSlayerData: No of Kills Found')

	exp = zombie_data['xp']
	print('sbstalk - getZombieSlayerData: Exp Found')

	level = findSlayerLevel(exp)

	print('sbstalk - getZombieSlayerData: Level Found')
	moneyspent = findSlayerCost(t1_kills, t2_kills, t3_kills, t4_kills)

	t4r, req_exp, money_req = findCostToNextLevel(exp)
	
	levelcompletion = exp * 100 / (req_exp + exp)

	return [t1_kills, t2_kills, t3_kills, t4_kills, exp, level, numberformat.human_format(moneyspent), levelcompletion, t4r, req_exp, numberformat.human_format(money_req)]

def getSpiderSlayerData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	full_data = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()
	zombie_data = full_data['profile']['members'][uuid]['slayer_bosses']['spider']

	t1_kills = zombie_data['boss_kills_tier_0']
	t2_kills = zombie_data['boss_kills_tier_1']
	t3_kills = zombie_data['boss_kills_tier_2']
	t4_kills = zombie_data['boss_kills_tier_3']
	print('sbstalk - getSpiderSlayerData: No of Kills Found')

	exp = zombie_data['xp']
	print('sbstalk - getSpiderSlayerData: Exp Found')

	level = findSlayerLevel(exp)

	print('sbstalk - getSpiderSlayerData: Level Found')
	moneyspent = findSlayerCost(t1_kills, t2_kills, t3_kills, t4_kills)

	t4r, req_exp, money_req = findCostToNextLevel(exp)
	
	levelcompletion = exp * 100 / (req_exp + exp)

	return [t1_kills, t2_kills, t3_kills, t4_kills, exp, level, numberformat.human_format(moneyspent), levelcompletion, t4r, req_exp, numberformat.human_format(money_req)]

def getWolfSlayerData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	full_data = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()
	zombie_data = full_data['profile']['members'][uuid]['slayer_bosses']['wolf']

	t1_kills = zombie_data['boss_kills_tier_0']
	t2_kills = zombie_data['boss_kills_tier_1']
	t3_kills = zombie_data['boss_kills_tier_2']
	t4_kills = zombie_data['boss_kills_tier_3']
	print('sbstalk - getWolfSlayerData: No of Kills Found')

	exp = zombie_data['xp']
	print('sbstalk - getWolfSlayerData: Exp Found')

	level = findSlayerLevel(exp)

	print('sbstalk - getWolfSlayerData: Level Found')
	moneyspent = findSlayerCost(t1_kills, t2_kills, t3_kills, t4_kills)

	t4r, req_exp, money_req = findCostToNextLevel(exp)
	
	levelcompletion = exp * 100 / (req_exp + exp)

	return [t1_kills, t2_kills, t3_kills, t4_kills, exp, level, numberformat.human_format(moneyspent), levelcompletion, t4r, req_exp, numberformat.human_format(money_req)]



# def getSpiderSlayerData(uuid):
# def getWolfSlayerData(uuid):
# def getTotalSlayerData(uuid):

# def getDungeonData(uuid):

# def getSBdata(uuid):
# 	highest_crit_damage = stats['highest_critical_damage']
# 	collected_fairy_souls = datap['fairy_souls_collected']

# uuid = getUUID('NottCurious')
# playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()
# print(playerdata['player']['stats']['SkyBlock']['profiles'])
# print(getLatestProfile(uuid), int(getBankBalance(uuid)))
# print(formatExp(11555397))
# exptoup = [0, 50, 125, 200, 300, 500, 750, 1000, 1500, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1500000, 1600000, 1700000, 1800000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2750000, 2900000, 3100000, 3400000, 3700000, 4000000, 4300000, 4600000, 4900000, 5200000, 5500000, 5800000, 6100000, 6400000, 6700000, 7000000] 
# print(len(exptoup))
# print(getSkills(getUUID('NottCurious')))
# print(getSBdata(getUUID('NottCurious')))
# print(getZombieSlayerData(getUUID('NottCurious')))