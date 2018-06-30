#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  CombienDeBises.py
#  
#  Copyright 2018 Samuel Hill <sam@huygens>
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

'''
This script will get a list of french départements and use this
information to scrape the data from combiendebises.com
'''

from bs4 import BeautifulSoup
import urllib.request, urllib.error, urllib.parse
import re

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

def departements():
	# Grab list of départements from the internet
	list_site = 'http://les-departements.fr/carte-des-departements.html'
	Request = urllib.request.Request(list_site, headers=hdr)
	Webpage = urllib.request.urlopen(Request).read().decode('utf-8')
	
	# Structure data and parse using beautiful soup
	soup = BeautifulSoup(Webpage, 'html.parser')
	
	# Find list containing département info
	liste = soup.find('ul', id='list-1')
	
	# Create convertion dictionary between département to code
	convert = {item.text.split(' - ')[1].strip(): item.text.split('-')[0].strip() for item in liste.findAll('li')}
	
	return convert

def bises(departement):
	# Now we have the codes, we can scrape the data from combiendebise.com
	biseSite = 'http://www.combiendebises.com/info.html?d={0}'
	BiseRequest = urllib.request.Request(biseSite.format(departement.upper()), headers=hdr)
	BisePage = urllib.request.urlopen(BiseRequest).read().decode('utf-8')
	soup = BeautifulSoup(BisePage, 'html.parser')
	ul = soup.find('ul')
	
	# Compile regex for extracting data
	matchstr = '(\d+)% des votants font (\d) bise'
	prog = re.compile(matchstr)
	
	# Iterate through all bises and saves results
	Bises = {}
	for item in ul.findAll('li')[:-3]:
		text = item.text
		result = prog.match(text)
		Bises[result.group(2)] = int(result.group(1))
	
	return Bises	

# Get list of departements
Departements = departements()
    
Info = {dep: bises(code) for dep, code in Departements.items()}
    
def main(args):
    # Get list of departements
    Departements = departements()
    
    Info = {dep: bises(code) for dep, code in Departements.items()}


if __name__ == '__main__':
	
