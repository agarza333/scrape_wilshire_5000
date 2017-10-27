
####################
##### Code #########
####################
### This code will find all the text values associated with anchor tags to links
### use this to test against the dictionary built of the stocks with avg vol < 3M


from bs4 import BeautifulSoup
import pprint
import urllib2
import re
import time

wilshires = []
def get_wilshire_stocks(url):
	check = True
	try:
		response = urllib2.urlopen(url)
		html = response.read()
	except urllib2.HTTPError as e:
		print e.code  # pur a continue statement in the loop here to try the next date
		check = False
		time.sleep(1)
	if check:
		soup = BeautifulSoup(html)
		for name in soup.find_all('tr'):
			for index, x in enumerate(name):
				if str(x) != ' ':
					if index%2 == 0:
						wilshires.append(str(x.contents[0].replace('\t', '')))
				else:
					pass

def prep_tickers(path):
	def filter_(index, name):
		if index%2 != 0:
			return name
		else:
			pass

	stocks = []
	quads = []
	with open(path, 'r') as f:
		quads = [line.strip().split('\t') for line in f]
		stocks = [filter_(index, name) for quad in quads for index, name in enumerate(quad)]
	stocks = filter(lambda x: x is not None, stocks)

	return stocks

path = 'your_path/data/stock_.txt'
stocker = prep_tickers(path)
print stocker
print len(stocker)
# url = 'http://financemainpage.com/Listing_of_All_Wilshire_5000_Stocks.html'
# get_wilshire_stocks(url)

write_path = 'your_path/data/wilshire_stocks.txt'
open(write_path, 'w').close()
with open(write_path, 'r+') as g:
	g.write(str(stocker))

