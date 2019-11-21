# coding: utf-8

import model
from xml.etree.ElementTree import Element, SubElement

# <?xml version="1.0" encoding="UTF-8"?>
# <XMLBIBLE xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
#     xsi:noNamespaceSchemaLocation="zef2005.xsd"
#     version="2.0.0.0"
#     status="v"
#     type="x-bible"
#     biblename="NASB"
#     revision="0">
#     <INFORMATION/>
#     <BIBLEBOOK bnumber="1" bname="Genesis">
#         <CHAPTER cnumber="1">
#             <VERS vnumber="1">In the beginning God created the heavens and the earth.</VERS>
#             <VERS vnumber="2">The earth was formless and void, and darkness was over the surface of the deep, and the Spirit of God was moving over the surface of the waters.</VERS>
#             <VERS vnumber="3">Then God said, "Let there be light"; and there was light.</VERS>
#             <VERS vnumber="4">God saw that the light was good; and God separated the light from the darkness.</VERS>
#             <VERS vnumber="5">God called the light day, and the darkness He called night. And there was evening and there was morning, one day.</VERS>
#         </CHAPTER>
#     </BIBLEBOOK>
# </XMLBIBLE>

class BT:
    def __init__(self,name, shortname):
        self.name = name
        self.shortname = shortname


book_titles = [
    BT('Not a book', 'NOB'), # Added to align indexes wjth book numbers.
    BT(u'1 Mózes', u'1Móz'),
    BT(u'2 Mózes', u'2Móz'),
    BT(u'3 Mózes', u'3Móz'),
    BT(u'4 Mózes', u'4Móz'),
    BT(u'5 Mózes', u'5Móz'),
    BT(u'Józsué', u'Józs'),
    BT(u'Bírák', u'Bír'),
    BT(u'Ruth', u'Ruth'),
    BT(u'1 Sámuel', u'1Sám'),
    BT(u'2 Sámuel', u'2Sám'),
    BT(u'1 Királyok', u'1Kir'),
    BT(u'2 Királyok', u'2Kir'),
    BT(u'1 Krónikák', u'1Krón'),
    BT(u'2 Krónika', u'2Krón'),
    BT(u'Ezsdrás', u'Ezsd'),
    BT(u'Nehemiás', u'Neh'),
    BT(u'Eszter', u'Eszt'),
    BT(u'Jób', u'Jób'),
    BT(u'Zsoltárok', u'Zsolt'),
    BT(u'Példabeszédek', u'Péld'),
    BT(u'Prédikátor', u'Préd'),
    BT(u'Énekek éneke', u'Énekek'),
    BT(u'Ézsaiás', u'Ézs'),
    BT(u'Jeremiás', u'Jer'),
    BT(u'Jeremiás siralmai', u'JSir'),
    BT(u'Ezékiel', u'Ez'),
    BT(u'Dániel', u'Dán'),
    BT(u'Hóseás', u'Hós'),
    BT(u'Jóel', u'Jóel'),
    BT(u'Ámósz', u'Ám'),
    BT(u'Abdiás', u'Abd'),
    BT(u'Jónás', u'Jón'),
    BT(u'Mikeás', u'Mik'),
    BT(u'Náhum', u'Náh'),
    BT(u'Habakuk', u'Hab'),
    BT(u'Zofóniás', u'Zof'),
    BT(u'Haggeus', u'Hag'),
    BT(u'Zakariás', u'Zak'),
    BT(u'Malakiás', u'Mal'),
    BT(u'Máté', u'Mt'),
    BT(u'Márk', u'Mk'),
    BT(u'Lukács', u'Luk'),
    BT(u'János', u'Ján'),
    BT(u'Apostolok cselekedetei', u'ApCsel'),
    BT(u'Rómaiakhoz', u'Róm'),
    BT(u'1 Korintusi', u'1Kor'),
    BT(u'2 Korintusi', u'2Kor'),
    BT(u'Galatákhoz', u'Gal'),
    BT(u'Efézusiakhoz', u'Ef'),
    BT(u'Filippiekhez', u'Fil'),
    BT(u'Kolosséiakhoz', u'Kol'),
    BT(u'1 Thesszalonika', u'1Thessz'),
    BT(u'2 Thesszalonika', u'2Thessz'),
    BT(u'1 Timóteushoz', u'1Tim'),
    BT(u'2 Timóteushoz', u'2Tim'),
    BT(u'Tituszhoz', u'Tit'),
    BT(u'Filemonhoz', u'Filem'),
    BT(u'Zsidókhoz', u'Zsid'),
    BT(u'Jakab', u'Jak'),
    BT(u'1 Péter', u'1Pét'),
    BT(u'2 Péter', u'2Pét'),
    BT(u'1 János', u'1Ján'),
    BT(u'2 János', u'2Ján'),
    BT(u'3 János', u'3Ján'),
    BT(u'Júdás', u'Júd'),
    BT(u'Jelenések', u'Jel')
]


def verseToNode(verse):
    node = Element('VERS')
    node.set('vnumber',str(verse.number))
    node.text=verse.text
    return node


def chapterToNode(chapter):
    node = Element('CHAPTER')
    node.set('cnumber',str(chapter.number))

    for verse in chapter.verses:
        verseNode = verseToNode(verse)
        node.append(verseNode)
    return node


def bookToNode(book):
    node = Element('BIBLEBOOK')
    node.set('bnumber',str(book.number))
    node.set('bname',book_titles[book.number].name)
    node.set('bsname',book_titles[book.number].shortname)

    for chapter in book.chapters:
        chapterNode = chapterToNode(chapter)
        node.append(chapterNode)

    return node

def bibleToNode(bible):
    node = Element('XMLBIBLE')
    node.set('xmlns:xsi','http://www.w3.org/2001/XMLSchema-instance')
    node.set('xsi:noNamespaceSchemaLocation','zef2005.xsd')
    node.set('version','2.0.1.16')
    node.set('status','v')
    node.set('type','x-bible')
    node.set('biblename', bible.name)
    node.set('revision','0')
    node.append(informationToNode(bible))
    for book in bible.books:
        bookNode = bookToNode(book)
        node.append(bookNode)

    return node

def exportToZefaniaXML(bible):
    bibleNode = bibleToNode(bible)
    return bibleNode

# <INFORMATION>
# <format>Zefania XML Bible Markup Language</format>
# <date>2005-03-10</date>
# <title>Magyar Újfordítású Biblia</title>
# <contributors>
# Magyar Bibliatársulat Hungarian Bible Society H-1113 Budapest Bocskai út 35. Tel.: 36-1 386-8267; 36-1 386-8277 Tel./Fax: 36-1 466-9392
# </contributors>
# <source>http://web.axelero.hu/kaveonline/sword/</source>
# <subject>holy bible</subject>
# <creator>ws</creator>
# <publisher>the word company</publisher>
# <identifier>HunUj</identifier>
# <language>HUN</language>
# <description>Magyar Bibliatarsulat Ujforditasu Bibliaja</description>
# <rights>Public Domain; Free distribution</rights>
# </INFORMATION>
def informationToNode(bible):
    node = Element('INFORMATION')
    return node