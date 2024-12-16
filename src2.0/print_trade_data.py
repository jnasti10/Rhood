#! /usr/local/bin/python3.8
from utils.trade_data import Trade_data
import json

obj = Trade_data(20000)
obj.load()
obj.print()
exit()
