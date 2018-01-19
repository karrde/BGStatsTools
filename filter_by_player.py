#!/usr/bin/python

import json
import sys

DEBUG = 0


def debug(debug_str):
    if DEBUG:
        print debug_str

bgexports_file = open('BGStatsExport.json')
json1_str = bgexports_file.read()
bgexports_data = json.loads(json1_str)

print "Select user to filter:"
for x in range(0, len(bgexports_data['players'])):
    print "{}. {}".format(x, bgexports_data['players'][x]['name'])

try:
    player_choice=int(raw_input('Choice:'))
except ValueError:
    sys.exit("Not a number")
    

player_choice -= 1
if (player_choice > len(bgexports_data['players'])) or (player_choice < 0):
    sys.exit("Choice out of range")
    

filtered_data = {}
filtered_data['players'] = []
filtered_data['plays'] = []
filtered_data['games'] = []
filtered_data['locations'] = []
player = bgexports_data['players'][player_choice]


games = []
locations = []
players = []
for play in range(0, len(bgexports_data['plays'])):
    debug("looking at play {}".format(play))
    if [player['id'] in [d['playerRefId'] for d in bgexports_data['plays'][play]['playerScores'] if 'playerRefId' in d]][0]:
        debug("Found player")
        filtered_data['plays'].append(bgexports_data['plays'][play])
        games.append(bgexports_data['plays'][play]['gameRefId'])
        if 'locationRefId' in bgexports_data['plays'][play]:
            locations.append(bgexports_data['plays'][play]['locationRefId'])
        players.extend([d['playerRefId'] for d in bgexports_data['plays'][play]['playerScores'] if 'playerRefId' in d])
        
games = list(set(games))
locations = list(set(locations))
players = list(set(players))

for game in range(0, len(bgexports_data['games'])):
    if bgexports_data['games'][game]['id'] in games:
        filtered_data['games'].append(bgexports_data['games'][game])
         
for location in range(0, len(bgexports_data['locations'])):
    if bgexports_data['locations'][location]['id'] in locations:
        filtered_data['locations'].append(bgexports_data['locations'][location])

for player in range(0, len(bgexports_data['players'])):
    if bgexports_data['players'][player]['id'] in players:
        filtered_data['players'].append(bgexports_data['players'][player])

bgfiltered_file = open('BGStatsFilteredExport.json','w')
bgfiltered_file.write(json.dumps(filtered_data))

