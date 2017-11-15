import urllib2
import json
kk = 'Chicago'
print type(kk)
url = 'https://api.foursquare.com/v2/venues/search?near='+kk+'&client_id=ZJI0H5P2ZLUB1FY2PZHQKI1Y40QCMRUDBZ1AYINMTJOPRUS5&client_secret=FPTTNGZNI3TYLS4QEC2RF2MTUOLJ101Y3F41ENHK0B54BGXA&v=20170101'

obj = urllib2.urlopen(url)

data = json.load(obj)

for i in data['response']['venues']:
	print i['name']
	break