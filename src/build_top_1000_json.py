import json
import re
from collections import Counter

hierarchy = {
  'A':{'code':'A', 'subject':'General Works','count':0,'children':{}},
  'B':{'code':'B', 'subject':'Philosophy, Psychology, Religion','count':0,'children':{}},
  'C':{'code':'C', 'subject':'Auxiliary Sciences of History (General)','count':0,'children':{}},
  'D':{'code':'D', 'subject':'World History (except American History)','count':0,'children':{}},
  'E':{'code':'E', 'subject':'American History','count':0,'children':{}},
  'F':{'code':'F', 'subject':'Local History of the United States and British, Dutch, French, and Latin America','count':0,'children':{}},
  'G':{'code':'G', 'subject':'Geography, Anthropology, Recreation','count':0,'children':{}},
  'H':{'code':'H', 'subject':'Social Sciences','count':0,'children':{}},
  'J':{'code':'J', 'subject':'Political Science','count':0,'children':{}},
  'K':{'code':'K', 'subject':'Law','count':0,'children':{}},
  'L':{'code':'L', 'subject':'Education','count':0,'children':{}},
  'M':{'code':'M', 'subject':'Music','count':0,'children':{}},
  'N':{'code':'N', 'subject':'Fine Arts','count':0,'children':{}},
  'P':{'code':'P', 'subject':'Language and Literature','count':0,'children':{}},
  'Q':{'code':'Q', 'subject':'Science','count':0,'children':{}},
  'R':{'code':'R', 'subject':'Medicine','count':0,'children':{}},
  'S':{'code':'S', 'subject':'Agriculture','count':0,'children':{}},
  'T':{'code':'T', 'subject':'Technology','count':0,'children':{}},
  'U':{'code':'U', 'subject':'Military Science','count':0,'children':{}},
  'V':{'code':'V', 'subject':'Naval Science','count':0,'children':{}},
  'Z':{'code':'Z', 'subject':'Bibliography, Library Science','count':0,'children':{}}
}



by_holdings = json.load(open('by_holdings.json'))
# by_holdings = json.load(open('by_holdings10k.json'))

lcc_data = json.load(open('lcc.json'))
lcc = re.compile(r'([A-Z]+)([0-9]+)')

all_subjects =[]
all_subjects_count={}
all_data =[]
for rec_group in by_holdings:

	if 'classify' not in rec_group[0]:
		continue

	lcc_class = rec_group[0]['classify']

	subject = 'Unknown'
	c = lcc_class.split('.')[0]
	cl = lcc.search(c)
	if cl != None:
		
		alpha = cl.group(1)
		num = int(cl.group(2))

		if alpha in lcc_data:
			for a in lcc_data[alpha]:

				if num >= a['start'] and num <= a['stop']:
					if len(a['parents']) > 0:
						
						for b in lcc_data[alpha]:

							if b['id'] == a['parents'][0]:
								subject = b['subject']
								break

					else:
						
						subject = a['subject']

	subject = re.sub(r'\s+',' ',subject)
	# if subject != 'English' and 'literature' not in subject.lower():
	# 	continue

	all_subjects.append(subject)

	data = {
		'main_bib_id': rec_group[0]['ht_bib_key'],
		'oclc':[],
		'lccn':[],
		'issn':[],
		'description':{},
		'title': rec_group[0]['title'],
		'author': rec_group[0]['author'],
		'imprint': rec_group[0]['imprint'],
		'holdings':rec_group[0]['holdings'],
		'owi': rec_group[0]['owi']


	}
	if data['author'] == '':
		data['author'] = None
	if data['imprint'] == '':
		data['imprint'] = None

	lang = {}
	for rec in rec_group:

		if rec['lang'] not in lang:
			lang[rec['lang']] = []

		lang[rec['lang']].append(rec['ht_bib_key'])
		lang[rec['lang']] = list(set(lang[rec['lang']]))

		if rec['description'] != '':
			if rec['description'] not in data['description']:
				data['description'][rec['description']] = []

			data['description'][rec['description']].append(rec['ht_bib_key'])

			data['description'][rec['description']] = list(set(data['description'][rec['description']]))

		if ',' in rec['oclc_num']:
			data['oclc'] = data['oclc'] + rec['oclc_num'].split(",")
		elif rec['oclc_num'] != '':
			data['oclc'].append(rec['oclc_num'])

		if rec['issn'] != None and rec['issn'] != "":
			if ',' in rec['issn']:
				data['issn'] = data['issn'] + rec['issn'].split(",")
			elif rec['issn'] != '':
				data['issn'].append(rec['issn'])

		if rec['issn'] != None and rec['issn'] != "":
			data['lccn'] = rec['lccn']

	data['oclc'] = list(set(data['oclc']))
	data['lang'] = lang

	data['subject'] = subject
	all_data.append(data)

subjects = dict(Counter(all_subjects))
subjects = dict(sorted(subjects.items(), key=lambda item: item[1], reverse=True))

json.dump({'subjects':subjects,'titles':all_data}, open('top_1000.json','w'),indent=2)
# json.dump({'subjects':subjects,'titles':all_data}, open('top_10k.json','w'),indent=2)

# print(len(list(set(all_subjects))))
# print(Counter(all_subjects))