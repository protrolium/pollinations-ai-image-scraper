from bs4 import BeautifulSoup
import os
import urllib
import requests
import re
import sys

if len(sys.argv) < 2:
    sys.exit("href.py url output_dir")

url = sys.argv[1]
out_dir = sys.argv[2]

if not os.path.exists(out_dir):
    os.mkdir(out_dir)

req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
raw = []

print("The href links are :")
for link in soup.find_all('a'):
    #    original print statement
    #    print(link.get('href'))
    raw.append(link.get('href'))

# find only the lines that match the pattern:
# ipfs/QmS4L7oFXi2gJDua7RTEecUwXQ5JX7FHMtPbN7odA5AUix/output/00000.jpg
reg = re.compile(r'^.*?(output).*jpg$')
cleaned = list(filter(reg.search, raw))

# prepend the string 'https://ipfs.pollinations.ai/' to each list item
# ["https://ipfs.pollinations.ai/" + str(x) for x in cleaned]
full_url = [f'https://ipfs.pollinations.ai/{i}' for i in cleaned]

# print(fullURL)

# write links to list
with open('links.txt', 'w') as f:
    for row in full_url:
        f.write("%s\n" % str(row))

#save links to directory
for each in full_url:
	filename=each.split('/')[-1]
	urllib.request.urlretrieve(each, (os.path.join(out_dir,filename)))