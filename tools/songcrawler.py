#!/usr/bin/python3
# coding: utf-8

from lxml import html
import requests
from xml.etree.ElementTree import tostring
from songmodel import Song
import singleversesongs

base_url = 'https://enekeskonyv.reformatus.hu'


def load_dom(session, url):
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


def saveToFile(fname, xml):
    f = open(fname, "w")
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    f.write(xml)
    f.close()


def load_song_list(session, base_url):
    dom = load_dom(session,base_url+'/digitalis-reformatus-enekeskonyv/')
    res = []
    # /html/body/main/article/section/div/table/tbody/tr[2]/td[1]
    indices = dom.xpath('//div[@class="block__content"]//tr/td[1]/text()')
    print(len(indices), indices)
    titles = dom.xpath('//div[@class="block__content"]//p[@class="post__song-title"]//a[@href]/text()')
    print(len(titles), titles)
    urls = dom.xpath('//div[@class="block__content"]//p[@class="post__song-title"]//a/@href')
    print(len(urls), urls)
    assert len(indices) == len(titles)
    assert len(titles) == len(indices)
    for i in range(len(indices)):
        s = Song(int(indices[i]), titles[i], base_url+urls[i])
        res.append(s)

    return res


def load_song(session, s):
    dom = load_dom(session,s.url)
    # /html/body/main/article/div/section[1]/div/div/h3

    verses = dom.xpath('//div[@class=\"block__content\"]//ol/li')
    if len(verses)<1:
        print('{}. {} is empty'.format(s.index, s.title))
        s.add_verse(1, singleversesongs.song[s.index])
        return s

    for index in range(len(verses)):
        vtext = verses[index].xpath('.//text()')
        lines = []
        for l in vtext:
            for line in l.split(' / '):
                lines.append(line.strip())
        s.add_verse(index+1,lines)

    return s



def load_songs(session, songs):
    for s in songs:
        load_song(session,s)


def save_songs_to_file(songs, target_dir):
    for s in songs:
        fn = '{}/{}'.format(target_dir, s.title)
        saveToFile(fn, tostring(s.to_xml(), "unicode"))
        print(fn)


if __name__ == '__main__':
    # UTF8Writer = getwriter('utf8')
    # sys.stdout = UTF8Writer(sys.stdout)

    session = requests.Session()
    songs = load_song_list(session, base_url);

    load_songs(session, songs)

    save_songs_to_file(songs, 'songs')
