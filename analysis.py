# -*- coding: utf-8 -*-
import csv
import requests
from datetime import date, timedelta, time, datetime
from pytz import timezone


def getDailyCount():
    people = 'a_flight_v4.txt'
    cargo = 'af_flight_v4.txt'
    people_file = wget(people)
    cargo_file = wget(cargo)

    (_yesterday_count, _today_count, _tomorrow_count,
     _yesterday_time, _today_time, _tomorrow_time,
     _yesterday_time_dep, _yesterday_time_land,
     _today_time_dep, _today_time_land,
     _tomorrow_time_dep, _tomorrow_time_land) = parse(people_file, 'A')

    (_yesterday_cargo_count, _today_cargo_count, _tomorrow_cargo_count,
     _yesterday_cargo_time, _today_cargo_time, _tomorrow_cargo_time,
     _yesterday_cargo_dep, _yesterday_cargo_land,
     _today_cargo_dep, _today_cargo_land,
     _tomorrow_cargo_dep, _tomorrow_cargo_land)  = parse(cargo_file, 'A')

    _yesterday_sum = sumoftime(_yesterday_time, _yesterday_cargo_time)
    _today_sum = sumoftime(_today_time, _today_cargo_time)
    _tomorrow_sum = sumoftime(_tomorrow_time, _tomorrow_cargo_time)

    _yesterday_dep = sumoftime(_yesterday_time_dep, _yesterday_cargo_dep)
    _yesterday_land = sumoftime(_yesterday_time_land, _yesterday_cargo_land)
    _today_dep = sumoftime(_today_time_dep, _today_cargo_dep)
    _today_land = sumoftime(_today_time_land, _today_cargo_land)
    _tomorrow_dep = sumoftime(_tomorrow_time_dep, _tomorrow_cargo_dep)
    _tomorrow_land = sumoftime(_tomorrow_time_land, _tomorrow_cargo_land)

    print(_yesterday_sum)
    print(_yesterday_dep)
    print(_yesterday_land)

    print(_today_sum)
    print(_today_dep)
    print(_today_land)

    print(_tomorrow_sum)
    print(_tomorrow_dep)
    print(_tomorrow_land)

    print(_yesterday_count, _today_count, _tomorrow_count)
    print(_yesterday_cargo_count, _today_cargo_count, _tomorrow_cargo_count)

    _yesterday_total = _yesterday_count + _yesterday_cargo_count
    _today_total = _today_count + _today_cargo_count
    _tomorrow_total = _tomorrow_count + _tomorrow_cargo_count
    print(_yesterday_total, _today_total, _tomorrow_total)

    return (_yesterday_total, _today_total, _tomorrow_total,
            _yesterday_sum, _today_sum, _tomorrow_sum,
            _yesterday_dep, _yesterday_land,
            _today_dep, _today_land,
            _tomorrow_dep, _tomorrow_land)


def sumoftime(people, cargo):
    _sum = [0 for i in range(24)]

    for i, (k, v) in enumerate(zip(people, cargo)):
        _sum[i] = k + v

    return _sum


def getDate():
    Taipei = timezone('Asia/Taipei')
    now = datetime.now(Taipei)
    # print now

    fmt = "%Y/%m/%d"
    _today = now.strftime(fmt)
    _yesterday = (now - timedelta(1)).strftime(fmt)
    _tomorrow = (now + timedelta(1)).strftime(fmt)
    # print _yesterday, _today, _tomorrow

    return (_yesterday, _today, _tomorrow)


def wget(page):
    timestamp = datetime.now().strftime("%m_%d.%H_%M")
    filename = page + "." + timestamp

    # response = urllib2.urlopen('http://www.taoyuan-airport.com/uploads/flightx/'+page)
    # html = response.read()
    r = requests.get('http://www.taoyuan-airport.com/uploads/flightx/'+page)
    html = r.text
    target = open(filename, 'w')
    target.write(html)
    return filename


def parse(filename, action=''):
    (_yesterday, _today, _tomorrow) = getDate()

    csvfile = open(filename, 'r')
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    last_time = 0
    destlist = []

    _yesterday_count = 0
    _today_count = 0
    _tomorrow_count = 0
    _yesterday_time_count = [0 for i in range(24)]
    _yesterday_time_departure = [0 for i in range(24)]
    _yesterday_time_landing = [0 for i in range(24)]
    _today_time_count = [0 for i in range(24)]
    _today_time_departure = [0 for i in range(24)]
    _today_time_landing = [0 for i in range(24)]
    _tomorrow_time_count = [0 for i in range(24)]
    _tomorrow_time_departure = [0 for i in range(24)]
    _tomorrow_time_landing = [0 for i in range(24)]

    for row in reader:
        msg = ""
        action = row[1]
        iata = row[2]
        NO = row[4]
        expect_day = row[6]
        expect_time = row[7]
        actual_day = row[8]
        actual_time = row[9]
        bay = row[5]
        dest = row[10]
        status = row[13]

        if actual_time != last_time: #clean list
            destlist = []

        if "CANCEL" in status:
            msg += "--- "

        elif dest in set(destlist):
            msg += "+++ "

        else:
            destlist.append(dest)
            hour, mins, sec = actual_time.split(":")

            if expect_day == _yesterday and actual_day == _yesterday:
                _yesterday_count += 1
                _yesterday_time_count[int(hour)] += 1
                msg += "%03d " % _yesterday_count

                if action == 'D':
                    _yesterday_time_departure[int(hour)] += 1
                elif action == 'A':
                    _yesterday_time_landing[int(hour)] += 1

            elif expect_day == _today:
                _today_count += 1
                _today_time_count[int(hour)] += 1
                msg += "%03d " % _today_count

                if action == 'D':
                    _today_time_departure[int(hour)] += 1
                elif action == 'A':
                    _today_time_landing[int(hour)] += 1

            elif expect_day == _tomorrow:
                _tomorrow_count += 1
                _tomorrow_time_count[int(hour)] += 1
                msg += "%03d " % _tomorrow_count

                if action == 'D':
                    _tomorrow_time_departure[int(hour)] += 1
                elif action == 'A':
                    _tomorrow_time_landing[int(hour)] += 1

            else:
                msg += "///"  + " "

        msg += action + " "
        msg += iata + NO + " "
        msg += expect_day + " " + expect_time + " "
        msg += actual_day + " " + actual_time + " "
        msg += dest + " "
        msg += status + " "
        print(msg)

        last_time = actual_time

    return (_yesterday_count, _today_count, _tomorrow_count,
            _yesterday_time_count, _today_time_count, _tomorrow_time_count,
            _yesterday_time_departure, _yesterday_time_landing,
            _today_time_departure, _today_time_landing,
            _tomorrow_time_departure, _tomorrow_time_landing)

if __name__ == '__main__':
    # getDailyCount()
    print(getDate())
