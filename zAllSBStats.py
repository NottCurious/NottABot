# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv
import zNumberFormat
import zSBStalk

# Loading Data From .env File
load_dotenv()
env_path = Path('.') / '.env'
api_key = os.getenv("API_KEY")

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

def getLatestProfile(username):
	return zSBStalk.getLatestProfile(getUUID(username))

def getStats(username):
	latestProfile, latestProfileID = getLatestProfile(username)

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()['profiles'][latestProfileID]['data']['stats']

	health = zNumberFormat.comma(data['health'])
	defence = zNumberFormat.comma(data['defense'])
	effective_health = zNumberFormat.comma(data['effective_health'])
	strength = zNumberFormat.comma(data['strength'])
	speed = zNumberFormat.comma(data['speed'])
	intelligence = zNumberFormat.comma(data['intelligence'])
	sea_creature_chance = zNumberFormat.comma(data['sea_creature_chance'])
	magic_find = zNumberFormat.comma(data['magic_find'])
	pet_luck = zNumberFormat.comma(data['pet_luck'])
	ferocity = zNumberFormat.comma(data['ferocity'])
	ability_damage = zNumberFormat.comma(data['ability_damage'])
	mining_speed = zNumberFormat.comma(data['mining_speed'])
	mining_fortune = zNumberFormat.comma(data['mining_fortune'])
	farming_fortune = zNumberFormat.comma(data['farming_fortune'])
	foraging_fortune = zNumberFormat.comma(data['foraging_fortune'])

	talismans = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()['profiles'][latestProfileID]['data']['talismanCount']

	return [health, defence, effective_health, strength, speed, intelligence, sea_creature_chance, magic_find, pet_luck, ferocity, ability_damage, mining_speed, mining_fortune, farming_fortune, foraging_fortune]

def getFairySouls(username):
	latestProfile, latestProfileID = getLatestProfile(username)

	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()['profiles'][latestProfileID]['data']['fairy_souls']

	collected = data['collected']
	total = data['total']
	progress = round(data['progress'] * 100, 2)

	return [collected, total, progress]
	
def maincommand(username):
	stats = getStats(username)
	fairy_souls = getFairySouls(username)

	return stats + fairy_souls