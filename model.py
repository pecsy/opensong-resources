

class Bible:
    def __init__(self,name,url):
        self.books = []
        self.name = name
        self.url = url

    def addBook(self, book):
        self.books.append(book)
        book.setNumber(len(self.books))


class Book:
    def __init__(self, title, url):
        self.title = title
        self.url = url
        self.number = 0
        self.chapters = []

    def setNumber(self,num):
        self.number = num

    def getTitle(self):
        return self.title

    def getUrl(self):
        return self.url

    def addChapter(self,chapter):
        self.chapters.append(chapter)
        chapter.setBook(self)
        chapter.setNumber(len(self.chapters))

class Verse:
    def __init__(self, num, text):
        self.number = num
        self.text = text

class Chapter:
    def __init__(self, url, summary):
         # type: (str, list) -> Chapter
        self.book = None
        self.url = url
        self.summary = summary
        self.verses = []

    def setBook(self,book):
        self.book = book
        return self

    def setNumber(self,num):
        self.number = num
        return self


    def addVerse(self,text):
        verse = Verse(len(self.verses)+1,text)
        self.verses.append(verse)
        return self