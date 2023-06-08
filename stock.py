import datetime
import requests
from datetime import date, timedelta
import apimoex

import control_db
from stock_helper import *


def get_companies(user_id):
    user = control_db.get_user(user_id)
    if user == -1:
        return []
    else:
        us_id, sec, l_date = user
        ls = sec.split(" ")
        return ls


def add_company(user_id, company):
    company = company.upper()
    if not exist(company):
        return False
    user = control_db.get_user(user_id)
    if user == -1:
        control_db.set_user(user_id, [company], datetime.datetime.now().strftime("%y-%m-%d-%H-%M-%S"))
    else:
        us_id, sec, l_date = user
        ls = []
        if len(sec) == 0:
            ls = [company]
        else:
            ls = sec.split(" ")
            ls.append(company)
        control_db.set_user(us_id, ls, l_date)
    return True


def clear(user_id):
    user = control_db.get_user(user_id)
    us_id, sec, l_date = user
    control_db.set_user(user_id, "", l_date)


def delete_company(user_id, company):
    company = company.upper()
    user = control_db.get_user(user_id)
    if user == -1:
        return False
    else:
        us_id, sec, l_date = user
        ls = []
        if len(sec) != 0:
            ls = sec.split(" ")
        if company not in ls:
            return False
        ls.remove(company)
        control_db.set_user(us_id, ls, l_date)
        return True


def get_info_about_companies(user_id, interval=24, start_time=date.today() - timedelta(days=2)):
    companies = get_companies(user_id)
    with requests.Session() as session:
        result = [info_about_company(session, company, interval, start_time) for company in companies]
        return result


def already_in(user_id, company):
    return company in get_companies(user_id)


def get_size_companies(user_id):
    return len(get_companies(user_id))
