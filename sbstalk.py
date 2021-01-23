# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

# username = 'NottCurious'

# Getting UUID Using Mojang API
def getUUID(username):
	print("Receiving Mojang Player Data")
	try:
		playerdata_mojang = get("https://api.mojang.com/users/profiles/minecraft/%s" % (username)).json()
	
		uuid = playerdata_mojang["id"]
		print("UUID Received")

		return uuid
	except:
		return 'no'

def getLatestProfile(uuid):
	# uuid = getUUID(username)

	playerdata = get('https://api.hypixel.net/player?key=%s&uuid=%s' % (api_key, uuid)).json()

	j = 1
	latest_profile = []

	for i in playerdata['player']['stats']['SkyBlock']['profiles']:
		if j == 1:
			latest_profile = playerdata['player']['stats']['SkyBlock']['profiles'][i]['cute_name']
			latest_profile_id = playerdata['player']['stats']['SkyBlock']['profiles'][i]['profile_id']
			j += 1
	
	return latest_profile, latest_profile_id

def getBankBalance(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()

	bank_money = sbdata['profile']['banking']['balance']
	purse = sbdata['profile']['members'][uuid]['coin_purse']

	return int(bank_money), int(purse)

def formatExp(exp):
	exptoup = [0, 50, 125, 200, 300, 500, 750, 1000, 1500, 2000, 3500, 5000, 7500, 10000, 15000, 20000, 30000, 50000, 75000, 100000, 200000, 300000, 400000, 500000, 600000, 700000, 800000, 900000, 1000000, 1100000, 1200000, 1300000, 1400000, 1500000, 1600000, 1700000, 1800000, 1900000, 2000000, 2100000, 2200000, 2300000, 2400000, 2500000, 2600000, 2750000, 2900000, 3100000, 3400000, 3700000, 4000000, 4300000, 4600000, 4900000, 5200000, 5500000, 5800000, 6100000, 6400000, 6700000, 7000000] 

	i = 0

	while exp >= exptoup[i] and i in range(len(exptoup) - 1):
		exp -= exptoup[i]
		i += 1

	return i if i == 60 else i - 1

def getSkills(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()

	datap = sbdata['profile']['members'][uuid]

	combat = formatExp(int(datap['experience_skill_combat']))
	foraging = formatExp(int(datap['experience_skill_foraging']))
	farming = formatExp(int(datap['experience_skill_farming']))
	enchanting = formatExp(int(datap['experience_skill_enchanting']))
	alchemy = formatExp(int(datap['experience_skill_alchemy']))
	mining = formatExp(int(datap['experience_skill_mining']))
	fishing = formatExp(int(datap['experience_skill_fishing']))

	return [combat, foraging, farming, enchanting, alchemy, mining, fishing]

def getAuctionData(uuid):
	profile_name, profile_id = getLatestProfile(uuid)
	sbdata = get('https://api.hypixel.net/skyblock/profile?key=%s&profile=%s' % (api_key, profile_id)).json()

	datap = sbdata['profile']['members'][uuid]

	stats = datap['stats']
	
	auction_bids = stats['auctions_bids']
	auction_highest_bid = int(stats['auctions_highest_bid'])
	auctions_won = stats['auctions_won']
	gold_spent_auctions = int(stats['auctions_gold_spent']) + 1
	gold_earnt_auctions = int(stats['auctions_gold_earned']) + 1
	completed_auctions = stats['auctions_completed']

# def getZombieSlayerData(uuid):
# def getSpiderSlayerData(uuid):
# def getWolfSlayerData(uuid):
# def getTotalSlayerData(uuid):

# def getDungeonData(uuid):

# def getCollectionData(uuid):

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

# print(getSBdata(getUUID('NottCurious')))