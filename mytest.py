import urllib3
from lxml import etree
import xml.etree.ElementTree as ET

http = urllib3.PoolManager()
r = http.request('GET', 'http://www.labs.skanetrafiken.se/v2.2/stationresults.asp?selPointFrKey=70011')
root = etree.fromstring(r.data)

print(r.data)

for Line in root.findall('Line'):
    no = Line.find('No').text
    name = Line.find('Name').text
    
    print(name, no)
    
