from MySqlTasty import MySqlTasty
import scriptures   #https://github.com/davisd/python-scriptures

def toSuperScript(s):
        s = str(s)
        sups={u'0': u'\u2070',
              u'1': u'\xb9',
              u'2': u'\xb2',
              u'3': u'\xb3',
              u'4': u'\u2074',              
              u'5': u'\u2075',
              u'6': u'\u2076',
              u'7': u'\u2077',
              u'8': u'\u2078',
              u'9': u'\u2079'}
        if s.isdigit():
            return ''.join([sups[i] for i in s])
   
class BibleDB(object):
    
    Bible = None
    __Books=[]
    
        
    def __BuildPassageFromArray(self,DictArray,vStart):
        passage = ''
        for i, verses in enumerate(DictArray):
            passage += toSuperScript(vStart)+DictArray[i]['text']
            vStart = vStart+1
        return passage
        
    def __init__(self):
        global Bible
        global __Books
        Bible = MySqlTasty('BIBLE','Koki','311311Susi','107.170.42.28')
        __Books = self.GetBooks()
           
    def GetBooks(self):
        Bible.execute('select n as Book,b as Id from key_english')
        return Bible.GetResultsDictArray()
    def GetChapters(self):
        pass
    def GetVerses(self):
        pass
                        
    def ResolveRequest(self,StringRequest):
            Passage = ''
            passageRefTuple = scriptures.extract(StringRequest)
            if len(passageRefTuple) > 0:
                BookID       = ''
                ChapterID    = ''
                VerseStartID = ''
                VerseEndID   = ''
                BookName = str(passageRefTuple[0][0])
                if BookName == 'Revelation of Jesus Christ':
                    BookName = 'Revelation'
                BookName = BookName.replace('II','2')
                BookName = BookName.replace('I','1')
                print(BookName+'***************************************************************************')
                for i, book in enumerate(__Books):
                    if BookName == __Books[i]['Book']:
                        BookID  = format(__Books[i]['Id'],'02')
                        ChapterID = format(passageRefTuple[0][1],'03')
                        VerseStartID   = format(passageRefTuple[0][2],'03')
                        VerseEndID     = format(passageRefTuple[0][4],'03')
                idStart = str(BookID+ChapterID+VerseStartID)
                idEnd   = str(BookID+ChapterID+VerseEndID)
                
                Bible.execute('SELECT t as text FROM t_asv WHERE id BETWEEN '+idStart+' AND '+idEnd)
                SelectDataArray = Bible.GetResultsDictArray()
                Passage = self.__BuildPassageFromArray(SelectDataArray,passageRefTuple[0][2])
            return Passage

            
    def ReturnTest(self):
        return str(self.GetBooks()[0][0])
        # Bible.execute(sql)
        # Data = Bible.GetResultsDictArray()
        # return Data[0]['a']
        
        
        
    
        