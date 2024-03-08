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
        ATR1 = random.randint(200, 300)
    elif timeframe == "h":
        ATR1 = random.randint(20, 30)
    else:
        ATR1 = random.randint(100, 150)
    return ATR1

# This function returns back the date for each candle
def get_date(date, delta):
    date -= timedelta(days=delta)
    return date
        
# Main function that generates candles
def generate_candles(rate, timeframe, numCandles):
    decimals = calculate_decimal_places(rate) # In order to use ATR appropriately
    adjusted_ATR = round(get_ATR(timeframe) * 10**(-decimals), 4)

    candles = []
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
        else:
            # For the subsequent candles, ensure the Open is equal to the last candle's Close, randomze the rest
            candle['Open'] = round(candles[-1]['Close'], 4)
            candle['High'] = round(candle['Open'] + random.uniform(0, adjusted_ATR), 4)
            candle['Low'] = round(candle['Open'] - random.uniform(0, adjusted_ATR), 4)
            candle['Close'] = round(random.uniform(candle['Low'], candle['High']), 4)
            candle['Volume'] = random.randint(1000, 100000)

        candles.append(candle)
    
    # Now we make sure to add a date to each candle, starting from today (daily)
    for index, candle in enumerate(candles, start=1):
        candle['Date'] = get_date(current_date, index).strftime("%Y-%m-%dT%H:%M:%S.000Z")

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
    timeframe = "w"
    numCandles = 1000

    candles = generate_candles(rate, timeframe, numCandles)
    export_to_csv(candles)

