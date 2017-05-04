#!/usr/bin/env python

from sys import argv
from os import makedirs, unlink, sep
from os.path import dirname, exists, isdir, splitext
from string import replace, find, lower
from htmllib import HTMLParser    #
from urllib import urlretrieve
from urllib.parse import urlparse, urljoin
from formatter import DumbWriter, AbstractFormatter
from cStringIO import StringIO    #

class Retriever(object):# download Web pages
    
    def __init__(self, url):
        self.url = url
        self.file = self.filename(url)

    def filename(self, url, deffile='index.htm'):
        parsedurl = urlparse(url, 'http:', 0)
        path = parsedurl[1] + parsedurl[2]
        ext = splitext(path)
        if ext[1] == '':
            if path[-1] == '/':
                path += deffile
            else:
                path += '/' + deffile
        ldir = dirname(path)
        if sep != '/':
            ldir = repalce(ldir, '/', sep)
        if not isdir(ldir):
            if exists(ldir): unlink(ldir)
            makedirs(ldir)
        return(path)

    def download(self):

        try:
            retval = urlretrieve(self.url, self.file)
        except IOError:
            retval = ('*** ERROR: invalid URL "%s"' % self.url)
        return retval
    
    def passAndGetLink(self):
        self.parse = HTMLParser(AbstractFormatter(Dumbwriter(StringIO())))
        self.parse.feed(open(self.file).read())
        self.parse.close()
        return self.parser.anchorlist