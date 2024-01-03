
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

search_results = json.load(open('combined_lists.json'))


count=0

for rec in search_results['titles']:
	count+=1
	print(count)
	subjects = []
	if 'oclc' in rec:

		if rec['oclc'] != None:

			# oclc = rec['oclc'][0]

			oclc = rec['oclc'][0]

			if os.path.isfile('classify_by_oclc/'+oclc):

				oclc_text = open('classify_by_oclc/'+oclc).read()


				if '<response code="102"/>' not in oclc_text:

					

					element = ET.ElementTree(ET.fromstring(oclc_text)).getroot()


					

					e = element.find('{http://classify.oclc.org}recommendations')
					if e == None:
						continue

					e = e.find('{http://classify.oclc.org}fast')
					if e == None:
						continue
					e = e.find('{http://classify.oclc.org}headings')
					if e == None:
						continue


					for sub in e.findall('{http://classify.oclc.org}heading'):
						print(sub.text)
						subjects.append(sub.text)


					# rec['editions'] = int(e.attrib['editions'])
					# rec['eholdings'] = int(e.attrib['eholdings'])
					# rec['holdings'] = int(e.attrib['holdings'])
					# rec['owi'] = int(e.attrib['owi'])
					# if e != None:


					# 	rec['classify'] = e.attrib['sfa']
					rec['subjects']=subjects


json.dump(search_results,open('combined_lists.json','w'),indent=2)