import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import ConnectionPatch

MIN = 0
MAX = 200

def getXY(logfile : str):
    with open(logfile, 'r') as f:
        lines = f.readlines()
    lines = [x.strip() for x in lines]
    lines = [x[1:len(x) - 1] for x in lines]
    x = []
    y = []
    for item in lines:
        item = item.split(', ')
        x.append(int(float(item[0])))
        y.append(float(item[1]))
    
    return x, y

plt.rcParams['axes.grid'] = True
x_t, y_t = getXY('ble.log')
x_gps, y_gps = getXY('gps.log')

x_babyOn = np.arange(MIN, MAX, 1)
y_babyOn = []
y_babyOn = [1 if x > x_t[0] and x <= x_t[-1] else 0 for x in x_babyOn]
print(x_t[0])

fig, axs = plt.subplots(3)  # Create a figure containing a single axes.

#upper bound
axs[0].plot(x_t, y_t, linewidth=2.0);
axs[0].axhline(y=40, color='r', linestyle='-')
axs[0].axhline(y=38, color='g', linestyle='--')

#lower bound
axs[0].axhline(y=4, color='r', linestyle='-')
axs[0].axhline(y=6, color='g', linestyle='--')

axs[0].set(xlabel='time (s)', ylabel='Temperature (°C)', 
    xlim=(MIN, MAX), ylim=(36, 42), xticks=np.arange(MIN, MAX, 20), yticks=np.arange(35, 42))


axs[1].scatter(x_gps, y_gps, linewidth=2.0);
axs[1].axhline(y=50, color='r', linestyle='-')
axs[1].set(xlabel='time (s)', ylabel='Distance (m)', xlim=(MIN, MAX), xticks=np.arange(MIN, MAX, 20), yticks=np.arange(0, 200, 50))

axs[2].step(x_babyOn, y_babyOn, linewidth=2.0);
axs[2].set(xlabel='time (s)', ylabel='Baby is On', 
    xlim=(MIN, MAX), ylim=(0, 2), xticks=np.arange(MIN, MAX, 20))

"""
con1 = ConnectionPatch(xyA=(x_t[0], 42), xyB=(x_t[0], 0),
        coordsA="data", coordsB="data", axesA=axs[0], axesB=axs[2],
        arrowstyle="-", linewidth=2, color="purple")

con2 = ConnectionPatch(xyA=(x_t[-1], 42), xyB=(x_t[-1], 0),
        coordsA="data", coordsB="data", axesA=axs[0], axesB=axs[2],
        arrowstyle="-", linewidth=2, color="purple")
"""
alarm = 155
con1 = ConnectionPatch(xyA=(155, 42), xyB=(155, 0),
        coordsA="data", coordsB="data", axesA=axs[0], axesB=axs[2],
        arrowstyle="-", linewidth=2, color="purple")

axs[2].add_artist(con1)
# axs[2].add_artist(con2)

# CHANGE MANUALLY FOR EACH PLOT 
axs[0].annotate("alarm",
                  xy=(alarm, y_t[x_t.index(alarm)]), xycoords='data',
                  xytext=(alarm - 20, y_t[x_t.index(alarm)] - 2), textcoords='data',
                  size=8, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w"),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"), 
                  )

a = 107
axs[1].annotate("car_moving",
                  xy=(a, y_gps[x_gps.index(a)]), xycoords='data',
                  xytext=(a, y_gps[x_gps.index(a)] - 50), textcoords='data',
                  size=8, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w"),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"), 
                  )

a = 149
axs[1].annotate("car_stopped",
                  xy=(a, y_gps[x_gps.index(a)]), xycoords='data',
                  xytext=(a + 25, y_gps[x_gps.index(a)] + 70), textcoords='data',
                  size=8, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w"),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"), 
                  )

axs[2].annotate("baby_set",
                  xy=(x_t[0], 1), xycoords='data',
                  xytext=(x_t[0] + 20, 0.5), textcoords='data',
                  size=8, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w"),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"), 
                  )

a = x_t[-1]
axs[2].annotate("default",
                  xy=(a, 1), xycoords='data',
                  xytext=(a + 20, 0.5), textcoords='data',
                  size=8, va="center", ha="center",
                  bbox=dict(boxstyle="round4", fc="w"),
                  arrowprops=dict(arrowstyle="-|>",
                                  connectionstyle="arc3,rad=-0.2",
                                  fc="w"), 
                  )

plt.show()
fig.savefig('graph2.png')