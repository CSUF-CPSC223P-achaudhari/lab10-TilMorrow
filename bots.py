import threading
from time import sleep
import json

def bot_fetcher(items_list,cart_list,lock, /):
    invetory =[]
    with open("inventory.dat","rb") as file:
        inventory = json.load(file)

    for key in items_list:
        value = inventory[key]
        duration = value[1]
        item = value[0]
        sleep(duration)
        lock.acquire()
        cart_list.append([key, item])
        lock.release()


def bot_clerk(items_list,/):
    #cart_list = items_list
    bot0=[]
    bot1 = []
    bot2 = []
    cart_list = []
    lock = threading.Lock()
    for n, key in enumerate(items_list):
        botnum = n%3
        if botnum == 0:
            bot0.append(key)
        elif botnum == 1:
            bot1.append(key)
        elif botnum == 2:
            bot2.append(key)
            
    threads = []
    if len(bot0) > 0:
        t = threading.Thread(target = bot_fetcher, args = (bot0, cart_list, lock))
        t.start()
        threads.append(t)
    if len(bot1) > 0:
        t = threading.Thread(target = bot_fetcher, args = (bot1, cart_list, lock))
        t.start()
        threads.append(t)
    if len(bot2) > 0:
        t = threading.Thread(target = bot_fetcher, args = (bot2, cart_list, lock))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()
    return cart_list


