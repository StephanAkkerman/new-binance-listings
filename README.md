# New Binance Listings
As the name suggests this script sends you an automated message if Binance has just listed a new coin.

## Setup
Follow the link in src/binance_keys.py to set up your personal Telegram bot, and get your id token so you can send Telegram messages via your bot to yourself.

## How it works
Every minute (could be faster if you would like) the Binance exchange is checked, if the total amount of symbols listed on their exchange has changed compared to last time a message is send. This message contains the new symbols that got listed on the spot exchange.

## Dependencies
The required packages to run this code can be found in the `requirements.txt` file. To run this file, execute the following code block:
```
$ pip install -r requirements.txt 
```
Alternatively, you can install the required packages manually like this:
```
$ pip install <package>
```

## How to run
- Clone the repository
- Run `$ python src/main.py`
- See result

