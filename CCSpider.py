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
import time
import requests
from bs4 import BeautifulSoup

def genHeaders (url) :
	host = url
	if url :
		match = re.compile (':\/\/(.*?com)')
		res = match.search(url)
		if res :
			host = res.group(1)
			
	headers = {
		'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.8',
		'Connection':'keep-alive',
		'Cookie':'UM_distinctid=15f437b4b97121-042a2340cadd34-31607c03-fa000-15f437b4b98a8; Hm_lvt_9a737a8572f89206db6e9c301695b55a=1508665672; CNZZDATA3866066=cnzz_eid%3D2085941068-1504442894-%26ntime%3D1504442894; CNZZDATA1263415983=1603382650-1509833581-null%7C1509833581',
		'Host': host,
		'If-Modified-Since':'Fri, 03 Nov 2017 13:28:46 GMT',
		'If-None-Match':"59fc6f0e-5d9",
		'Referer': url,
		'Upgrade-Insecure-Requests': '1',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
	}
	
	return headers
	
def genDownHeaders (url, site) :
	host = url
	if url :
		#match = re.compile (':\/\/(.*?com)')
		#match = re.compile (':\/\/(.*?55888)')
		match = re.compile (':\/\/(.*?me)')
		res = match.search(url)
		if res :
			host = res.group(1)

	print host
	headers = {
		'Accept':'image/webp,image/apng,image/*,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate',
		'Accept-Language':'en-US,en;q=0.8',
		'Connection':'keep-alive',
		'Cookie':'UM_distinctid=15f437b4b97121-042a2340cadd34-31607c03-fa000-15f437b4b98a8; Hm_lvt_9a737a8572f89206db6e9c301695b55a=1508665672; CNZZDATA3866066=cnzz_eid%3D2085941068-1504442894-%26ntime%3D1504442894; CNZZDATA1263415983=1603382650-1509833581-null%7C1509833581',
		'Host': host,
		'If-Modified-Since':'Fri, 03 Nov 2017 13:28:46 GMT',
		'If-None-Match':"59fc6f0e-5d9",
		#'Referer':url,
		'Referer':site,
		'Upgrade-Insecure-Requests': '1',
		'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
	}
	
	return headers

def getSite (url, rootdir) :
	headers = genHeaders(url)
	requests.Session()
	r = requests.get (url, headers = headers)
	r.encoding = r.apparent_encoding
	html = r.text

	soup = BeautifulSoup (html, 'html.parser')

	#<content id="content">
	#a class="post-title-link" 

	#content = soup.find("content", id="content").find_all("a")
	content = soup.find_all("a", attrs = {'class': 'post-title-link'})

	siteList = []
	for li in content :
		site = li['href']
		
		if site in siteList:
			continue
		else :
			siteList.append(site)
			
		print site
		
		download(site, rootdir)


def download (site, rootdir) :
	print site
	r = requests.get (site)
	r.encoding = r.apparent_encoding
	html = r.text
		
	soup = BeautifulSoup (html, 'html.parser')

	content = soup.find("content", id="content")
	img = content.find("img")
	#fenye = content.find(attrs={'class':'fenye'}).find('span')
	
	fenye = content.find('span', attrs={'class':'rw'})
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

		#print outURL
		
		#outURL = outURL.replace('img1', 'img2')
		#outURL = outURL.replace('me', 'com:55888')
		outURL = outURL.replace('com', 'me')
		print outURL
		
		#continue

		path = os.path.join (subpath, fileName)
		
		print path
		
		if os.path.exists (path) :
			print "The file has exists"
			continue
		
		headers = genDownHeaders(outURL, site)

		saveImge = requests.get(outURL, headers = headers)
		with open (path, "wb") as f:
			f.write (saveImge.content)
			f.close()
		
		time.sleep (0.5);

def genRootDir (rootdir) :	
	try :
		os.mkdir (rootdir)
	except:
		print "dir exists is OK!"

