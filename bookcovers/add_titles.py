import json
import shutil
from PIL import Image, ImageDraw, ImageFont
import os
import re


data = json.load(open('../combined_lists.json'))
count = 0

for rec in data['titles']:
	count=count+1

	print(rec['owi'], "|")




	title = rec['title']

	title = title.replace('...','')
	title = title.strip()


	if '/' in title:
		title = title.split('/')[0]

	if '.' in title and 'Mr.' not in title and 'Mrs.' not in title:
		title = title.split('.')[0]

	if ',' in title:
		title = title.split(',')[0]







	title_author = rec['author']

	# print(titles)

	touse = title
	if len(touse) < 5:

		touse = rec['title']



	if touse[-1] == ',' or touse[-1] == ';':
		touse = touse[0:-1]
	print(touse)

	touse_org = touse

	filename = f'covers/{rec["owi"]}.jpg'
	multiline = False
	if len(touse) > 75:
		touse = touse.split(" ")
		multiline = True

		mid = int(len(touse)/2)


		touse1 = " ".join(touse[0:mid]) 
		touse2 = " ".join(touse[mid:])

	if os.path.isfile(filename):


		im = Image.open(filename)
		im = im.convert("RGBA")
		


		
		font_filename = "/Users/m/Downloads/Noto_sans/static/NotoSans-SemiBold.ttf"

		if len(re.findall(r'[\u0627-\u064a]',touse_org)) > 0:
			font_filename = "/Users/m/Downloads/Noto_Sans_Arabic/static/NotoSansArabic-SemiBold.ttf"



		add_author = False
		touse_author = ''
		if rec['author'] != None:
				
			if len(rec['author'].strip()) != 0:
				add_author=True
				asplit = rec['author'].split(",")
				if len(asplit) > 0:
					touse_author = asplit[0]
				else:
					touse_author = rec['author']

			print(add_author,"!!!!!!!",touse_author)
		



		# 
		# print(im.size)



		TINT_COLOR = (0, 0, 0)  # Black
		TRANSPARENCY = .50  # Degree of transparency, 0-100%
		OPACITY = int(255 * TRANSPARENCY)

		overlay = Image.new('RGBA', im.size, TINT_COLOR+(0,))
		overlay_draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
		overlay_draw.rectangle(((0,700), (1024,900)), fill=TINT_COLOR+(OPACITY,))
		img = Image.alpha_composite(im, overlay)
		# img = img.convert("RGB") # Remove alpha for saving in jpg format.
		
		draw = ImageDraw.Draw(img)

		if multiline == False:

			x = 0
			y = 0
			old_x = 0 
			old_y = 0
			fontsize = 16
			while x < 900 and y < 200:
					
				old_x = x
				old_y = y

				font = ImageFont.truetype(font_filename, fontsize)
				text_length = draw.textlength(touse, font=font)
				bbox = draw.textbbox((0,0), touse, font=font)



				x = bbox[2]
				y = bbox[3]

				fontsize=fontsize+1

			draw.text((1024/2,800), touse, anchor='mm', fill="white", font=font)


		else:

			x = 0
			y = 0
			old_x = 0 
			old_y = 0
			fontsize = 16
			while x < 900 and y < 100:
					
				old_x = x
				old_y = y

				font = ImageFont.truetype(font_filename, fontsize)
				text_length = draw.textlength(touse1, font=font)
				bbox = draw.textbbox((0,0), touse1, font=font)



				x = bbox[2]
				y = bbox[3]

				fontsize=fontsize+1
	

			lineone_height = old_y
			draw.text((1024/2,750), touse1, anchor='mm', fill="white", font=font)
			
			x = 0
			y = 0
			old_x = 0 
			old_y = 0
			fontsize = 16

			while x < 900 and y < 100:
					
				old_x = x
				old_y = y

				font = ImageFont.truetype(font_filename, fontsize)
				text_length = draw.textlength(touse2, font=font)
				bbox = draw.textbbox((0,0), touse2, font=font)



				x = bbox[2]
				y = bbox[3]

				fontsize=fontsize+1
	





			draw.text((1024/2,755 + lineone_height), touse2, anchor='mm', fill="white", font=font)

		if add_author == True:


			font = ImageFont.truetype(font_filename, 58)
			bbox = draw.textbbox((0,0), touse_author, font=font)
			print(bbox)
			author_text_length = bbox[2]
			center = (1024 / 2) - (author_text_length / 2)
			center_text = center + (author_text_length / 2)
			print("center",center)
			overlay = Image.new('RGBA', im.size, TINT_COLOR+(0,))
			overlay_draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
			overlay_draw.rectangle(((center-10,901), (center+author_text_length+10,950)), fill=TINT_COLOR+(OPACITY,))
			img = Image.alpha_composite(img, overlay)
			draw = ImageDraw.Draw(img)
			draw.text((center_text,925), touse_author, anchor='mm', fill="white", font=font)

		img = img.convert("RGB") # Remove alpha for saving in jpg format.
		img.save(filename.replace('covers/','covers/withtext/'))











# print(image_url)