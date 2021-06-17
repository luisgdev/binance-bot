import re
#from helpers import scraper
# Pylance doesn't recognize helpers module on prev sentence.
# import helpers.scraper as scraper
import scraper

# Words to ignore: result, proof, hit, missed, warning


def find_symbol(text):
    pat_list = [
        r'[#$][a-zA-Z]{3,5}\s',
        r'[A-Z]{2,5}/BTC\s',
        r'[A-Z]{3,5}\s'
    ]
    for pat in pat_list:
        match = re.search(pat, text, flags=0)
        if match:
            coin = re.search(pat, text, flags=0).group()
            return coin
    return None


# https://t.me/crypto_pump_island/26677


def test():
    msg = scraper.scrap('crypto_pump_island', 26678)
    if msg:
        res = find_symbol(msg)
        if res:
            res = res.replace('#', '').replace('$', '').replace('/BTC', '')
            print(f'Coin found: {res}')
        else:
            print(f'No coin found: {res}')
    else:
        print('No text found in post!')

if __name__ == '__main__':
    test()
