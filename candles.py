import random
import csv
from datetime import datetime, timedelta

# Function to calculate the number of decimal places in a given value
def calculate_decimal_places(value): 
    return len(str(value).split('.')[1])

# This function ensures that we get candles that look appropriate to the timeframe
def get_ATR(timeframe):
    if timeframe == "d":
        ATR1 = random.randint(80, 120)
    elif timeframe == "w":
        ATR1 = random.randint(200, 400)
    elif timeframe == "h":
        ATR1 = random.randint(20, 50)
    elif timeframe == "m":
        ATR1 = random.randint(5, 30)
    else:
        ATR1 = random.randint(100, 200)
    return ATR1

# This function returns back the date for each candle
def get_date(date, delta, timeframe):
    if timeframe == "d":
        date -= timedelta(days=delta)
    elif timeframe == "h":
        date -= timedelta(hours=delta)
    elif timeframe == "m":
        date -= timedelta(minutes=delta)
    elif timeframe == "w":
        date -= timedelta(weeks=delta)
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
            candle['Open'] = round(random.uniform(rate - adjusted_ATR, rate + adjusted_ATR), 4)
            candle['High'] = round(candle['Open'] + random.uniform(0, adjusted_ATR), 4)
            candle['Low'] = round(candle['Open'] - random.uniform(0, adjusted_ATR), 4)
            candle['Close'] = round(rate, 4)
            candle['Volume'] = random.randint(1000, 100000)
            candle['Date'] = current_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        else:
            # For the subsequent candles, ensure the Open is equal to the last candle's Close, randomze the rest
            candle['Open'] = round(candles[-1]['Close'], 4)
            candle['High'] = round(candle['Open'] + random.uniform(0, adjusted_ATR), 4)
            candle['Low'] = round(candle['Open'] - random.uniform(0, adjusted_ATR), 4)
            candle['Close'] = round(random.uniform(candle['Low'], candle['High']), 4)
            candle['Volume'] = random.randint(1000, 100000)
            candle['Date'] = ""

        candles.append(candle)
    
    # Now we make sure to add a date to each candle, starting from today (daily)
    for index, candle in enumerate(candles, start=1):
        if not candle['Date']:
            candle['Date'] = get_date(current_date, index, timeframe).strftime("%Y-%m-%dT%H:%M:%S.000Z")

    candles.reverse()  # So that the last candle is equal to the seed rate 
    return candles

def export_to_csv(candles, filename='output.csv'):
    with open(filename, 'w', newline='') as csvfile:
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for candle in candles:
            writer.writerow(candle)

def main():
    rate = 1.28418
    timeframe = "h"
    numCandles = 3
   # date_from = "2023-05-17T19:24:07.000Z" # optional
    date_from = ""
    candles = generate_candles(rate, timeframe, numCandles, date_from)
    export_to_csv(candles)
    print(candles)

main()