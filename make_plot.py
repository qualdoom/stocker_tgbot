import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib

matplotlib.use('agg')


def make_plot(x, y):
    _x = matplotlib.dates.date2num(x)
    myFmt = mdates.DateFormatter('%H:%M %D')
    plt.figure(figsize=(16, 9))
    plt.plot(_x, y, color='blue')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.savefig('graphics.png', bbox_inches='tight')
    plt.close()
