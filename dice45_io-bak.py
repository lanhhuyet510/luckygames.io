#!/usr/bin/python3.7

import json
import requests
import secrets
import os

TOTAL_PROFIT = 0
TOTAL_BET = 0
TARGET_PROFIT = 20
CURRENT_BALANCE = 0
DOMAIN = "io"
HEADERS = {
            'User-Agent': 'YOUR USER AGENT',
            'Accept': 'text/html, */*; q=0.01',
            'Accept-Language': 'en-US,en;q=0.5',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'X-Requested-With': 'XMLHttpRequest',
            'Cookie': '<YOUR COOKIE'
        }
serverSeedHash = ""


def randomSeed():
    global serverSeedHash
    global BALANCE
    global HEADERS
    try:
        API_ENDPOINT = "https://luckygames." + DOMAIN + "/request/"
        DATA = {'action':'randomizeSeed', 'hash' : 'YOUR HASH HERE', 'previousSeedHash':''}
        r = requests.post(url = API_ENDPOINT, headers = HEADERS, data = DATA, timeout = 10)
        serverSeedHash = json.loads(r.text).get('serverSeedHash','null')
    except:
        serverSeedHash = randomSeed()
    return serverSeedHash

def writeHistory(betID, clientSeed, _prevServerSeed, serverSeedHash, resultNumber, profit):
    LOG_FILE = "game_history.txt"
    logWriter = open(LOG_FILE, "a+")
    logWriter.write("%s|%s|%s|%s|%s|%s \r\n" % (betID, clientSeed, _prevServerSeed, serverSeedHash, resultNumber, profit))
    logWriter.close()

def writeHighRoll(betID, clientSeed, serverSeedHash, resultNumber, betAmount, profit):
    global DOMAIN
    logWriter = open('highBets_' + DOMAIN +'.txt', "a+")
    logWriter.write("%s|%s|%s|%s|%s|%s \r\n" % (betID, clientSeed, serverSeedHash, resultNumber, betAmount, profit))
    logWriter.close()

def doBet(coinName, betAmount, prediction, direction):
    global TOTAL_BET
    global TOTAL_PROFIT
    global HEADERS
    global CURRENT_BALANCE
    global serverSeedHash
    try:
        clientSeed = secrets.token_hex(16)
        if TOTAL_BET == 0:
            serverSeedHash = randomSeed()
        API_ENDPOINT = "https://luckygames." + DOMAIN + "/play/"
        DATA = {'game':'dice', 'coin' : coinName, 'betAmount': betAmount, 'prediction':prediction, 'direction':direction,'clientSeed':clientSeed, 'serverSeedHash': serverSeedHash, 'hash':'YOUR HASH HERE'}
        r = requests.post(url = API_ENDPOINT, headers = HEADERS, data = DATA, timeout = 10)
        r_response = json.loads(r.text)
        _resultNumber = r_response.get('resultNumber','null')
        _gameResult = r_response.get('gameResult','null')
        _result = r_response.get('result','null')
        _profit = r_response.get('profit','null')
        _betID = r_response.get('id','null')
        _prevServerSeedHash = r_response.get('prevServerSeedHash','null')
        _prevServerSeed = r_response.get('prevServerSeed','null')
        _resultNumber = r_response.get('resultNumber','null')
        serverSeedHash = r_response.get('serverSeedHash', 'null')
        CURRENT_BALANCE = float(r_response.get('balance', '0'))
        
        if _result == 'false' or _result == False or _result == 'null':
            #print ("Trying again..")
            serverSeedHash = randomSeed()
            doBet(coinName, betAmount, prediction, direction)
        else:
            if float(betAmount) >= 1:
                writeHighRoll(_betID, clientSeed, _prevServerSeedHash, _resultNumber, betAmount, _profit)
            #writeHistory(_betID, clientSeed, _prevServerSeedHash, _resultNumber, _profit)
            #print ("Bet Amount: " + betAmount)
            #print ("Game Result: " + _gameResult)
            #print ("Profit: " + _profit)
            TOTAL_PROFIT = TOTAL_PROFIT + float(_profit)
            #print ("TOTAL PROFIT: {0:.10f}".format(TOTAL_PROFIT))
            return _gameResult
    except:
        #print ("Trying again..")
        serverSeedHash = randomSeed()
        doBet(coinName, betAmount, prediction, direction)

def main():
    global TOTAL_PROFIT
    global CURRENT_BALANCE
    global TARGET_PROFIT
    global TOTAL_BET
    coinName = 'doge'
    baseBetAmount = 0.0000025000
    betAmount = 0.0000025000
    direction = 'over'
    prediction = 55
    while TOTAL_PROFIT < TARGET_PROFIT:
        #secretsGenerator = secrets.SystemRandom()
        #choseRandomDirection = secretsGenerator.randint(0,99)
        #choseRandomDirection = 60
        #if choseRandomDirection < 50:
        #    direction = 'under'
        #    prediction = 45
        #else:
        #    direction = 'over'
        #    prediction = 55
        _gameResult = doBet(coinName, '{0:10f}'.format(betAmount), prediction, direction)
        TOTAL_BET = TOTAL_BET + 1
        if _gameResult == "win":
            if TOTAL_BET > 5000:
                break
            if CURRENT_BALANCE > 1:
                baseBetAmount = CURRENT_BALANCE / 268435455
            betAmount = baseBetAmount
        else:
            betAmount = betAmount * 2
    logWriter = open('completed_' + DOMAIN + '.txt', "a+")
    logWriter.write("Completed! Profit: " + str(TOTAL_PROFIT) + " \r\n")
    logWriter.close()
            

if __name__== "__main__" :
    main()
