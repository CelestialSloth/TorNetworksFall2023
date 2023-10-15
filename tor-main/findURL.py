#!/usr/bin/python3
from bs4 import BeautifulSoup
from sys import argv

def main() -> str:
    """
    Returns end of URL to unique_Tor so they can download IP to AS mappings from caida.

    Uses BeautifulSoup to find correct url from CAIDA which varies depending on time the
    data was collected. Used to find link to download the first set of data on the first 
    month for a certain year/month pair from CAIDA website. Reads url saved from unique_Tor
    into html_file
    
    Returns: 
        A string of the found end of a url
    """
    try:
        with open("html_file") as f:
            soup = BeautifulSoup(f, 'html.parser')
    except (OSError, IOError):
        print("Could not open html_file in findURL.py")
        exit(1)

    #print(soup.find_all('a'))
    download_link = soup.find_all('a')[5].get('href')
    print(download_link)

    return download_link

if __name__ == '__main__':
    main()
