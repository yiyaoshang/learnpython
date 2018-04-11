import urllib
import urllib2

values = {"login":"wmbgsf302115","loginword":"ll010203"}
data = urllib.urlencode(values)
url = "http://e.meituan.com/"

request = urllib2.Request(url,data)
response = urllib2.urlopen(request)

print response.read()
