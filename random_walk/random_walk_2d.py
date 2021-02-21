import numpy as np 
import pylab 
import random 
n = 1000  # broj koraka
x = np.zeros(n)  # x i y su koordinate
y = np.zeros(n) 
direkcija=["y+","y-","x+","x-"]  # 4 smjera kretanja

for i in range(1, n):
    korak = random.choice(direkcija)  # Nasumicno odabiranje iz liste direkcija
    if korak == "x+":
        x[i] = x[i - 1] + 1  # trenutni korak = prethodni + pomak u nasumicnom smijeru
        y[i] = y[i - 1]
    elif korak == "x-":
        x[i] = x[i - 1] - 1
        y[i] = y[i - 1]
    elif korak == "y+":
        x[i] = x[i - 1]
        y[i] = y[i - 1] + 1
    else: 
        x[i] = x[i - 1]
        y[i] = y[i - 1] - 1

pylab.title("Random Walk 2-D")
pylab.plot(x, y)
pylab.show()