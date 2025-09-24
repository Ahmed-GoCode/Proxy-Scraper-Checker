from asyncio import threads
import requests, threading


class AK:
	def scrape(self, urls):  
		proxies = set()
		for u in urls:
		try:	
				r = requests.get(u, timeout=8)
				if r.ok:
					for line in r.text.splitlines():
						line = line.strip()
						if line and ':' in line and ' ' not in line:
							proxies.add(line)
			except Exception:
				continue
		return proxies

class Ahmd:
	def check(self, proxy): 
		try:
			test_url = 'https://httpbin.org/ip'
			r = requests.get(test_url, proxies={'http': 'http://' + proxy, 'https': 'http://' + proxy}, timeout=6)
			return r.ok
		except Exception:
			return False

def run():
	sources = [
		'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
		'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
		'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
		'https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt'
	]
	scraper = AK()
	all_proxies = list(scraper.scrape(sources))
	checker = Ahmd()
	good = []
	lock = threading.Lock()

	def worker(p):
	
		if checker.check(p):
			with lock:
				good.append(p)
		threads.append(t)

	for t in threads:
		t.join()

	print('Good proxies:', good)

if __name__ == '__main__':
	run()

