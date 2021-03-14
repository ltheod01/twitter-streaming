from itertools import count
import pandas as pd
import matplotlib.pyplot as plt

from matplotlib.animation import FuncAnimation
#matplotlib notebook

plt.style.use('fivethirtyeight')

frame_len = 10000

fig = plt.figure(figsize = (9,6))

def animate(i):
    data = pd.read_csv('sentiment.csv')
    y1 = data['Dogecoin']
    y2 = data['Bitcoin']

    if len(y1)<=frame_len:
        plt.cla()
        plt.plot(y1, label = 'Dogecoin')
        plt.plot(y2, label = 'Bitcoin')
    else:
        plt.cla()
        plt.plot(y1[-frame_len: ], label = 'Dogecoin')
        plt.plot(y2[-frame_len: ], label = 'Bitcoin')

    plt.legend(loc='upper left')
    plt.tight_layout()



    
ani = FuncAnimation(plt.gcf(), animate, interval = 1000)
plt.show()
