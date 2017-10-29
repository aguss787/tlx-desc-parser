import html
import re

class basePattern:
    pattern = re.compile(".+")

    @classmethod
    def search(cls, string):
        return cls.pattern.search(string)

    @classmethod
    def parse(cls, string):
        matchRes = cls.search(string)
        if not matchRes:
            return None

        return html.escape(string)

class suberscriptPattern(basePattern):
    tag = ''

    @classmethod
    def parse(cls, string):
        matchRes = cls.search(string)
        if not matchRes:
            return None

        return parse(string[:matchRes.start()]) \
               + ('<%s>%s</%s>' % (cls.tag, parse(matchRes.group(1)), cls.tag)) \
               + parse(string[matchRes.end():])

class subscriptPattern(suberscriptPattern):
    pattern = re.compile('(?<!\\\)\_([^\s]+)')
    tag = 'sub'

class bracketedSubscriptPattern(suberscriptPattern):
    pattern = re.compile('(?<!\\\)\_\{([^\s]+)\}')
    tag = 'sub'

class superscriptPattern(suberscriptPattern):
    pattern = re.compile('(?<!\\\)\^([^\s]+)')
    tag = 'sup'

class bracketedSuperscriptPattern(suberscriptPattern):
    pattern = re.compile('(?<!\\\)\^\{([^\s]+)\}')
    tag = 'sup'

class codePattern(basePattern):
    pattern = re.compile('(?<!\\\)\`(.+?)(?<!\\\)\`')

    @classmethod
    def parse(cls, string):
        matchRes = cls.search(string)
        if not matchRes:
            return None

        return parse(string[:matchRes.start()]) \
               + ('<code>%s</code>' % (parse(matchRes.group(1)))) \
               + parse(string[matchRes.end():])


class imagePattern(basePattern):
    pattern = re.compile("(?<!\\\)<img: ([a-zA-Z\._-]+)>")

    @classmethod
    def parse(cls, string):
        matchRes = cls.search(string)
        if not matchRes:
            return None

        fileName = matchRes.group(1)
        return '<center><img alt="" src="render/%s" style="width:500px" /></center>' % fileName


class linkPattern(basePattern):
    pattern = re.compile("(?<!\\\)<link: ([a-zA-Z\._]+)>(.*?)</link>")

    @classmethod
    def parse(cls, string):
        matchRes = cls.search(string)
        if not matchRes:
            return None

        fileName = matchRes.group(1)
        linkText = matchRes.group(2)
        return parse(string[:matchRes.start()]) \
               + '<a href="render/%s">%s</a>' % (fileName, parse(linkText)) \
               + parse(string[matchRes.end():])

class backslashPattern(basePattern):
    pattern = re.compile("\\\(.)")

    @classmethod
    def parse(cls, string):
        matchRes = cls.search(string)
        if not matchRes:
            return None

        return parse(string[:matchRes.start()]) \
               + ('%s' % parse(matchRes.group(1))) \
               + parse(string[matchRes.end():])

patterns = [
    codePattern,
    bracketedSubscriptPattern,
    bracketedSuperscriptPattern,
    subscriptPattern,
    superscriptPattern,
    imagePattern,
    linkPattern,
    backslashPattern,
    basePattern,
]

def parse(string):
    if not string:
        return ""
    for pattern in patterns:
        if pattern.search(string):
            return pattern.parse(string)
    return None

def htmlParse(string):
    return parse(string)
