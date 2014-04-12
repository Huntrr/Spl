import sys
import math
import lang

"""A Shakespeare Compiler written in Python, splc.py
This is a compiler that implements the majority of the Shakespeare programming language
invented by Kalle Hasselstrom and Jon Aslund, I take no credit for inventing the language.
This software is free to edit or use, and though I doubt anyone would use this for many projects,
I guess I would appreciate some degree of acknowledgment if you do.
(c) V1.1 Sam Donow 2013-2014
sad3@williams.edu
drsam94@gmail.com"""
#missing features
#full support for multi-word nouns/names
#Stacks, who needs them?

N          = 0
src        = ""
vartable   = set([])
speaker    = ""
target     = ""
stage      = set([])
actnum     = 0
act_names  = {}
scene_names= []

#report a compile-time error, then exit
def Assert(b, s):
    global N
    if not b:
        sys.stderr.write(s + " at line " + str(N) + "\n")
        sys.exit(1)
lang.Assert = Assert

#Abstraction for writing to file, eased python 2/3 agnosticity,
#and will eventually allow file output instead of stdout if that
#ever is desired
def writeToFile(s):
    sys.stdout.write(str(s) + "\n")

def parseEnterOrExit():
    global stage
    endBracket = src[N].find(']')
    Assert(endBracket >= 0, "[ without matching ]")
    enterOrExit = src[N][src[N].find('[')+1:src[N].find(']')]
    if lang.beginsWithNoWhitespace(enterOrExit, "Enter"):
        names = enterOrExit[enterOrExit.find(" ") + 1:].split(" and ")
        for namestr in names:
            name = namestr.split(" ")[-1]
            Assert(name in vartable, "Undeclared actor entering a scene")
            stage.add(name)
        Assert(len(stage) < 3, "Too many actors on stage")
    elif lang.beginsWithNoWhitespace(enterOrExit, "Exit"):
        names = enterOrExit[enterOrExit.find(" ") + 1:].split(" and ")
        for namestr in names:
            name = namestr.split(" ")[-1]
            Assert(name in stage, "Trying to make an actor who is not in the scene exit")
            stage.remove(name)
    elif lang.beginsWithNoWhitespace(enterOrExit, "Exeunt"):
        if enterOrExit.find(" ") == -1:
            stage = set([])
        else: 
            names = enterOrExit[enterOrExit.find(" ") + 1:].split(" and ")
            for namestr in names:
                name = namestr.split(" ")[-1]
                Assert(name in stage, "Trying to make an actor who is not in the scene exit")
                stage.remove(name)
    else:
        Assert(False, "Bracketed clause without Enter, Exit, or Exeunt")

#returns an array of the punctuation-delimited statements at the current location in the parsing
def getStatements():
    global N
    statements = []
    line = lang.trimLeadingWhitespace(src[N])
    unfinished = False
    while line.find(':') < 0 and line.find('[') < 0:
        punctuation = lang.findPunctuation(line)
        if punctuation < 0:
            if unfinished == False:
                statements.append(line[:-1])
            else: 
                statements[-1] += line[:-1]
            N += 1
            line = src[N]
            unfinished = True
        elif punctuation > 0:
            if not unfinished:
                statements.append("")
            statements[-1] += line[:punctuation]
            line = line[punctuation + 1:]
            unfinished = False
    retval = []
    for stat in statements:
        if len(lang.trimWhitespace(stat)) > 0:
            retval.append(stat)
    return retval


def TreeToString(tree):
    if tree.left == "":
        #just a value
        return str(tree.value)
    elif tree.right == "":
        #unary operator
        return "int(" + str(tree.value) + "(" + TreeToString(tree.left) + "))"
    else:
        #binary operator
        return "int((" + TreeToString(tree.left) + " " + str(tree.value) + " " + TreeToString(tree.right) + "))"

def parseExpr(expr):
    tree = lang.buildExpressionTree(expr.split(" "), target, speaker, vartable)[0]
    return TreeToString(tree)

def parseStatement(stat):
    statement = lang.trimLeadingWhitespace(stat).lower()
    first = statement.split(" ")[0]
    trimmed = lang.trimWhitespace(statement)
    if first in ["you", "thou"]:
        #this is an assignment of the form Prounoun [as adj as] expression
        expr = ""
        if statement.rfind("as") >= 0:
            expr = statement[statement.rfind("as") + 3:]
        else:
            expr = statement[len(first) + 1:]
        return target + " = " + parseExpr(expr)
    elif trimmed == "openyourheart" or trimmed == "openthyheart":
        #numerical output
        return 'sys.stdout.write(str(' + target + '))'
    elif trimmed == "speakyourmind" or trimmed == "speakthymind":
        #character output
        return 'sys.stdout.write(chr(' + target + '))'
    elif trimmed == "listentoyourheart" or trimmed == "listentothyheart":
        #numerical input
        return target + " = int(raw_input())"
    elif trimmed == "openyourmind" or trimmed == "openthymind":
        #character input
        return target + " = getChar()"
    elif first in ["am", "are", "art", "be", "is"]:
        #questions - do not yet support "not"
        left  = ""
        kind  = ""
        right = ""
        flipped = False;
        if statement.split(" ")[2] == "not":
            flipped = True;
        if statement.find("as") >= 0:
            left, kind, right = statement.split(" as ")
            Assert(lang.isAdjective(kind), "Ill-formed conditional in " + statement)
            kind = "equal"
        elif statement.find("more") >= 0:
            words = statement.split(" ")
            moreloc = 0
            for i in range(0, len(words)):
                if words[i] == "more":
                    moreloc = i
                    break
            Assert(lang.isAdjective(words[moreloc + 1]), "Ill-formed conditional in " + statement)
            kind = "greater" if words[moreloc + 1] in lang.pos_adj else "lesser"
            left, right = statement.split(" more " + words[moreloc + 1] + " ")
        else:
            comp = ""
            for word in statement.split(" "):
                if lang.isComparative(word):
                    comp = word
                    break
            Assert(len(comp) > 0, "Ill-formed conditional in " + statement)
            kind = "greater" if comp in lang.pos_comp else "lesser"
            left, right = statement.split(comp)
        if flipped:
            return "condition = !((" + parseExpr(left) + ") " + (">" if kind == "greater" else "<" if kind == "lesser" else "==") + " (" + parseExpr(right) + "))"
        else:
            return "condition = (" + parseExpr(left) + ") " + (">" if kind == "greater" else "<" if kind == "lesser" else "==") + " (" + parseExpr(right) + ")"
    elif lang.beginsWith(statement, "if so,"):
        #positive condition
        location = statement.find("if so,")
        return "if condition: \n\t\t" + parseStatement(statement[location + 7:]) + "\n"
    elif lang.beginsWith(statement, "if not,"):
        #negative condition
        location = statement.find("if not,")
        return "if not condition: \n\t\t" + parseStatement(statement[location + 8:]) + "\n"
    elif lang.beginsWith(statement, "let us") or lang.beginsWith(statement, "we shall") or lang.beginsWith(statement, "we must"):
        words = statement.split(" ")
        nextTwo = words[2] + " " + words[3]
        Assert (nextTwo == "return to" or nextTwo == "proceed to", "Ill-formed goto")
        # classic goto with scene or act
        if words[4] == "scene":
            return getFunction(str(actnum), str(lang.parseRomanNumeral(words[5])))
        elif words[4] == "act":
            #typeword = words[4] if words[4] == "act" else ("act_" + str(actnum) + "_scene")
            return getFunction(str(lang.parseRomanNumeral(words[5])), 1)
        else:
            restOfPhrase = lang.concatWords(words[4:])
            type_ = "scene" if restOfPhrase in scene_names[actnum].keys() \
            else "act" if restOfPhrase in act_names.keys() else "none"
            Assert (type_ != "none", "Goto refers to nonexistant act or scene")
            nameDict = act_names if type_ == "act" else scene_names[actnum]
            if type_ == "act":
                return getFunction(str(nameDict[restOfPhrase]), 1)
            elif type_ == "scene":
                return getFunction(str(actnum), str(nameDict[restOfPhrase]))
            #typeword = act if type_ == "act" else ("act_" + str(actnum) + "_scene")
            #return "goto " + typeword + str(nameDict[restOfPhrase]) + ";\n"
    elif first == "remember":
        #push subject to target's stack
        subjects = statement.split(" ")[1:]
        finalSubj = speaker #default to speaker with just a "REMEMBER!" statement
        for subject in subjects:
            if lang.isSecondPerson(subject):
                finalSubj = target
                break
            elif lang.isFirstPerson(subject):
                break
            
        return target + "_stack.append(" + finalSubj + ")"
    elif first == "recall":
        #pop from subject's stack to target's var
        subjects = statement.split(" ")[1:]
        finalSubj = target #default to target with just a "RECALL!" statement
        for subject in subjects:
            if lang.isFirstPerson(subject):
                finalSubj = speaker
                break
            elif lang.isSecondPerson(subject):
                break
        
        return target + " = " + finalSubj + "_stack.pop()"
    else:
        return ""

def getFunction(actN, sceneN):
    return "act_" + actN + "_scene" + sceneN + "()"

def writeScenes(scenes, isLast):
    #writeToFile("def act_" + str(actnum) + "():")
    writeToFile("#ACT " + str(actnum))
    for j in range(0, len(scenes)):
        writeToFile("def act_" + str(actnum) + "_scene" + str(j + 1) + "():")
        writeToFile("\t" + getGlobals())
        if(scenes[j][0] == "\n"):
            writeToFile(scenes[j][1:])
        else:
            writeToFile(scenes[j])
        if j < len(scenes) - 1:
            writeToFile("\tact_" + str(actnum) + "_scene" + str(j + 2) + "()\n")
        elif not isLast:
            writeToFile("\tact_" + str(actnum + 1) + "_scene1()\n")
    #writeToFile("#END ACT " + str(actnum) + "\n\n")
    
def handleDeclarations():
    global N
    global src
    #variables, declaration syntax:
    #Name, value
    declarations = []
    unfinished = False
    while not lang.beginsWithNoWhitespace(src[N], 'Act'):
        Assert(N < len(src) - 1, "File contains no Acts")
        if len(lang.trimWhitespace(src[N])) > 0:
            if not unfinished:
                declarations.append(src[N])
            else:
                declarations[-1] += src[N]
            unfinished = src[N].find('.') < 0
        N += 1

    for dec in declarations:
        commaIndex = dec.find(',')
        Assert(commaIndex > 0, "Improper declaration " + str(declarations))
        wordsInName = lang.trimLeadingWhitespace(dec[:commaIndex]).split(" ")
        varname = wordsInName[-1]
        value = lang.safeParseNum(dec[commaIndex:-2])
        writeToFile(str(varname) + " = " + str(value))
        writeToFile(str(varname) + "_stack = []")
        Assert(varname in lang.valid_names, "Non-Shakespearean variable name")
        vartable.add(varname)

# Gets all the names of scenes and acts, and adds them to the respective tables
# This must be done in a preprocessing step, in order to enable gotos to future acts/scenes
def parseAllActAndSceneDescriptions():
    global scene_names
    global act_names
    current_act = 0
    current_scene = 0
    scene_names = [{}]
    for line in src:
        if lang.beginsWithNoWhitespace(line, "Act"):
            desc = lang.getActOrSceneDescription(line)
            current_act += 1
            act_names[desc] = current_act
            scene_names.append(dict())
            current_scene = 0
        elif lang.beginsWithNoWhitespace(line, "Scene"):
            desc = lang.getActOrSceneDescription(line)
            current_scene += 1
            scene_names[current_act][desc] = current_scene

def getMathHelpers():
    s = ""
    f = open("include/mathhelpers.py", 'r')
    for line in f.readlines():
        s += line
    f.close()
    return s

def getGlobals():
    s = "global "
    for var in vartable:
        s += var + ", "
    return s[:-2]
    

#--------------------------------------------------------------------------#
#                            BEGIN MAIN PROGRAM                            #
#--------------------------------------------------------------------------#
Assert(len(sys.argv) > 1, "No input file")
filename = sys.argv[1]

f = open(filename, 'r')
src = f.readlines()
f.close()

#parse the title - all the text up until the first .
#title is unimportant and is thrown out
while src[N].find('.') < 0:
    N += 1
N += 1
#title is thrown out

writeToFile("#" + filename + "\n" + 
"#translated with pyspeare by Hunter Lightman, based off of splc.py (c) Sam Donow 2013-2014\n" + 
"import math\nimport sys\n" + 
"condition = 0\n")

writeToFile("#BASIC MATH FUNCTIONS")
writeToFile(getMathHelpers())

writeToFile("\n#START OF PROGRAM\n#DECLARATIONS")

handleDeclarations()
writeToFile("\n#SCRIPT")
parseAllActAndSceneDescriptions()

scenes = []
unfinished = False
while N < len(src):
    if lang.beginsWithNoWhitespace(src[N], 'Act'):
        Assert (lang.getActOrSceneNumber(src[N], 'Act') == actnum + 1, "Illegal Act numbering")
        if actnum > 0:
            writeScenes(scenes, False)
            scenes = []
        actnum += 1
        #act_names[lang.getActOrSceneDescription(src[N])] = actnum
        N += 1
    elif lang.beginsWithNoWhitespace(src[N], 'Scene'):
        Assert (lang.getActOrSceneNumber(src[N], 'Scene') == len(scenes) + 1, "Illegal Scene numbering")
        #scene_names[lang.getActOrSceneDescription(src[N])] = len(scenes) + 1
        N += 1
        speaker = ""
        target  = ""
        while (N < len(src)) and not (lang.beginsWithNoWhitespace(src[N], 'Scene') or lang.beginsWithNoWhitespace(src[N], 'Act')):
            if lang.beginsWithNoWhitespace(src[N], '['):
                parseEnterOrExit()
                if not unfinished:
                    scenes.append("\n")
                    unfinished = True
                N += 1
            elif src[N].find(':') >= 0:
                name = (src[N][:src[N].find(':')]).split(" ")[-1]
                Assert (name in stage, "An actor who is not on stage is trying to speak")
                for actor in stage:
                    if actor != name:
                        target = actor
                        speaker = name
                N += 1
                statements = getStatements()
                scenecode = ""
                for statement in statements:
                    scenecode += "\t" + parseStatement(statement) + "\n"
                if not unfinished:
                    scenes.append(scenecode)
                    unfinished = True
                else:
                    scenes[-1] += scenecode
            else:
                N += 1
        unfinished = False

    else:
        N += 1

writeScenes(scenes, True)
writeToFile("\tsys.exit()\n\nact_1_scene1()\n#FIN")