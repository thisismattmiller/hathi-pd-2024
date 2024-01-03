from openai import OpenAI
client = OpenAI()
import json
import shutil
import requests
import os
import random


data = json.load(open('../combined_lists.json'))
count = 0

for rec in data['titles']:

  count=count+1
  owi = rec['owi']
  print(owi, "|")

  title = rec['title']

  title = title.replace('...','')
  title = title.strip()


  if '/' in title:
    title = title.split('/')[0]

  if '.' in title and 'Mr.' not in title and 'Mrs.' not in title:
    title = title.split('.')[0]

  if ',' in title:
    title = title.split(',')[0]





  touse = title
  if len(touse) < 5:

    touse = rec['title']

  print(touse)


  filename = f'covers/{owi}.jpg'

  if os.path.isfile(filename):
    continue


  # if count > 200:
  #   break

  touse = touse.replace("'",'')

  if touse == 'The history of Don Quixote de La Mancha':
    touse = 'A Knight fighting windmills'
    


  if touse == 'The case book of Sherlock Holmes':
    touse = 'The case book of a London detective'


  if touse == 'The confessions of an English opium-eater':
    touse = 'The confessions of an English poppy-eater'
  if touse == 'Isis':
    touse = 'history of science, history of medicine, and the history of technology, as well as their cultural influences'

  if touse == 'The noble savage : a study in romantic naturalism':
    touse = 'The human : a study in naturalism'

  if touse == 'The one-act plays of Luigi Pirandello':
    touse = 'The one-act plays of L Pirandello'

  if touse == 'The strange Vanguard; a fantasia':
    touse = 'The strange Vanguard;'

  if touse == 'Phonophotography in folk music; American negro songs in new notation':
    touse = 'Phonophotography in folk music; American American songs in new notation'

  if touse == 'Teresa of Watling street; a fantasia on modern themes':
    touse = 'Teresa of Watling street; a story on modern themes'

  if touse == 'A splendid gypsy: John Drew':
    touse = 'A splendid Romany: John Drew'

  if touse == 'Mario Donadieu':
    touse = 'A story about Donadieu in paris, tinged with individualism inspired by Nietzsche'
    rec['author'] = ""

  if touse == 'Philippe Quinault; sa vie':
    touse = 'Quinault; sa vie'



  
  prompt=f"A old 1920's book textless illustration inspired by the title '{touse}' by {rec['author']} the illustration has no words or text shown."
  
  prompt = prompt.replace('Luigi', "L")

  prompt = prompt.replace('Mario', "Mr")





  print(prompt)

  try:
    response = client.images.generate(
      model="dall-e-3",
      # prompt="A book cover illustration for the book 'The essayes of Michael, lord of Montaigne, translated into English by John Florio and with an introduction by Desmond MacCarthy'. Do not include any text in the image.",
      prompt=prompt,
      size="1024x1024",
      quality="standard",
      n=1,
    )
  except KeyboardInterrupt: # Breaking here so the program can end
    xxxx=xxx

  except Exception as e: 

    print("ERROR ON THIS ONE:",prompt)
    print(e)

  

  image_url = response.data[0].url
  response = requests.get(image_url, stream=True)
  with open(filename, 'wb') as out_file:
    shutil.copyfileobj(response.raw, out_file)
  del response

  # break

# print(image_url)