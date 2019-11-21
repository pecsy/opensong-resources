#!/usr/bin/python
# coding: utf-8

from lxml import html
import requests
import sys
import model
from kitchen.text.converters import getwriter
import re
from xml.etree.ElementTree import tostring

from model import Bible
from zefania import exportToZefaniaXML

base_url = 'http://abibliamindenkie.hu/'

def loadDOM(session, url):
    response = session.get(url)
    if response.status_code == 200:
        print('Loaded {0} successfully'.format(url))
    else:
        print('Failed to load {0}. Status: {1}'.format(url, response.status_code))
        return None
    response.encoding = 'utf-8'
    dom = html.fromstring(response.content)
    return dom

def getNodeText(node):
    text = node.xpath('text()')
    text = map(lambda s: s.strip(), text)
    text = filter(lambda s: len(s)>0,text)
    return " ".join(text)

def parseChapter(session, chapter):
    dom = loadDOM(session, chapter.url)
    vnodes = dom.xpath('//p[@id]')
    vnodes = filter(lambda n: re.match("v[0-9]+",n.get("id")),vnodes)
    verses = map(getNodeText, vnodes )
    verses = filter(lambda s: (len(s)>0),verses)
    for verse in verses:
        chapter.addVerse(verse)
    return chapter


def parseBook(session, book):
    dom = loadDOM(session, book.url)
    urls = dom.xpath('//div[@class="book-content"]//a/@href')
    summaries = dom.xpath('//div[@class="book-content"]//span[@class="chapter-title-list"]')
    for i in range(0, len(urls)):
        si = summaries[i]
        summary = si.xpath('span/text()')
        chapter  = model.Chapter(base_url+urls[i],summary)
        book.addChapter(chapter)

    for c in book.chapters:
        parseChapter(session,c)

    return book


def parseBible(session, url):
    tree = loadDOM(session, url)
    titles = tree.xpath('//div[@class="edition-content"]//a[@href]/text()')
    urls = tree.xpath('//div[@class="edition-content"]//a/@href')
    bible = model.Bible(u'Magyar Revideált Új fordítás', url)  # type: Bible
    for i in range(0, len(titles)):
        book = model.Book(titles[i],url+urls[i])
        bible.addBook(book)

    for b in bible.books:
        parseBook(session,b)

    return bible


def testParseBook(session):
    bible = model.Bible('Revidealt uj forditas', base_url)
    book = model.Book('Mozes elso konyve', 'https://abibliamindenkie.hu//uj/GEN/' )
    parseBook(session,book);

    print( book.title + " @ " + book.url )
    for c in book.chapters:
        print( c.url )
        for l in c.summary:
            print('   * ' + l)

    for v in book.chapters[0].verses:
        print(str(v.number)+": " + v.text)


    bible.addBook(book)
    return bible


def saveToFile(fname, xml):
    f = open(fname, "w")
    f.write(xml)
    f.close()


if __name__ == '__main__':
    UTF8Writer = getwriter('utf8')
    sys.stdout = UTF8Writer(sys.stdout)

    session = requests.Session()
 #   bible = testParseBook(session)
 #   fname = 'genezis.xml'
    bible = parseBible(session,base_url)
    fname = 'revufo.xml'
    zefaniaDom = exportToZefaniaXML(bible)
    saveToFile(fname,tostring(zefaniaDom,'UTF-8'))
