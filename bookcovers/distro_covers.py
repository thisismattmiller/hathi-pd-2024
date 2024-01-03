import json
import shutil
from PIL import Image, ImageDraw, ImageFont
import os
import re
import csv

outfile = open('images_meta.csv','w')
writer = csv.writer(outfile)

data = json.load(open('../combined_lists.json'))
count = 0


writer.writerow(['hathi','title','author','oclc','lccn'])

for rec in data['titles']:
	count=count+1

	print(rec['owi'], "|")
	owi = rec['owi']
	hathi_id = rec['main_bib_id']


	shutil.copyfile(f"covers/withtext/{owi}.jpg", f"images/{hathi_id}.jpg")

	shutil.copyfile(f"covers/{owi}.jpg", f"images_no_text/{hathi_id}.jpg")


	writer.writerow([hathi_id,rec['title'],rec['author'],"|".join(rec['oclc']),rec['lccn']])


outfile.close()



# print(image_url)