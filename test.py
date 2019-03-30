from threading import Thread
import time
from _actual_aside import AsidePrint
aside = AsidePrint()
aside.run()

for x in range(10):
    aside.append(x)

def threaded_adder(num):
    global aside
    for x in range(10):
        aside.append(f"Adder {num} added {x}")
        time.sleep(0.5)


adders = []
for x in range(5):
    adder = Thread(target=threaded_adder, args=(x, ))
    adders.append(adder)

for a in adders:
    a.start()

aside.append('Done')