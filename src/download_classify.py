import json
import shutil
import requests
import os


WSkey = 'YOUR_KEY_HERE'

headers = {'X-OCLC-API-Key': WSkey}

search_results = json.load(open('search_results.json'))

counter = 0
unique_oclc = []
total = len(search_results['gathers'])
for rec in search_results['gathers']:

	if 'oclc_num' in rec:

		if rec['oclc_num'] != None:

			rec['oclc_num'] = rec['oclc_num'].split(',')
			# if isinstance(rec['oclc_num'], list):
			unique_oclc = unique_oclc + rec['oclc_num']
			# elif isinstance(rec['oclc_num'], str):
				# unique_oclc.append(rec['oclc_num'])

			# if len(unique_oclc) >= 100:

			# 	break


unique_oclc = list(set(unique_oclc))

print(len(unique_oclc))

count= 0

for oclc in unique_oclc:

	if os.path.isfile('classify_by_oclc/'+oclc):
		print('skipp ',oclc)
		continue
	count+=1

	try:
		print(count,'/',len(unique_oclc))
		payload = {'oclc':oclc}
		response = requests.get('https://metadata.api.oclc.org/classify/', params=payload, headers=headers)
		with open('classify_by_oclc/'+oclc, 'w') as out:
			out.write(response.text)
	except:

		print("Error with this one",oclc)

# dupe_check = {}
# no_oclc = []
# unique = []
# with open('/Users/m/data/hathi_full_20210101_pd.txt') as infile:
# 	reader = csv.reader(infile, delimiter="\t",quoting=csv.QUOTE_NONE)
# 	for l in reader:
# 		if l[7] != '':
# 			if l[7] not in dupe_check:
# 				dupe_check[l[7]] = True
# 				unique.append(l)


# 		else:
# 			no_oclc.append(l)
# 			unique.append(l)

# print(len(unique))
# print(len(no_oclc))

# count = 0
# for r in unique:

# 	htid = r[0].replace(':','').replace('/','')
# 	url = f"https://babel.hathitrust.org/cgi/imgsrv/image?id={htid};width=400"

# 	if os.path.isfile('/Users/m/data/hathi_1925_pd_metadata/'+htid):
# 		print('skipp ',htid)
# 		continue
# 	count+=1
# 	print(count,'/',len(unique))
# 	if r[7] != '':
		
# 		o = r[7].split(',')[0]

# 		payload = {'oclc':o}
# 		response = requests.get('http://classify.oclc.org/classify2/Classify', params=payload)
# 		with open('/Users/m/data/hathi_1925_pd_metadata/'+htid, 'w') as out:
# 			out.write(response.text)



# 	else:

# 		author = r[25]
# 		title = r[11]
# 		payload = {'author':author[0:49], 'title':title[0:49]}
# 		response = requests.get('http://classify.oclc.org/classify2/Classify', params=payload)
# 		with open('/Users/m/data/hathi_1925_pd_metadata/'+htid, 'w') as out:
# 			out.write(response.text)
