
from bs4 import BeautifulSoup
from urllib.error import URLError
from urllib.request import urlopen
import time
import argparse


class Wilshire_Stocks(object):

    def __init__(self, url, output_path):
        self.wilshires = []
        self.url = url
        self.output_path = output_path

    def get_wilshire_stocks(self):
        check = True
        try:
            response = urlopen(self.url)
            html = response.read()
        except URLError as e:
            print(e.code)
            check = False
            time.sleep(1)
        if check:
            soup = BeautifulSoup(html, "lxml")
            for name in soup.find_all('tr'):
                for index, x in enumerate(name):
                    if str(x) != ' ':
                        if index % 2 == 0:
                            self.wilshires.append(
                                str(x.contents[0].replace('\t', '')))
                    else:
                        pass

    def prep_tickers(self, path):
        def filter_(index, name):
            if index % 2 != 0:
                return name
            else:
                pass

        stocks = []
        quads = []
        with open(path, 'r') as f:
            quads = [line.strip().split('\t') for line in f]
            stocks = [filter_(index, name)
                      for quad in quads for index, name in enumerate(quad)]
        stocks = filter(lambda x: x is not None, stocks)

        return stocks

    def write_to_path(self, stocks):
        open(self.output_path, 'w').close()
        with open(self.output_path, 'r+') as g:
            g.write(str(stocks))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--OUTPUT_PATH',
        required=True,
        help='Please type a string for the path where to output (i.e. "Your_Path/write/" )')

    args = parser.parse_args()
    url = 'http://financemainpage.com/Listing_of_All_Wilshire_5000_Stocks.html'
    ws = Wilshire_Stocks(url, args.OUTPUT_PATH)
    ws.get_wilshire_stocks()
    ws.write_to_path(ws.wilshires)
