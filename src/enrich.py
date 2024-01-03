
import json
import os
import xml.etree.ElementTree as ET
import re


search_results = json.load(open('search_results.json'))




count = 0
nolcc = 0

for rec in search_results['gathers']:
	count+=1
	print(count, nolcc)

	if 'oclc_num' in rec:

		if rec['oclc_num'] != None:

			# oclc = rec['oclc'][0]

			oclc = rec['oclc_num'].split(',')[0]

			if os.path.isfile('classify_by_oclc/'+oclc):

				oclc_text = open('classify_by_oclc/'+oclc).read()


				if '<response code="102"/>' not in oclc_text:

					

					element = ET.ElementTree(ET.fromstring(oclc_text)).getroot()



					e = element.find('{http://classify.oclc.org}recommendations/{http://classify.oclc.org}lcc/{http://classify.oclc.org}mostPopular')
					if e != None:


						rec['classify'] = e.attrib['sfa']


	filename = rec['catalog_url'].split('/')[-1] + '.json'
	# print(filename)
	if os.path.isfile('data/'+filename):

		marc = json.load(open('data/'+filename))
		
		for field in marc['fields']:

			if '050' in field:

				for subfield in field['050']['subfields']:
					if 'a' in subfield:
						rec['050a'] = subfield['a']


		for field in marc['fields']:

			if '090' in field:
				# print(field)
					for subfield in field['090']['subfields']:
						if 'a' in subfield:
							rec['090a'] = subfield['a']



	if 'lccn' in rec:
		if rec['lccn'] != None:
			lccn = rec['lccn']

			if ',' in lccn:
				lccn = lccn.split(',')[0]

			lccn = re.sub("[^0-9]", "", lccn)


			if os.path.isfile('lccn/'+lccn):

				with open('lccn/'+lccn) as infile:

					classval = infile.read().strip()

					rec['050a'] = classval


	if 'classify' not in rec:
		if '050a' not in rec:
			if '090a' not in rec:
				nolcc=nolcc+1



json.dump(search_results,open('search_results_enriched.json','w'),indent=2)

