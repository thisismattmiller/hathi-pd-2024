import json
from os.path import exists
import requests
import time
import re

from bs4 import BeautifulSoup


search_results = json.load(open('search_results_enriched.json'))
# search_results = json.load(open('search_results.json'))


count = 0
nolcc = 0
already_done = {}

for rec in search_results['gathers']:
	count+=1
	if 'classify' not in rec:
		if '050a' not in rec and '090a' not in rec:
			if 'lccn' in rec:
				if rec['lccn'] != None:
					lccn = rec['lccn']

					if ',' in lccn:
						lccn = lccn.split(',')[0]

					lccn = re.sub("[^0-9]", "", lccn)
					
					if lccn in already_done:
						continue

					if not exists('lccn/'+lccn):
						# lccn=lccn.split('/')[0]
						print(lccn)


						url = f"https://id.loc.gov/search/?q={lccn}&q=cs%3Ahttp%3A%2F%2Fid.loc.gov%2Fresources%2Finstances"
						r = requests.get(url)		
						soup = BeautifulSoup(r.text)

						links = soup.find_all('a',{'title':'Click to view record'})

						if len(links) == 1:


							idlink = links[0].get('href')

							idlink = 'https://id.loc.gov' + idlink + '.nt'
							r = requests.get(idlink)
							print(idlink)
							for line in r.text.split('\n'):
								if 'http://id.loc.gov/ontologies/bibframe/instanceOf' in line:


									workid = line.split('> <')[-1].split('>')[0] + '.nt'
									print(line)
									print(workid)

									if 'http://id.loc.gov/resources/works/' in workid:

										r = requests.get(workid)
										for line in r.text.split('\n'):
											if 'http://id.loc.gov/ontologies/bibframe/classificationPortion' in line:

												lcc = line.split('"')[1].split('"')[0]
												print(lcc)

												with open('lccn/'+lccn,'w') as outfile:
													outfile.write(lcc)

												break


									break

							

						already_done[lccn] = True


						# time.sleep(6)
						# with open('lccn/'+lccn,'w') as out:

						# 	out.write(r.text)
						# 	time.sleep(1)
							




