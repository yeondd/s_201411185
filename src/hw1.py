import urllib2
import re
from lxml import etree

response = urllib2.urlopen("http://python.org")
_html = response.read()

print "1. By regex"
p = re.compile('href="(http://.*?)"')
nodes = p.findall(_html)

print "Number of http url: ", len(nodes)
print ""
for i, node in enumerate(nodes):
	print i,":",node

print ""
print "2. By xpath"
htmlTree = etree.HTML(_html)
result = etree.tostring(htmlTree, pretty_print=True, method="html")

xnodes = htmlTree.xpath('//a[@href]')
print "Number of http url: ", len(xnodes)
print type(xnodes[0].attrib)
for i, node in enumerate(xnodes):
	print i,":",node.attrib
