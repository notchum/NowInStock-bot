import webbrowser
import requests
import bs4
import urllib
import newegg
import threading
import json
import re
from sys import platform
if platform == "linux" or platform == "linux2" or platform == "darwin": # Mac & Linux
    	import pygame 
elif platform == "win32":
    	import winsound
import counter
import time

class GpuBot:

	def __init__(self, filename):
		self.settings = json.load(open(filename))
		self.counter = counter.Counter(self.settings['counter'])
		self.threads, self.link_map = [], {}
		util.print_header("Settings:", json.dumps(self.settings, indent=2))

	def run(self):
		gpus_lst = [(gpu, use) for gpu, use in self.settings['gpus'].iteritems() if use]
		for gpu, use in gpus_lst[1:]:
			t = threading.Thread(target=self.monitor_loop, args=(gpu,))
			t.daemon=True
			t.start()
			self.threads.append(t)
		
		gc = threading.Thread(target=self.run_gc)
		gc.daemon=True
		gc.start()

		self.monitor_loop()

	def monitor_loop(self):
		while True:
			self.monitor()
			time.sleep(self.settings['check_interval_sec'])
	
	def monitor(self):
		soup = bs4.BeautifulSoup(urllib.urlopen("https://www.nowinstock.net/videogaming/consoles/sonyps5/"), 'html.parser')

		# <div id="data">
		# <table width="610">
		# 		<tr bgcolor="#CCCCCC">
		# 			<th id="nameh">Name</th>
		# 			<th width="90">Status<span style="vertical-align:super; font-size:8px;">1</span></th>
		# 			<th width="65">Last Price<span style="vertical-align:super; font-size:8px;">1</span></th>
		# 			<th width="100">Last Stock<span style="vertical-align:super; font-size:8px;">1</span></th>
		# 		</tr><tr id="tr29860" onMous.......
		trs = soup.find('table').find_all('tr')[1:] # strip the header tag
		trs = trs[0:len(trs)-1] # trim the last two for "item alerts via google groups" tag

		for found in [tr for tr in trs if "out of stock" not in tr.text.lower()]:
			link = found.find('a', attrs={'href': re.compile("^http")})
			# print 'link:', link
			if link is None:
				print('error, why couldnt we find a link:', found)
				continue
			
			# decode it
			link = urllib2.unquote(str(link.get('href')))
			if 'ebay' in link:
				continue # ignore the ebay links

			if self.is_new_link(link):
				self.dispatch_link(link)

	def is_new_link(self, link):
		if link not in self.link_map:
			self.link_map[link] = time.time()
			return True
		return False
		
	def run_gc(self):
		while True:
			for l, tt in self.link_map.items():
				if time.time() - tt > self.settings['gc_expire_sec']:
					print("expired link, removing:", l)
					del self.link_map[l]
			time.sleep(self.settings["gc_interval_sec"])

	def dispatch_link(self, link):
		domain = urlparse(link).hostname
		print(f"found ps5 --- url: {link}")
		self.counter.incr('domains', domain)
		# take action
		if 'walmart' in link:
			return			
		else:
			print('havent implemented', domain)

	def join(self):
		for t in self.threads:
			t.join()
