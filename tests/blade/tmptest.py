import pandas as pd
import talib.abstract as ta
import numpy as np
import talib 



df= pd.DataFrame()
df["a"]=pd.Series([999,2,3,4,5])
df["b"]=pd.Series([10,20,304,1])
print(df)
print(talib.get_functions() )
print ( talib.get_function_groups() )


df = pd.DataFrame({'B': [0, 1, 2, np.nan, 4]})
#print(df)


#GET https://www.okx.com/api/v5/market/mark-price-candles

import requests
import pandas as pd
import ccxt
import json

# URL
url = "https://www.okx.com/api/v5/market/mark-price-candles?instId=BTC-USD-SWAP&bar=1Dutc"

# Send GET request
response = requests.get(url)

# Convert the response to JSON
data = response.json()

# Convert the JSON data to a dataframe
df = pd.DataFrame(data['data'])

# Convert the first column to datetime
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0].astype(float) / 1000, unit='s')

print("通过OKX公共API获取UTC日线数据：\n")

# Print the dataframe
print(df)


# URL
url = "https://www.okx.com/api/v5/market/mark-price-candles?instId=BTC-USD-SWAP&bar=1D"

# Send GET request
response = requests.get(url)

# Convert the response to JSON
data = response.json()

# Convert the JSON data to a dataframe
df = pd.DataFrame(data['data'])


# Convert the first column to datetime
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0].astype(float) / 1000, unit='s')

print("通过OKX公共API获取香港时间日线数据：\n")

# Print the dataframe
print(df)


# URL
url = "https://www.okx.com/api/v5/market/history-mark-price-candles?instId=BTC-USD-SWAP&bar=1Dutc"

# Send GET request
response = requests.get(url)

# Convert the response to JSON
data = response.json()

# Convert the JSON data to a dataframe
df = pd.DataFrame(data['data'])

# Convert the first column to datetime
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0].astype(float) / 1000, unit='s')

print("通过OKX公共API获取历史UTC日线数据：\n")

# Print the dataframe
print(df)


# URL
url = "https://www.okx.com/api/v5/market/history-mark-price-candles?instId=BTC-USD-SWAP&bar=1D"

# Send GET request
response = requests.get(url)

# Convert the response to JSON
data = response.json()

# Convert the JSON data to a dataframe
df = pd.DataFrame(data['data'])


# Convert the first column to datetime
df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0].astype(float) / 1000, unit='s')

print("通过OKX公共API获取香港时间日线历史数据：\n")

# Print the dataframe
print(df)


print("=="*100 +"\n")
config={}
# 读取配置文件
with open('./user_data/config_okx.json', 'r') as f:
    config = json.load(f)

cfg={"apiKey":config["exchange"]["key"],"secret":config["exchange"]["secret"],"password":config["exchange"]["password"]}
#print(cfg)

exchange = ccxt.okx(cfg)
exchange.enableRateLimit=True
exchange.httpsProxy=config["exchange"]["ccxt_config"]["httpsProxy"]
positions = exchange.fetchPositions()
for position in positions:
    print("position",json.dumps(position, indent=4))
