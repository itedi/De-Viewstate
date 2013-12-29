#!/usr/bin/env python
import argparse
import urllib2
#import lxml.html wouldn't work :(
import HTMLParser 
banner = """
######################################
#        			     #
#	De-ViewState.py		     #
#	    			     #
#   -- By Henry Pitcairn	     #
######################################
"""

print banner # I MUST HAVE CREDIT!!!!!!

parser = argparse.ArgumentParser(description='Decode Viewstate.')
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-u', '--url', help='URL to page from which to grab ViewState')
group.add_argument('-i', '--input', help='Get input html from [file]')
parser.add_argument('-w', '--write', help='Write output to [file] (if none is specified output will be printed to the terminal window)', required=False)
parser.add_argument('-m', '--mode', help='Mode in which to ouput data: s[egmented] (output the data broken into parts) or r[aw] (output the data all in one chunk)  (default is segmented)', required=False)
args = parser.parse_args()

def segment(text, length):
    return [text[i:i+length] for i in range(0, len(text), length)]

def get_content(page_url):
	resp = urllib2.urlopen(page_url)
	data = resp.read()
	return data

def get_viewstate(html):
	i = html.index('id="__VIEWSTATE" value="')+24
	i2 = 0
	c_html = html[i:]
	for j in range(0,len(c_html)):
		if c_html[j] == '"':
			i2 = j
			break
	return c_html[:i2]

content = ''
if args.url:
	content = get_content(args.url)
elif args.input:
	f = open(args.input, 'r')
	content = f.read()
	f.close()
decoded = ''
viewstate = get_viewstate(content)
if viewstate == 'NOT_FOUND':
	print 'Viewstate not found in input!'
else:
	print "Found viewstate: "+viewstate
	if args.mode:
		if args.mode[0] == 'r':
			decoded = viewstate.decode('base64')
			print "Decoded: \n"+decoded
	else:
		segmented = segment(viewstate, 32)
		for seg in segmented:
			decoded += seg+';\t'+seg.decode('base64')+'\n'
			print seg+';\t'+seg.decode('base64')+'\n'
	if args.write:
		f = open(args.write, 'w')
		f.write(viewstate+'\n\n'+decoded)
		f.close()
print "Goodbye!"
