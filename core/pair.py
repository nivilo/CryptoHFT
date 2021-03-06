"""
CryptoHFT is a software that lets you trade cryptocurrencies on Binance
using an high-frequency-trading like algorithm.

Copyright (C) 2020 Emanuele Civini - ciwines - emanuelecivini11@gmail.com

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

###############################################################################

# STANDARD IMPORTS
from datetime import datetime

# CORE IMPORTS
from core.pair_data import PairData
from core.analyzer.trend_analyzer import *

###############################################################################

class Pair:
    # CONSTRUCTOR
    def __init__(self, name: str):
        self.name = name
        self.data = PairData()
        self.trendAnalyzer = TrendAnalyzer(self.data)
        self.currentDirection = TrendDirection.USELESS
        self.usable = True
        self.timestamp = 0

    # METHODS
    def updateCandlesticks(self, open: list, high: list,
                           low: list, close: list,
                           volume: list, closeTime: list) -> None:
        self.data.updateCandlesticks(open, high, low, close, volume, closeTime)
        self.trendAnalyzer.updatePairData(self.data)
        self.currentDirection = self.trendAnalyzer.getTrend()

    def getLastPrice(self) -> None:
        return self.close[0]

    def calculateMeanVolume(self) -> float:
        return self.data.calculateMeanVolume()

    def disable(self) -> None:
        self.usable = False
        self.timestamp = datetime.now()

    def enable(self, secondInterval: int) -> bool:
        if not self.usable:
            if datetime.now() - self.timestamp >= secondInterval:
                self.usable = True
                self.timestamp = 0
                return True
            return False
        return True