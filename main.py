class Exception(Exception):
    def __init__(self, message):
        self.message = message
        self.name = 'Exception'

def start_day_of_ethiopian(year):
    new_year_day = year // 100 - year // 400 - 4
    return new_year_day if (year - 1) % 4 == 3 else new_year_day + 1

def to_gregorian(date_array):
    if isinstance(date_array, list):
        inputs = date_array
    else:
        inputs = list(date_array)

    if 0 in inputs or None in inputs or len(inputs) != 3:
        raise Exception("Malformed input can't be converted.")

    year, month, date = inputs

    new_year_day = start_day_of_ethiopian(year)
    gregorian_year = year + 7

    gregorian_months = [0.0, 30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31, 30]

    next_year = gregorian_year + 1
    if (next_year % 4 == 0 and next_year % 100 != 0) or next_year % 400 == 0:
        gregorian_months[6] = 29

    until = (month - 1) * 30.0 + date

    if until <= 37 and year <= 1575:
        until += 28
        gregorian_months[0] = 31
    else:
        until += new_year_day - 1

    if (year - 1) % 4 == 3:
        until += 1

    m = 0
    gregorian_date = None

    for i in range(len(gregorian_months)):
        if until <= gregorian_months[i]:
            m = i
            gregorian_date = until
            break
        else:
            m = i
            until -= gregorian_months[i]

    if m > 4:
        gregorian_year += 1

    order = [8, 9, 10, 11, 12, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    gregorian_months = order[m]

    return [gregorian_year, gregorian_months, gregorian_date]

def to_ethiopian(date_array):
    if isinstance(date_array, list):
        inputs = date_array
    else:
        inputs = list(date_array)

    if 0 in inputs or None in inputs or len(inputs) != 3:
        raise Exception("Malformed input can't be converted.")

    year, month, date = inputs

    if month == 10 and 5 <= date <= 14 and year == 1582:
        raise Exception('Invalid Date between 5-14 May 1582.')

    gregorian_months = [0.0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    ethiopian_months = [0.0, 30, 30, 30, 30, 30, 30, 30, 30, 30, 5, 30, 30, 30, 30]

    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        gregorian_months[2] = 29

    ethiopian_year = year - 8

    if ethiopian_year % 4 == 3:
        ethiopian_months[10] = 6

    new_year_day = start_day_of_ethiopian(year - 8)

    until = 0
    for i in range(1, month):
        until += gregorian_months[i]
    until += date

    tahissas = 26 if ethiopian_year % 4 == 0 else 25

    if year < 1582:
        ethiopian_months[1] = 0
        ethiopian_months[2] = tahissas
    elif until <= 277 and year == 1582:
        ethiopian_months[1] = 0
        ethiopian_months[2] = tahissas
    else:
        tahissas = new_year_day - 3
        ethiopian_months[1] = tahissas

    ethiopian_date = None

    for m in range(1, len(ethiopian_months)):
        if until <= ethiopian_months[m]:
            ethiopian_date = until + (30 - tahissas) if m == 1 or ethiopian_months[m] == 0 else until
            break
        else:
            until -= ethiopian_months[m]

    if m > 10:
        ethiopian_year += 1

    order = [0, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 1, 2, 3, 4]
    ethiopian_month = order[m]

    return [ethiopian_year, ethiopian_month, ethiopian_date+1]

# Example usage:
# gregorian_date = to_gregorian([2013, 3, 5])
# ethiopian_date = to_ethiopian([2003, 2, 8])
# print(ethiopian_date)
# print(gregorian_date)