def square(x):
    return x * x
    
def cube(x):
    return x * x * x
    
def twice(x):
    return 2 * x
    
def getChar():
    r = 0
    try:
        r = ord(str(raw_input())[0])
    except:
        r = -1
    return r