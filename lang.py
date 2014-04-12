import math
import sys



pos_adj    = []
neg_adj    = []
pos_comp   = []
neg_comp   = []
pos_nouns  = []
neg_nouns  = []
valid_names= []
zero_nouns = ['nothing', 'zero']

first_person = []
second_person = []

def Assert(b, s):
    if not b:
        sys.stderr.write(s + " at line " + "ERROR" + "\n")
        sys.exit(1)

def isFirstPerson(s):
    return s in first_person
    
def isSecondPerson(s):
    return s in second_person

def isNoun(word):
    return word in pos_nouns or word in neg_nouns or word in zero_nouns

def isAdjective(word):
    return word in pos_adj or word in neg_adj

def isComparative(word):
    return word in pos_comp or word in neg_comp

#returns 1 for "nice" and neutral nouns, -1 for nasty ones
def nounValue(word):
    Assert(isNoun(word), "Tried to find the nounvalue of a non-noun")
    return 1 if word in pos_nouns else -1 if word in neg_nouns else 0

#return s with all whitespace characters removed
def trimWhitespace(s):
    trimmed = ""
    for c in s:
        if c not in ['\t', '\r', '\n', ' ']:
            trimmed += c
    return trimmed
    
#return s with all whitespace characters before the first non-whitedspace character removed
def trimLeadingWhitespace(s):
    trimIndex = 0
    for c in s:
        if c in ['\t', '\r', '\n', ' ']:
            trimIndex +=1
        else:
            break
    return s[trimIndex:]

#A whitespace-agnositic beginswith method
def beginsWithNoWhitespace(s, pattern):
    return beginsWith(trimWhitespace(s), pattern)

def beginsWith(s, pattern):
    return s[:len(pattern)] == pattern 
    
def loadFileIntoList(filename, list):
    f = open(filename, 'r')
    for word in f.readlines():
        list.append(word.split(" ")[-1][:-1])
    f.close()

#load initial noun and adjective lists
def loadWordLists():
    loadFileIntoList("include/neutral_adjective.wordlist" , pos_adj)
    loadFileIntoList("include/positive_adjective.wordlist", pos_adj)
    loadFileIntoList("include/negative_adjective.wordlist", neg_adj)
    loadFileIntoList("include/positive_noun.wordlist", pos_nouns)
    loadFileIntoList("include/neutral_noun.wordlist" , pos_nouns)
    loadFileIntoList("include/negative_noun.wordlist", neg_nouns)
    loadFileIntoList("include/positive_comparative.wordlist", pos_comp)
    loadFileIntoList("include/positive_comparative.wordlist", neg_comp)
    loadFileIntoList("include/character.wordlist", valid_names)
    
    loadFileIntoList("include/second_person.wordlist", second_person)
    loadFileIntoList("include/second_person_possessive.wordlist", second_person)
    loadFileIntoList("include/second_person_reflexive.wordlist", second_person)
    
    loadFileIntoList("include/first_person.wordlist", first_person)
    loadFileIntoList("include/first_person_possessive.wordlist", first_person)
    loadFileIntoList("include/first_person_reflexive.wordlist", first_person)

roman_values = { 'M': 1000, 'D': 500, 'C': 1000, 'L': 50, 'X': 10, 'V': 5, 'I': 1 }
def parseRomanNumeral(roman_string):
    roman_string = roman_string.upper() 
    strindex = 0
    roman_sum = 0
    while strindex < len(roman_string) - 1:
        if(roman_values[roman_string[strindex]] < roman_values[roman_string[strindex+1]]):
            roman_sum -= roman_values[roman_string[strindex]]
        else:
            roman_sum += roman_values[roman_string[strindex]]
        strindex += 1
    return roman_sum + roman_values[roman_string[strindex]]

def isNumber(s):
    words = s.split(" ")
    for word in words:
        if isNoun(word):
            return True
    return False


#parse a string that is supposed to evaluate to a number
def safeParseNum(s):
    words = s.split(" ")
    nounIndex = len(words)
    for i in range(0,len(words)):
        if isNoun(words[i]):
            nounIndex = i
            break
    if(nounIndex < len(words)):
        value = nounValue(words[nounIndex])
        for word in words[:nounIndex]:
            if isAdjective(word):
                value *= 2
        return value
    else:
        return 0

#parse a string that is supposed to evaluate to a number
def parseNum(s):
    words = s.split(" ")
    nounIndex = len(words)
    for i in range(0,len(words)):
        if isNoun(words[i]):
            nounIndex = i
            break
    Assert (nounIndex < len(words), str(words) + "\nExpected a number, but found no noun")
    value = nounValue(words[nounIndex])
    for word in words[:nounIndex]:
        if isAdjective(word):
            value *= 2
    return value

#returns the index of the leftmost punctuation mark in s
def findPunctuation(s):
    valids = []
    for val in [s.find('.'), s.find('!'), s.find('?')]:
        if val >= 0:
            valids.append(val)
    return -1 if len(valids) == 0 else min(valids)

def wordToOperator(op):
    if op == "sum":
        return "+"
    elif op == "difference":
        return "-"
    elif op == "quotient":
        return "/"
    elif op == "product":
        return "*"
    else:
        Assert(False, "Illegal Operator")
        
class Tree:
    def __init__(self, v, l, r):
        self.value = v
        self.left  = l
        self.right = r


binop = ["sum", "difference", "quotient", "product"]
unop  = ["square", "cube", "twice"]
def buildExpressionTree(expr, target, speaker, vartable):
    Assert (len(expr) > 0, "Ill-formed Expression in " + str(expr))
    if expr[0] == "square":
        if expr[1] == "root":
            op = "math.sqrt"
            expr = expr[2:]
            num, expr = buildExpressionTree(expr, target, speaker, vartable)
            return Tree(op, num, ""), expr
    elif expr[0] == "remainder":
        if expr[1] == "of" and expr[2] == "the" and expr[3] == "quotient":
            expr = expr[4:]
            op = "%"
            left, expr  = buildExpressionTree(expr, target, speaker, vartable)
            right, expr = buildExpressionTree(expr, target, speaker, vartable)
            return Tree(op, left, right), expr
    if expr[0] in binop:
        op = wordToOperator(expr[0])
        expr  = expr[1:]
        left, expr  = buildExpressionTree(expr, target, speaker, vartable)
        right, expr = buildExpressionTree(expr, target, speaker, vartable)
        return Tree(op, left, right), expr
    elif expr[0] in unop:
        op = expr[0]
        expr = expr[1:]
        num, expr = buildExpressionTree(expr, target, speaker, vartable)
        return Tree(op, num, ""), expr

    if True:
        i = 1 if expr[0] == "and" else 0
        numstr = ""
        while expr[i] not in binop and expr[i] not in unop and expr[i] not in ["and", "remainder"]:
            if expr[i] in ["you", "thee", "yourself", "thyself", "thou"]:
                expr = expr[i + 1:]
                return Tree(target, "", ""), expr
            elif expr[i] in ["me", "myself", "i"]:
                expr = expr[i + 1:]
                return Tree(speaker, "", ""), expr
            elif expr[i].capitalize() in vartable:
                name = expr[i]
                expr = expr[i + 1:]
                return Tree(name.capitalize(), "", ""), expr
            elif i == len(expr) - 1:
                numstr += expr[i]
                i = len(expr)
                break
            else:
                numstr += expr[i] + " "
                i += 1
        if i == len(expr):
            expr = []
        else:
            expr = expr[i:]
        if not isNumber(numstr):
            return buildExpressionTree(expr, target, speaker, vartable)
        else:
            return Tree(str(parseNum(numstr)), "", ""), expr

def concatWords(wordArray):
    c = ""
    for word in wordArray:
        c += word
    return c

def firstWord(statement):
    words = statement.split(" ")
    for word in words:
        if len(word) > 0:
            return word
            
def getActOrSceneNumber(s, actOrScene):
    num = s[s.find(actOrScene):].split(" ")[1]
    if num.find(':') > 0:
        num = num[:num.find(':')]
    else:
        Assert (False, "Bad " + actOrScene + " heading")
    return parseRomanNumeral(num)

def getActOrSceneDescription(s):
    desc = trimWhitespace(s[s.find(':')+1:]).lower()
    p = findPunctuation(desc)
    if p > 0:
        desc = desc[:p]
    return desc

loadWordLists()