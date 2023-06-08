import stock


def get_both_cost(company, last_time, current_time):
    a = stock.get_cost_in_time(company, last_time)
    b = stock.get_cost_in_time(company, current_time)
    return [a, b]


def get_difference(company, last_time, current_time):
    x = get_both_cost(company, last_time, current_time)
    if x[0] < x[1]:
        return [x[0], x[1], x[1] - x[0], x[1] / x[0] * 100 - 100]
    else:
        return [x[0], x[1], x[1] - x[0], x[0] / x[1] * 100 - 100]
