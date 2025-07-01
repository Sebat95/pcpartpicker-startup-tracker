import ctypes
import requests
import urllib3
from bs4 import BeautifulSoup
import datetime
import sys

# suppress the InsecureRequestWarning to allow "verify=false"
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


def get_value_from_website(url):
    # get current year for appropriate class
    class_name = f"td__price td__price-{datetime.datetime.now().year}"

    # simulate browser
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:139.0) Gecko/20100101 Firefox/139.0',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br, zstd',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'Priority': 'u=0, i'
    }
    try:
        # do not verify https since I cannot update CA on here
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()  # raise an HTTP errors

        soup = BeautifulSoup(response.text, 'html.parser')

        # get elements that hold prices in partpicker
        target_element = soup.find_all(class_=class_name)

        if target_element:
            # get the text of last element (the grand total) and strip whitespace
            return target_element[-1].get_text(strip=True)
        else:
            print(f"Element with class '{class_name}' not found")
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


if __name__ == "__main__":
    # modify the value in the script or pass it as first param
    website_url = "https://pcpartpicker.com/guide/Kwv6Mp" if len(sys.argv) <= 1 else sys.argv[1]

    # retrieve grand total
    price_value = get_value_from_website(website_url) or "ERROR"

    # open (windows) system popup
    ctypes.windll.user32.MessageBoxW(0, price_value, "The price now is:")
