REM 使用虚拟环境
REM call .venv\Scripts\activate.bat
REM python ./freqtrade/main.py download-data -c ./user_data/config_binance_future.json --days 90 --timeframes 1h

REM 非虚拟环境
C:\py310\python.exe ./freqtrade/main.py download-data -c ./user_data/config_binance_future.json --days 90 --timeframes 1h

pause