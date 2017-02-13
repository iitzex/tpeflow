# -*- coding: utf-8 -*-
import analysis
import FB
import graph
from datetime import date, timedelta


def show(count):
    fmt = "%m/%d"
    _today = date.today().strftime(fmt)
    _yesterday = (date.today() - timedelta(days=1)).strftime(fmt)
    _tomorrow  = (date.today() + timedelta(days=1)).strftime(fmt)

    msg = "    "
    msg += _yesterday +",%3d" % count[0] + "  "
    msg += _today + ",%3d" % count[1] +"  "
    msg += _tomorrow + ",%3d" % count[2] + "\n"
    msg += "-----------------------------------\n"

    for i in range(24):
        msg += "%02d" % i
        msg += " %02d(%02d,%02d)" % (count[3][i], count[6][i], count[7][i])
        msg += " %02d(%02d,%02d)" % (count[4][i], count[8][i], count[9][i])
        msg += " %02d(%02d,%02d)" % (count[5][i], count[10][i], count[11][i])
        msg += "\n"
    return msg, _yesterday, _today, _tomorrow

if __name__ == '__main__':
    count = analysis.getDailyCount()

    msg, _yesterday, _today, _tomorrow = show(count)
    print msg

    graph.plot(count, _yesterday, _today, _tomorrow)

    FB.post_graph(_today, msg)
    # FB.post(msg)
