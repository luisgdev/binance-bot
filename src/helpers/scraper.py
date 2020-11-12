from requests.exceptions import ConnectionError, HTTPError, InvalidURL
from bs4 import BeautifulSoup
import requests


# Scrapping Telegram channel


def get_page(url):
    try:
        response = requests.get(url)
        print(f'Status Code: {response.status_code}')
    except ConnectionError:
        return 'ConnectionError'
    except HTTPError:
        return 'HTTPEror'
    except InvalidURL:
        return 'InvalidURL'
    except Exception as e:
        return f'Exception: {e}'
    else:
        return response


# Read certain post from a channel
def scrap(channel, post):
    channel_url = f'https://t.me/{channel}/{post}?embed=1'
    page = get_page(channel_url)
    if isinstance(page, str):
        return page
    else:
        page = page.text
    soup = BeautifulSoup(page, 'html5lib')
    # Scraping the target element
    msg = soup.find('div', attrs={'class':'tgme_widget_message_text js-message_text'})
    error = soup.find('div', attrs={'class':'tgme_widget_message_error'})
    # Verify
    if msg != None:
        return msg.text
    elif error != None:
        # 'Post not found'
        return error.text


# Get the last post number from a certain channel
def last_post_n(channel):
    channel_url = f'https://t.me/s/{channel}/'
    page = get_page(channel_url)
    if isinstance(page, str):
        return page
    else:
        page = page.text
    soup = BeautifulSoup(page, 'html5lib')
    # Scraping the target element
    history = soup.find_all('div', attrs={'class': 'tgme_widget_message force_userpic js-widget_message'})
    last_post = history[-2]['data-post']
    n_post = last_post.split('/')[1]
    print(f'Last post number: {n_post}')
    return n_post


def test():
    # https://t.me/Forex_Tradings/2960
    result = scrap('Forex_Tradings', 2960)
    print(f'RESULT: {result}')


if __name__ == "__main__":
    print('This is not main!')
    last_post_n('crypto_pump_island')