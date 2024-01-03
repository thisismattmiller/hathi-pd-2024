
import json
import os
import xml.etree.ElementTree as ET
import re
import string
import unicodedata

def normalize_string(s):
    s = str(s)
    s = s.translate(str.maketrans('', '', string.punctuation))
    s = " ".join(s.split())
    s = s.lower()
    s = s.casefold()
    s = ''.join(c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn')
    s = s.replace('the','')
    return s

search_results = json.load(open('search_results_enriched.json'))




count = 0

for rec in search_results['gathers']:
	count+=1
	print(count)

	if 'oclc_num' in rec:

		if rec['oclc_num'] != None:

			# oclc = rec['oclc'][0]

			oclc = rec['oclc_num'].split(',')[0]

			if os.path.isfile('classify_by_oclc/'+oclc):

				oclc_text = open('classify_by_oclc/'+oclc).read()


				if '<response code="102"/>' not in oclc_text:

					

					element = ET.ElementTree(ET.fromstring(oclc_text)).getroot()


					

					e = element.find('{http://classify.oclc.org}work')
					print(e.attrib['editions'],e.attrib['eholdings'],e.attrib['holdings'],e.attrib['title'])
					
					rec['editions'] = int(e.attrib['editions'])
					rec['eholdings'] = int(e.attrib['eholdings'])
					rec['holdings'] = int(e.attrib['holdings'])
					rec['owi'] = int(e.attrib['owi'])
					# if e != None:


					# 	rec['classify'] = e.attrib['sfa']


count = 0
dedupe = {}

for rec in search_results['gathers']:
	count+=1
	print(count)
	if 'holdings' in rec:

		# combo = normalize_string(rec['title'] + rec['author'])
		owi = rec['owi']

		if owi not in dedupe:
			dedupe[owi] = []

		dedupe[owi].append(rec)


to_sort = {}

for o in dedupe:
	bigest = 0
	for rec in dedupe[o]:
		if rec['holdings'] > bigest:
			bigest = rec['holdings']
			to_sort[o] = {'holdings':bigest, 'recs':dedupe[o]}




by_holdings = sorted(to_sort,key=lambda x:to_sort[x]['holdings'], reverse=True)
by_holdings = by_holdings[0:1000]
by_holdings10k = sorted(to_sort,key=lambda x:to_sort[x]['holdings'], reverse=True)[0:10000]

sorted_by_holdings = []
for k in by_holdings:
	sorted_by_holdings.append(dedupe[k])

sorted_by_holdings10k = []
for k in by_holdings10k:
	sorted_by_holdings10k.append(dedupe[k])



json.dump(search_results,open('search_results_enriched.json','w'),indent=2)
json.dump(sorted_by_holdings,open('by_holdings.json','w'),indent=2)
json.dump(sorted_by_holdings10k,open('by_holdings10k.json','w'),indent=2)

