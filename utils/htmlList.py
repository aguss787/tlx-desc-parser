from utils.util import isList
from utils.util import getListLevel
from utils.htmlPattern import htmlParse

class HtmlList:
    statementList = []

    def __init__(self):
        self.statementList = []

    def add(self, statement):
        if not isList(statement):
            raise Exception('not a list')
        self.statementList.append(statement)

    def toString(self):
        levelMap = {-1}
        for i in self.statementList:
            levelMap.add(getListLevel(i))

        levelList = sorted([i for i in levelMap])
        cur = 0
        res = ""

        for i in self.statementList:
            level = getListLevel(i)
            while levelList[cur] < level:
                res += "<ul>\n"
                cur += 1

            while levelList[cur] > level:
                res += "</ul>\n"
                cur -= 1

            res += "<li>"
            res += htmlParse(i.lstrip()[2:])
            res += "</li>\n"

        while cur > 0:
            res += "</ul>\n"
            cur -= 1

        return res
