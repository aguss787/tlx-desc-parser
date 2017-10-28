import re

def isCompleteSquareBracket(cur):
    curLen = len(cur);
    
    if curLen < 2:
        return False;

    if cur[0] != '[':
        return False;

    if cur[-1] != ']':
        return False;

    for i in range(1, curLen - 2):
        if cur[i] == '[' or cur[i] == ']':
            return False;

    return True;

def getline(inFile):
    cur = inFile.readline();
    if cur == "":
        return None
    return cur[:-1]

def isList(string):
    if not string:
        return False

    string = string.strip()

    sz = len(string)
    if sz < 2:
        return False

    return string[0:2] == '- ' or string[0:2] == '+ '

def getListLevel(string):
    if not isList(string):
        raise Exception('not a list')
    return len(string) - len(string.lstrip())
