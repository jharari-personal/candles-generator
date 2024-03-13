import random
import csv
from datetime import datetime, timedelta
import json

# Function to calculate the number of decimal places in a given value
def calculate_decimal_places(value): 
    return len(str(value).split('.')[1])

# This function ensures that we get candles that look appropriate to the timeframe
def get_ATR(timeframe):
    timeframes = {
        "1 D": (10, 200),
        "1 W": (170, 400),
        "1 Mo": (400, 1200),
        "1 Min": (1, 10),
        "5 Min": (2, 20),
        "10 Min": (3, 30),
        "15 Min": (4, 40),
        "30 Min": (5, 50),
        "1 Hour": (10, 80),
        "4 Hour":(20, 140)
    }
    return random.randint(*timeframes.get(timeframe, (100, 200)))

# This function returns back the date for each candle
def get_date(date, delta, timeframe):
    timeframes = {
        "1 D": timedelta(days=1),
        "1 W": timedelta(weeks=1),
        "1 Mo": timedelta(weeks=4),
        "1 Min": timedelta(minutes=1),
        "5 Min": timedelta(minutes=5),
        "10 Min": timedelta(minutes=10),
        "15 Min": timedelta(minutes=15),
        "30 Min": timedelta(minutes=30),
        "1 Hour": timedelta(hours=1),
        "4 Hour": timedelta(hours=4)
    }

    try:
        date -= timeframes[timeframe] * delta
    except KeyError:
        raise Exception("Invalid Timeframe")
    return date
        
# Main function that generates candles
def generate_candles(rate, timeframe, numCandles, date_from):
    decimals = calculate_decimal_places(rate) # In order to use ATR appropriately
    adjusted_ATR = round(get_ATR(timeframe) * 10**(-decimals), 4)

    candles = []
    if date_from:
        current_date = datetime.strptime(date_from, "%Y-%m-%dT%H:%M:%S.000Z")
    else:
        current_date = datetime.utcnow()

    for i in range(numCandles):
        candle = {}

        if not candles:
            # For the first candle in the array, make sure that the Close is equal to the seed rate
            candle['bidOpen'] = round(random.uniform(rate - adjusted_ATR, rate + adjusted_ATR), 4)
            candle['bidHigh'] = round(candle['bidOpen'] + random.uniform(0, adjusted_ATR), 4)
            candle['bidLow'] = round(candle['bidOpen'] - random.uniform(0, adjusted_ATR), 4)
            candle['bidClose'] = round(rate, 4)
            candle['volume'] = random.randint(round(get_ATR(timeframe)*0.1), round(get_ATR(timeframe)*100))
            candle['date'] = current_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        else:
            # For the subsequent candles, ensure the Open is equal to the last candle's Close, randomze the rest
            candle['bidOpen'] = round(candles[-1]['bidClose'], 4)
            candle['bidHigh'] = round(candle['bidOpen'] + random.uniform(0, adjusted_ATR), 4)
            candle['bidLow'] = round(candle['bidOpen'] - random.uniform(0, adjusted_ATR), 4)
            candle['bidClose'] = round(random.uniform(candle['bidLow'], candle['bidHigh']), 4)
            candle['volume'] = random.randint(round(get_ATR(timeframe)*0.1), round(get_ATR(timeframe)*100))
            candle['date'] = ""

        candles.append(candle)
    
    # Now we make sure to add a date to each candle, starting from today (daily)
    for index, candle in enumerate(candles, start=0):
        if not candle['date']:
            candle['date'] = get_date(current_date, index, timeframe).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    candles.reverse()  # So that the last candle is equal to the seed rate 
    return candles

def export_to_csv(candles, filename='output.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['date', 'bidOpen', 'bidHigh', 'bidLow', 'bidClose', 'volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for candle in candles:
            writer.writerow(candle)

def main():
    rate = 1.28418
    timeframe = "1 D"
    numCandles = 5
    date_from = "2023-05-17T19:24:07.000Z" # optional
    #date_from = ""
    candles = generate_candles(rate, timeframe, numCandles, date_from)
    export_to_csv(candles)
    print(json.dumps(candles, indent=4))

main()