from xml.etree.ElementTree import Element

# <?xml version="1.0" encoding="UTF-8"?>
# <song>
#   <title>3. Ó, mely sokan vannak, Akik háborgatnak</title>
#   <author></author>
#   <copyright></copyright>
#   <hymn_number></hymn_number>
#   <presentation>V1 V2 V3 V4</presentation>
#   <ccli></ccli>
#   <capo print="false"></capo>
#   <key></key>
#   <aka></aka>
#   <key_line></key_line>
#   <user1></user1>
#   <user2></user2>
#   <user3></user3>
#   <theme></theme>
#   <tempo></tempo>
#   <time_sig></time_sig>
#   <lyrics>
# lyrics comes here
# </lyrics></song>

class Song:

    def __init__(self, index, title, url):
        self.title = title
        self.author = ''
        self.copyright = ''
        self.hymn_number = index
        self.presentation = ''
        self.ccli = ''
        self.capo = ''
        self.key = ''
        self.aka = ''
        self.key_line = ''
        self.user1 = ''
        self.user2 = ''
        self.user3 = ''
        self.theme = ''
        self.tempo = ''
        self.time_sig = ''
        self.lyrics = []
        self.url = url

    def add_verse(self, index, lines):
        self.lyrics.append(Verse(index,lines))

    FIELDS = (
        'title', 'author', 'hymn_number', 'copyright', 'presentation', 'ccli', 'key', 'aka', 'key_line',
        'user1', 'user2', 'user3', 'theme', 'tempo', 'time_sig'
    )

    def to_xml(self):
        node = Element('song')
        for field in Song.FIELDS:
            f = Element(field)
            f.text = str(getattr(self, field))
            node.append(f)

        capo = Element('capo')
        capo.set("print", "false")
        capo.text = ''
        node.append(capo)
        lyrics = self.lyrics_to_xml()
        node.append(lyrics)
        return node

    def lyrics_to_xml(self):
        node = Element('lyrics')
        text = ''
        for v in self.lyrics:
            text += str(v) + '\n'
        node.text = text
        return node


class Verse:

    def __init__(self, index, lines):
        self.index = index
        self.lines = lines

    def __str__(self):
        res = '[V{}]\n'.format(self.index)
        for l in self.lines:
            res += ' ' + l + '\n'
        return res