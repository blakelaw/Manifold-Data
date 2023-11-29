# To modify this for other markets, change the contractSlug on line 26. To find this, go to any market page and copy-paste the text at the end of the URL
# Link to this market: https://manifold.markets/milanw/will-sam-altman-be-the-ceo-of-opena

import requests
import json
import csv
import datetime

def get_unix_timestamp(year, month, day, hour, minute):
    dt = datetime.datetime(year, month, day, hour, minute)
    # Convert to Unix timestamp in milliseconds
    return int(dt.timestamp() * 1000)

# Constants
MAX_COUNT = 20

def loadBets():
    ret = []
    i = 0
    lastId = None

    while True:
        response = requests.get(
            'https://manifold.markets/api/v0/bets',
            params={'limit': 1000, 'before': lastId, 'contractSlug': 'will-sam-altman-be-the-ceo-of-opena'} 
        )
        bets = json.loads(response.content)
        print('Page loaded...')

        if len(bets) == 0 or i > MAX_COUNT:
            print('finished at', i)
            print('lastId', lastId)
            return ret

        for bet in bets:
            if bet.get('isRedemption'):
                continue
            for fill in bet['fills']:
                ret.append({
                    "bet_id": bet['id'],
                    "timestamp": fill['timestamp'],
                    "amount": fill['amount'],
                    "probability": bet['probAfter']
                })

        lastId = bets[-1]['id']
        i += 1

def write_bets_to_csv(bets):
    with open('bets.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["bet_id", "timestamp", "amount", "probability"])
        writer.writeheader()
        for bet in bets:
            writer.writerow(bet)

def main():
    bets = loadBets()
    write_bets_to_csv(bets)
    print("Bets written to CSV file.")

main()
