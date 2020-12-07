# from bot import GpuBot
from walbot import WalBot
import sys
import json
import time
import bs4
import re
import requests
from urllib.parse import urlparse
if sys.platform == "win32":
    import winsound

nis_url = "https://www.nowinstock.net/videogaming/consoles/sonyps5/"
wal_url = "https://www.walmart.com/ip/Sony-PlayStation-5-Digital-Edition/493824815"

def monitor_loop():
	r = requests.get(wal_url)
	soup = bs4.BeautifulSoup(r.text, 'html.parser')

	trs = soup.find('table').find_all('tr')[1:] # strip the header tag
	trs = trs[0:len(trs)-1] # trim the last two for "item alerts via google groups" tag
	
	for found in [tr for tr in trs if "out of stock" not in tr.text.lower()]:
		link = found.find('a', attrs={'href': re.compile("^http")})
		# print 'link:', link
		if link is None:
			print('error, why couldnt we find a link:', found)
			continue
		
		# decode it
		link = urlparse(str(link.get('href')))
		if 'walmart' and 'Digital-Edition' in link.query:
			#walmart has stock!
			print(link.query)
			return False
	
	return True

def scrapeWalmart():
	print("Requesing the page...")
	page = requests.get(wal_url, headers = {"User-Agent":"Defined"})
	soup = bs4.BeautifulSoup(page.content, 'html.parser')
	product_info = soup.find(class_="prod-PriceSection").find_all('span')

	print("Formatting soup...")
	formatted_info = []
	for i in product_info:
		data = {
			'class': i['class'],
			'title': i.text
		}
		formatted_info.append(data)

	if ("Out of stock" in formatted_info[-1]['title']):
		print("------> Out of Stock.")
		return True
	else:
		return False

if __name__ == '__main__':
	# Check that there is a CLI arg
	if (len(sys.argv) != 2):
		print("Incorrect usage (no argument found)!\n\tUsage:   python xxx.py config.json")
		sys.exit(0)

	# Load the JSON file
	with open(sys.argv[1]) as f:
		personal_info = json.load(f)

	print('=========================================')
	print("         SCRAPING                ")
	print('=========================================')

	checkFlag = True
	while checkFlag:
		print("Scraping Walmart.com...")
		# checkFlag = monitor_loop()
		checkFlag = scrapeWalmart()
		time.sleep(5)
	
	# Ping 
	if (sys.platform == "win32"):
		winsound.PlaySound(sys.path[0] + '\\alarm.wav', winsound.SND_FILENAME)

	# Run the walmart bot (to order)
	walbot = WalBot(**personal_info)
	
	# hopefully everything went well bye
	print("Goodbye.")
