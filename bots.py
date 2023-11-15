import threading
from time import sleep
import json
    #Takes in two positional arguments of items and cart list & lock
def bot_fetcher(items_list,cart_list,lock, /):
    inventory =[]
    with open("inventory.dat","rb") as file:
        inventory = json.load(file)
    # Looping through each item in the item list
    for key in items_list:
        value = inventory[key]
        duration = value[1] #Sleeps for the amount of time from items_list
        item = value[0]
        sleep(duration)
        lock.acquire()
        cart_list.append([key, item])
        lock.release()

    #Takes items_list as positional argument
def bot_clerk(items_list,/):
    # Separating the items that have been passed into 3 robot
    #fetcher lists
    #   Each bot clerk will have 3 bots
    bot0=[]
    bot1 = []
    bot2 = []
    cart_list = []  # Defining an empty list for cart list
    lock = threading.Lock()     # Defining a thread lock
    # ALgorithm to separate the items into the 3 bots that will fetch
    for n, key in enumerate(items_list):    #
        botnum = n%3
        if botnum == 0:
            bot0.append(key)
        elif botnum == 1:
            bot1.append(key)
        elif botnum == 2:
            bot2.append(key)
            
    # threads is created to gather all the bot fetchers going off
    #one at a time to be able to have them completely finish all
    #(using.join()) by the end to return cart_list from bot_fetcher
    threads = []
    # Each thread is going to bot_ftcher with the arguments given of
    #the items in the bot, a cart_list, and locked for each one to
    #go one at a time
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
# join() to complete all of the threading beforehand to return the 
#cart_list
    for t in threads:
        t.join()
    return cart_list


