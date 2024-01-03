import json
from os.path import exists


oneK = json.load(open('top_1000.json'))
tenK = json.load(open('top_10k.json'))

allTitles = {
	
}
data = {
	"top1000AllSubjects": oneK['subjects'],
	"top2000LitSubjects": tenK['subjects'],
}

belong_in_list = {}

for rec in oneK['titles']:

	if rec['main_bib_id'] not in belong_in_list:
		belong_in_list[rec['main_bib_id']] = []
	belong_in_list[rec['main_bib_id']].append('1kAll')

	if isinstance(rec['lccn'], str):
		rec['lccn'] = rec['lccn'].split(",")
	allTitles[rec['main_bib_id']] = rec


for rec in tenK['titles']:
	if rec['main_bib_id'] not in belong_in_list:
		belong_in_list[rec['main_bib_id']] = []

	belong_in_list[rec['main_bib_id']].append('2kLit')
	if isinstance(rec['lccn'], str):
		rec['lccn'] = rec['lccn'].split(",")
	allTitles[rec['main_bib_id']] = rec


allTitlesList = []
for rec in allTitles:


	allTitles[rec]['lists'] = belong_in_list[rec]
	allTitlesList.append(allTitles[rec])



allTitlesSorted = sorted(allTitlesList, key=lambda d: d['holdings'], reverse=True) 



data['titles'] = allTitlesSorted

json.dump(data,open('combined_lists.json','w'),indent=2)