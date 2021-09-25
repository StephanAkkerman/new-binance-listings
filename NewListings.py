#!/usr/bin/python3
from binance import Client
import datetime     # Used for converting time to string
import requests     # Used for telegram messages
import threading    # Used for scheduling tasks not handled by the websocket
import math         # Used for calculating the precision for making orders
import time         # Used for time.sleep
import traceback    # Used for debugging

import binance_keys # Save API & Telegram keys here

bot_token = binance_keys.bot_token
send_to = binance_keys.send_to

# Max 1200 requests per minute (0.05 per second); 10 orders per second; 100,000 orders per 24hrs
# Binance API keys not necessary
client = Client()

def sendBuyAlert(bot_message : str):
    """ 
    Sends message via Telegram, using tokens specified in binance_keys.py 
    @param bot_messsage : string with the text message needed to be send
    """

    # Display message in console
    print(" ".join([bot_message, "at", datetime.datetime.now().strftime("%H:%M:%S")]))

    # Send message over Telegram
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + send_to + '&parse_mode=HTML&text=' + bot_message
    response = requests.get(send_text)

#This is necessary for newListings
oldSymbols = client.get_exchange_info().get("symbols")
    
def newListings():  
    """
    Checks if there a new listings and sends a message if there are
    """

    try:
        #Use the global oldSymbols
        global oldSymbols

        currentSymbols = client.get_exchange_info().get("symbols")
    
        # If symbols get removed, refresh oldSymbols
        if len(currentSymbols) < len(oldSymbols):
        
            #Refresh if symbols get deleted
            oldSymbols = client.get_exchange_info().get("symbols")

        # If there are new listings, currentLen will be larger
        # The new listings will always be at the end of the list of dicts
        if len(currentSymbols) > len(oldSymbols):     
            diff = len(currentSymbols) - len(oldSymbols)

            # Get the last new listings
            newSymbols = currentSymbols[-diff:]

            # Refresh oldSymbols so we wont get an infinite loop
            oldSymbols = client.get_exchange_info().get("symbols")

            # For all new symbols
            for syms in newSymbols:
                sym = (syms.get("symbol"))

                if "SPOT" in syms.get("permissions"): 
                    #Always send a message in case of a spot listing
                    sendBuyAlert("New SPOT Listing: " + sym)

        #Check every minute for changes
        threading.Timer(60, newListings).start()

    except Exception as e: 
        #Print out all the error information
        print(e)
        print(traceback.format_exc())

        #Wait 1 min before retrying
        print("retrying in 60 sec")
        time.sleep(60) 

        print("retrying...")

if __name__ == '__main__':
    print("Starting NewListings.py")
    newListings()