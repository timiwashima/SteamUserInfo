# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 12:26:46 2023
Get information on a Steam User, Playtime by OS, and 3 most recently played games
@author: tiwashima
"""
import requests
from datetime import datetime

apiKey=# Get your API Key here=https://steamcommunity.com/login/home/?goto=%2Fdev%2Fapikey

# Replace with the steamID you want to look at
steamID='76561197982490351'

# Basic Account Information
playerSummaryURL='http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key='+apiKey+'&steamids='+steamID
request=requests.get(playerSummaryURL)
playerDict=request.json()
# Strip off the "response" key and the "players" key to get into the keys/values I want to work with
playerResponseInfo=playerDict['response']
playerResponsePlayer=playerResponseInfo['players']
playerInfo={}
for x in playerResponsePlayer:
    playerInfo=x

personaStates={0:'Offline',
               1:'Online',
               2:'Busy',
               3:'Away',
               4:'Snooze',
               5:'Looking to Trade',
               6:'Looking to Play'}
userStatus=playerInfo['personastate']

createdHumanTime=datetime.fromtimestamp(playerInfo['timecreated']).strftime('%A, %B %d, %Y %H:%M')
logoffHumanTime=datetime.fromtimestamp(playerInfo['lastlogoff']).strftime('%A, %B %d, %Y %H:%M')

print('Name: ' + playerInfo['personaname'])
print('Real Name: ' + playerInfo['realname'])
print('Status: '+personaStates[playerInfo['personastate']])
print('Last logoff: ' + logoffHumanTime)
print('Account Created: ' + createdHumanTime)
print('Profile URL: ' + playerInfo['profileurl'])

# Show Gameplay Statistics by Platform
playStatisticsURL='http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key='+apiKey+'&steamid='+steamID+'&format=json'
request=requests.get(playStatisticsURL)
statsDict=request.json()
# Strip off "response" key and use only the games key
statsResponseInfo=statsDict['response']
stats=statsResponseInfo['games']
windows=0
linux=0
mac=0
totalHours=0
for x in stats:
    windows+=x['playtime_windows_forever']
    linux+=x['playtime_linux_forever']
    mac+=x['playtime_mac_forever']
    totalHours+=x['playtime_windows_forever']+x['playtime_linux_forever']+x['playtime_mac_forever']
windowsHours=windows/60
linuxHours=linux/60
macHours=mac/60
totalHours=totalHours/60
windowsRoundedHours=round(windowsHours,2)
windowsPercentage=windowsHours/(windowsHours+linuxHours+macHours)
linuxRoundedHours=round(linuxHours,2)
linuxPercentage=linuxHours/(windowsHours+linuxHours+macHours)
macRoundedHours=round(macHours,2)
macPercentage=macHours/(windowsHours+linuxHours+macHours)
totalRoundedHours=round(totalHours,2)
print('\nWindows Playtime: ' + str(windowsRoundedHours) + ' hours (' + '{:.1%}'.format(windowsPercentage) + ')') 
print('Linux Playtime: ' + str(linuxRoundedHours) + ' hours (' + '{:.1%}'.format(linuxPercentage) + ')')
print('Mac Playtime: ' + str(macRoundedHours) + ' hours (' + '{:.1%}'.format(macPercentage) + ')')
print('Total Playtime: ' + str(totalRoundedHours) + ' hours')

# Recently Played Games Information
gameSummaryURL='http://api.steampowered.com/IPlayerService/GetRecentlyPlayedGames/v0001/?key='+apiKey+'&steamid='+steamID+'&format=json'
request=requests.get(gameSummaryURL)
gameDict=request.json()
# Strip off the "response" to work with the list value for the "games" key
gameResponseInfo=gameDict['response']
games=gameResponseInfo['games']
print('\nRecently Played Games')
for x in games:
    gameInfo=x
    print(gameInfo['name'])
    #Calculate the minute time into hours and only 2 decimal places
    totalWindowsHours=gameInfo['playtime_windows_forever']/60
    totalWindowsRoundedHours=round(totalWindowsHours,2)
    totalLinuxHours=gameInfo['playtime_linux_forever']/60
    totalLinuxRoundedHours=round(totalLinuxHours,2)
    totalMacHours=gameInfo['playtime_mac_forever']/60
    totalMacRoundedHours=round(totalMacHours,2)
    totalGameHours=gameInfo['playtime_forever']/60
    totalGameRoundedHours=round(totalGameHours,2)
    windowsPercentage=totalWindowsHours/(totalWindowsHours+totalLinuxHours+totalMacHours)
    linuxPercentage=totalLinuxHours/(totalWindowsHours+totalLinuxHours+totalMacHours)
    macPercentage=totalMacHours/(totalWindowsHours+totalLinuxHours+totalMacHours)
    print('  Total Playtime: ' + str(totalGameRoundedHours) + ' hours')
    print('    Windows Playtime: ' + str(totalWindowsRoundedHours) + ' hours (' + '{:.1%}'.format(windowsPercentage) + ')')
    print('    Linux Playtime: ' + str(totalLinuxRoundedHours) + ' hours (' + '{:.1%}'.format(linuxPercentage) + ')')
    print('    Mac Playtime: ' + str(totalMacRoundedHours) + ' hours (' + '{:.1%}'.format(macPercentage) + ')')
