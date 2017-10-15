import re
import os
import requests
from bs4 import BeautifulSoup

def getSite (url, rootdir) :
	r = requests.get (url)
	r.encoding = r.apparent_encoding
	html = r.text

	soup = BeautifulSoup (html, 'html.parser')

	#<content id="content">

	content = soup.find("content", id="content").find_all("a")
	#print content

	siteList = []
	for li in content :
		site = li['href']
		
		if site in siteList:
			continue
		else :
			siteList.append(site)
			
		#print site
		
		download(site, rootdir)


def download (site, rootdir) :
	print site
	r = requests.get (site)
	r.encoding = r.apparent_encoding
	html = r.text
		
	soup = BeautifulSoup (html, 'html.parser')

	content = soup.find("content", id="content")
	img = content.find("img")
	fenye = content.find(attrs={'class':'fenye'}).find('span')
	
	imgURL = img['src']
	
	print imgURL

	string = fenye.string
	
	numbers = re.findall("\d+", string)
	print numbers
	
	if len(numbers) != 2 :
		print "count error [!= 2]"
		return
	minNO = int (numbers[0])
	maxNO = int (numbers[1]) + 1
	
	subdir = re.findall (r'/(\d+)/', imgURL)[0]
	print subdir
	
	subpath = os.path.join(rootdir, subdir)
	try :
		os.mkdir (subpath)
	except:
		print "subdir exits"
	
	for i in range(minNO, maxNO) :
		rep =  "/" + str(i) + "."
		outURL = re.sub (r"/\d+\.", rep, imgURL)
		fileName = re.sub (r'.*\/', '', outURL)

		print outURL

		path = os.path.join (subpath, fileName)
		
		print path
		
		if os.path.exists (path) :
			print "The file has exists"
			continue
		
		saveImge = requests.get(outURL)
		with open (path, "wb") as f:
			f.write (saveImge.content)
			f.close()

def genRootDir (rootdir) :	
	try :
		os.mkdir (rootdir)
	except:
		print "dir exists is OK!"

