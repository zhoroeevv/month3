import schedule, time, requests

def main():
    print("привет всем", time.ctime())

def second_func():
    print("Geeks & Codex")

def get_btc_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=BTCUSDT'
    respone = requests.get(url=url).json()
    btc_price= round(float(respone.get('price')))
    print(btc_price, time.ctime())
    
def get_eth_price():
    url = 'https://www.binance.com/api/v3/ticker/price?symbol=ETHUSDT'
    respone = requests.get(url=url).json()
    eth_price= round(float(respone.get('price')))
    print(eth_price, time.ctime())
    

schedule.every(2).seconds.do(get_btc_price)
schedule.every(2).seconds.do(get_eth_price)

# schedule.every().seconds.do(main)
# schedule.every().minutes.do(main)
# schedule.every().day.at('17:38').do(main)
# schedule.every().wednesday.at('17:41').do(main)
# schedule.every().day.at('17:43', 'Asia/Bishkek').do(main)
# schedule.every().minute.at(":30").do(main)
# schedule.every().minutes.do(main)
# schedule.every().minutes.do(second_func)


while True:
    schedule.run_pending()