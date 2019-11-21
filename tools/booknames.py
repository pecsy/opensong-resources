#!/usr/bin/python
# coding: utf-8

from lxml import etree
from kitchen.text.converters import getwriter
import sys

if __name__ == '__main__':
    UTF8Writer = getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)

    root = etree.parse('/Users/gpecsy/Desktop/ufo.xml')

    books = root.xpath('//BIBLEBOOK')

    for book in books:
        name = book.get('bname')
        shortname = book.get('bsname')
        print( "BT(u'"+name+"', u'"+shortname+"'),")
