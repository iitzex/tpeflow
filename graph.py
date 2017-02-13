import matplotlib.pyplot as plt
import numpy as np
import matplotlib
matplotlib.use('Agg')

def plot(count, _yesterday, _today, _tomorrow):
    xticks = np.arange(0, 24, 1)
    yticks = np.arange(0, 80, 5)
    plt.title('TPE Flow')
    plt.xlabel('Time(24hr)')
    plt.ylabel('Count')
    plt.xticks(xticks)
    plt.yticks(yticks)
    # plt.grid(True)

    yesterday, = plt.plot(xticks, count[3], color='g', linestyle='-', label=_yesterday + ', ' + str(count[0]))
    today, = plt.plot(xticks, count[4], color='b', label=_today + ', ' + str(count[1]))
    tomorrow, = plt.plot(xticks, count[5], color='r',linestyle='-', label=_tomorrow + ', ' + str(count[2]))
    arr = plt.bar(xticks-0.1, count[9], 0.2, color='#fe9900', alpha=0.4, label='arrival')
    dep = plt.bar(xticks-0.1, count[8], 0.2, color='#4D95F2', alpha=0.4, bottom=count[9], label='depature')

    for i in range(0, 24):
        arr_h = count[9][i] / 2
        dep_h = count[8][i] / 2 + count[9][i]
        plt.text(i + 0.1, arr_h, count[9][i], fontsize=10, color='#4b4b4b', alpha=0.7)
        plt.text(i + 0.1, dep_h, count[8][i], fontsize=10, color='#4b4b4b', alpha=0.7)
        plt.text(i - 0.1, count[4][i] + 1.5, count[4][i], fontsize=11)

    plt.ylim(0, 53)
    plt.xlim(-0.5, 24)
    plt.legend(loc=2, handles=[yesterday, today, tomorrow, dep, arr], fontsize=11)
    plt.savefig('tpeflow.png')
#    plt.show()
