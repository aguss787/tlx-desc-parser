from utils.util import isCompleteSquareBracket
from utils.util import getline
from utils.util import isList

from utils.htmlPattern import htmlParse

from utils.htmlList import HtmlList

class BaseSegment:
    html_tag = 'p';
    breakLine = '</br>\n';

    @classmethod
    def isMatch(cls, cur):
        return False;

    @classmethod
    def process(cls, cur, inFile):
        res = '<h3>%s</h3>\n' % (cur[1:-1])
        isOpen = False
        isInList = False
        q = []
        segment = None
        while True:
            cur = getline(inFile)

            if cur is None:
                break

            segment = getMatch(cur)

            if segment:
                break

            if isList(cur):
                if not q or not isinstance(q[-1], HtmlList):
                    q.append(HtmlList())
                q[-1].add(cur)
            else:
                q.append(cur)

        q.append('');
        sz = len(q);

        st = []
        for i in q:
            if not i and st:
                res += cls.writeStack(st)
                st = []
            elif i:
                st.append(i)

        if st:
            res += cls.writeStack(st)

        if segment:
            res += segment.process(cur, inFile)

        return res

    @classmethod
    def writeStack(cls, st):
        if not st:
            return

        res = ''
        isString = False
        for i in st:
            if isinstance(i, HtmlList):
                if isString:
                    res += '</%s>\n' % cls.html_tag
                res += i.toString()
                isString = False
            else:
                if isString:
                    res += cls.breakLine;
                else:
                    res += '<%s>\n' % cls.html_tag
                res += htmlParse(i) + '\n'
                isString = True
        
        if isString:
            res += '</%s>\n' % cls.html_tag

        return res


class Description(BaseSegment):
    @classmethod
    def isMatch(cls, cur):
        return isCompleteSquareBracket(cur)


class Constraint(BaseSegment):
    tag = {
        "[Batasan]",
        "[Subsoal]",
        "[Subtask]",
    }

    @classmethod
    def isMatch(cls, cur):
        return cur in cls.tag

    @classmethod
    def writeStack(cls, st):
        if not st:
            return

        res = ''
        isString = False
        for i in st:
            if isinstance(i, HtmlList):
                res += i.toString()
                isString = False
            elif i:
                if isString:
                    res += '</br>\n'
                res += '<h4>' + htmlParse(i) + '</h4>\n'
                isString = True

        return res

class SampleCase(BaseSegment):
    tag = {
        "Contoh Masukan",
        "Contoh Keluaran",
    }

    breakLine = '';
    html_tag = 'pre'

    @classmethod
    def isMatch(cls, cur):
        if not isCompleteSquareBracket(cur):
            return False
        res = False
        for i in cls.tag:
            strlen = len(i)
            res = res or (cur[1:1 + strlen] == i)
        return res 

segmentList = [
    SampleCase,
    Constraint,
    Description,
];

def getMatch(cur):
    for segment in segmentList:
        if segment.isMatch(cur):
            return segment
    return None

def parse(inFile):
    cur = inFile.readline();
    res = ''
    while True:
        cur = getline(inFile)
        if cur is None:
            break

        segment = getMatch(cur);
        if segment:
            res += segment.process(cur, inFile)

    return res
 
