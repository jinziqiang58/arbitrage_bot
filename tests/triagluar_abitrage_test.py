import ccxt
from datetime import datetime
import pandas as pd

pd.set_option('display.max_rows', 1500)
binance = ccxt.binance()
binance.load_markets()

Pairlists = list(binance.markets.keys())[:10]
Pl_sum = len(Pairlists)
s = []

for i in range(Pl_sum):
    name = str(Pairlists[i])
    c1 = name.split("/")[0]
    c2 = name.split("/")[1]
    ask = ccxt.binance().fetch_ticker(Pairlists[i])['ask']
    bid = ccxt.binance().fetch_ticker(Pairlists[i])['bid']
    s.append([name, c1, c2, ask, bid, str(datetime.today())[0:19]])
    

price = pd.DataFrame(s, columns=["name", "c1", "c2", "ask", "bid", "time"])
price = price.set_index("name")
print(price)
print(Pl_sum)

c = []
c = price['c1'].tolist() + price['c2'].tolist()

l = set(c)
l = sorted(l)

AbiPair = []
BaseCurrency = ["BTC", "ETH", "USDT", "BNB"]

for i0 in range(len(BaseCurrency)):
    T0 = BaseCurrency[i0]
    for i1 in range(len(l)):
        T1 = l[i1]
        if ((T0 + "/" + T1 in Pairlists) == True) or ((T1 + "/" + T0 in Pairlists) == True):

            for i2 in range(len(l)):
                T2 = l[i2]
                if ((T2 + "/" + T1 in Pairlists) == True) or ((T1 + "/" + T2 in Pairlists) == True):

                    if ((T2 + "/" + T0 in Pairlists) == True) or ((T0 + "/" + T2 in Pairlists) == True):
                        if (T1 + "/" + T0 in price.index.values) == True:
                            buyT1 = 1 / price.at[str(T1 + "/" + T0), 'ask']
                        else:
                            buyT1 = price.at[str(T0 + "/" + T1), 'bid']

                        if (T2 + "/" + T1 in price.index.values) == True:
                            buyT2 = buyT1 / price.at[str(T2 + "/" + T1), 'ask']
                        else:
                            buyT2 = buyT1 * price.at[str(T1 + "/" + T2), 'bid']

                        if (T0 + "/" + T2 in price.index.values) == True:
                            buyT0 = buyT2 / price.at[str(T0 + "/" + T2), 'ask'] - 1
                        else:
                            buyT0 = buyT2 * price.at[str(T2 + "/" + T0), 'bid'] - 1

                        AbiPair.append([T0, T1, T2, buyT1, buyT2, '{:.5f}'.format(buyT0)])


AbiPair = pd.DataFrame(AbiPair, columns=["T0", "T1", "T2", "BuyT1", "BuyT2", "BuyT0"])
AbiPair = AbiPair.sort_values('BuyT0', ascending=False)
print(AbiPair)