import freqtrade.vendor.qtpylib.indicators as qtpylib
import numpy as np
import talib.abstract as ta
from freqtrade.strategy import (IStrategy, informative, DecimalParameter)
from pandas import DataFrame, Series
import talib.abstract as ta
import math
import pandas_ta as pta
import freqtrade.vendor.qtpylib.indicators as qtpylib
# from finta import TA as fta
import logging
from logging import FATAL
from datetime import datetime, timedelta
from typing import Optional, Union
from freqtrade.persistence import Trade
from functools import reduce

logger = logging.getLogger(__name__)


class ecV1(IStrategy):

    def version(self) -> str:
        return "v1"

    INTERFACE_VERSION = 3

    can_short = True
    
    # ROI table: 
    minimal_roi = {
        "360": -1,
        "164": 0,
        "90": 0.015,
        "60": 0.03,
        "30": 0.1,
        "0": 0.2
    }

    # Stoploss:
    stoploss = -0.1

    # Trailing stop:
    trailing_stop = True
    trailing_stop_positive = 0.01
    trailing_stop_positive_offset = 0.05
    trailing_only_offset_is_reached = True

    # Sell signal
    use_exit_signal = True
    exit_profit_only = False
    exit_profit_offset = 0.01
    ignore_roi_if_entry_signal = False

    timeframe = '5m'

    process_only_new_candles = True
    startup_candle_count = 100

    plot_config = {
        'main_plot': {
            'ema_12': {},
            'ema_26': {},
            'ema_120_1h': {},
        },
    }

    # Strategy parameters 阈值
    buy_umacd_max = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.01176, space="buy")
    buy_umacd_min = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.01416, space="buy")
    sell_umacd_max = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.02323, space="sell")
    sell_umacd_min = DecimalParameter(-0.05, 0.05, decimals=5, default=-0.00707, space="sell")

    # Define informative upper timeframe for each pair. Decorators can be stacked on same
    # method. Available in populate_indicators as 'rsi_30m' and 'rsi_1h'.
    @informative('1h')
    def populate_indicators_1h(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        dataframe['ema_120'] = ta.EMA(dataframe, timeperiod=120)
        return dataframe

    # 5m
    def populate_indicators(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        dataframe['ema_12'] = ta.EMA(dataframe, timeperiod=12)
        dataframe['ema_26'] = ta.EMA(dataframe, timeperiod=26)
        dataframe['umacd'] = (dataframe['ema_12'] / dataframe['ema_26']) - 1
        # 多头行情 umacd > 0 反之 xx  绝对值 越大 短期均价 偏离 长期均价 越大 回归

        # 归一化 [0,1]  机器学习  freqai 

        return dataframe

    def populate_entry_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:
        long_conditions = []
        short_conditions = []
        dataframe.loc[:, 'enter_tag'] = ''

        # 做多 信号1 趋势类 ema金叉 
        enter_long_1 = (
            (dataframe["close"] > dataframe['ema_120_1h'])
            &
            qtpylib.crossed_above(dataframe['ema_12'], dataframe['ema_26'])
            &
            (dataframe['volume'] > 0)
        )
        dataframe.loc[enter_long_1, 'enter_tag'] += 'enter_long_1_'
        long_conditions.append(enter_long_1)

        # 做多 信号2 抄底类 xxx
        enter_long_2 = (
            (dataframe['umacd'].between(self.buy_umacd_min.value, self.buy_umacd_max.value))
            &
            (dataframe['volume'] > 0)
        )
        dataframe.loc[enter_long_2, 'enter_tag'] += 'enter_long_2_'
        long_conditions.append(enter_long_2)

        if long_conditions:
            dataframe.loc[
                reduce(lambda x, y: x | y, long_conditions),
                'enter_long'
            ]=1
        else:
            dataframe.loc[(), ['enter_long', 'enter_tag']] = (0, 'no_long_entry')

        # dataframe.loc[
        #     (
        #         (dataframe["close"] < dataframe['ema_120_1h'])
        #         &
        #         qtpylib.crossed_below(dataframe['ema_12'], dataframe['ema_26'])
        #         &
        #         (dataframe['volume'] > 0)
        #     ),
        #     ['enter_short', 'enter_tag']] = (1, 'short_1')

        return dataframe

    def populate_exit_trend(self, dataframe: DataFrame, metadata: dict) -> DataFrame:

        # dataframe.loc[
        #     (
        #         (dataframe["close"] < dataframe['ema_120_1h'])
        #         &
        #         (dataframe['volume'] > 0)
        #     ),
        #     ['exit_long', 'exit_tag']] = (1, 'exit_long_1')

        # dataframe.loc[
        #     (
        #         (dataframe["close"] > dataframe['ema_120_1h'])
        #         &
        #         (dataframe['volume'] > 0)
        #     ),
        #     ['exit_short', 'exit_tag']] = (1, 'exit_short_1')

        dataframe.loc[(), ['exit_long', 'exit_tag']] = (0, 'no_long_exit')
        dataframe.loc[(), ['exit_short', 'exit_tag']] = (0, 'no_short_exit')

        return dataframe

    def confirm_trade_entry(self, pair: str, order_type: str, amount: float, rate: float,
                            time_in_force: str, current_time: datetime, entry_tag: Optional[str], 
                            side: str, **kwargs) -> bool:

        # if entry_tag == "":
        #     return False

        return True

    def custom_exit(self, pair: str, trade: 'Trade', current_time: 'datetime', current_rate: float,
                    current_profit: float, **kwargs):

        # current_time ++
        # candle 指标
        dataframe, _ = self.dp.get_analyzed_dataframe(pair, self.timeframe)
        last_candle = dataframe.iloc[-1].squeeze()

        if trade.enter_tag == 'enter_long_1_':
            if last_candle['close'] < last_candle['ema_120_1h']:
                return "custom_exit_long_1"

    def confirm_trade_exit(self, pair: str, trade: Trade, order_type: str, amount: float,
                           rate: float, time_in_force: str, exit_reason: str,
                           current_time: datetime, **kwargs) -> bool:

        # # umacd 信号 不想使用 exit_signal
        # if trade.enter_tag == "enter_long_2_" and exit_reason == "exit_signal":
        #     return False
    
        return True

    # 前瞻性 回测陷阱 trailing_stop  --timeframe-detail 1m  降低 roi 影响  open high low close   14%  实盘  1%   1m   滑点    级别 突破 价格  1%  2%  

    # 开发 信号 umacd 