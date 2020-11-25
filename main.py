# from bot import GpuBot
from walbot import WalBot
import sys
import json
import time
import bs4
import re
import requests
from urllib.parse import urlparse

def monitor_loop():
	r = requests.get("https://www.nowinstock.net/videogaming/consoles/sonyps5/")
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

if __name__ == '__main__':
	# Check that there is a CLI arg
	if (len(sys.argv) != 2):
		print("Incorrect usage (no argument found)!\n\tUsage:   python xxx.py config.json")
		sys.exit(0)

	# Load the JSON file
	with open(sys.argv[1]) as f:
		personal_info = json.load(f)

	checkFlag = True
	while checkFlag:
		checkFlag = monitor_loop()
		time.sleep(2)
	
	# Run the walmart bot (to order)
	walbot = WalBot(**personal_info)
	
	# hopefully everything went well bye
	print("Goodbye.")
