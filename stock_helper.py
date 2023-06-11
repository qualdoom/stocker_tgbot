import datetime
import apimoex
import requests
from datetime import timedelta


def exist(company):
    with requests.Session() as session:
        x = apimoex.find_security_description(session, company)
        if len(x) != 0 and 'error' in x[0]:
            return False
        if len(apimoex.find_security_description(session, company)) == 0:
            return False
    return True


def choose_interval(last_time, current_time):
    if current_time - last_time < timedelta(days=1):
        return 1
    if current_time - last_time < timedelta(days=7):
        return 10
    if current_time - last_time < timedelta(days=31):
        return 60
    if current_time - last_time < timedelta(days=365 * 2):
        return 24
    if current_time - last_time < timedelta(days=365 * 7):
        return 7
    return 31


def get_cost_in_time(company, time):
    with requests.Session() as session:
        interval = choose_interval(time, datetime.datetime.today())
        x = apimoex.get_market_candles(session, company, start=time, interval=interval)
        if len(x) == 0:
            return apimoex.get_market_candles(session, company, interval=4)[-1]['close']
        else:
            return x[0]['open']


def info_about_company(session, company, interval, start_time, end_time=datetime.datetime.today()):
    data = apimoex.get_market_candles(session=session, security=company, interval=interval,
                                      start=str(start_time),
                                      end=str(end_time))  # return list of pandas frame
    if len(data) == 0:
        return {"error": 1}  # error appeared
    low = min(data, key=lambda x: int(x['low']))['low']
    high = max(data, key=lambda x: int(x['high']))['high']
    prices = [(e['close']) for e in data]
    time = [(e['begin']) for e in data]
    return {"company": company, "open": data[0]['open'], "close": data[-1]['close'], "high": high,
            "low": low, "price": prices, "date": time, "error": 0}


def get_info_about_company(company, interval=1, start_time=datetime.datetime.today() - timedelta(days=7),
                           end_time=datetime.datetime.today()):
    with requests.Session() as session:
        result = info_about_company(session, company, interval, start_time, end_time)
        return result
