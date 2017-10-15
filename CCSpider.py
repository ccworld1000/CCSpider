#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CCSpider.py
#  
#  Created by CC on 2017/10/12.
#  Copyright 2017 youhua deng (deng you hua | CC) <ccworld1000@gmail.com>
#  https://github.com/ccworld1000/CCSpider
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

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

