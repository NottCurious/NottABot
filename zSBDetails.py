# Importing Libraries
from requests import get
from pathlib import Path
import os
from dotenv import load_dotenv
import zNumberFormat

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

def getCurrentArmor(username):
	data = get('https://sky.shiiyu.moe/api/v2/profile/%s' % (username)).json()

	latest_profile, latest_profile_id = getLatestProfile(getUUID(username))

	armor = data['profiles'][latest_profile_id]['items']['armor']
	current_armor = []

	i = 0

	# # while i < 5:
	# # 	current_armor.append(armor[i]['display_name'] if armor[i] != None else '')
	# 	i += 1

	for i in range(len(armor)):
		current_armor.append(armor[i]['display_name'] if armor[i] != None else '')


	return current_armor
