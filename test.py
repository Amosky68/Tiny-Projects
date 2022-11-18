from collections import Counter



def boxSomation(a : str , b:str) -> str :
    return a + b



def rowSomation(previousRaw : list) :
    if previousRaw is not None and previousRaw is not []:

        nextlen = len(previousRaw) - 1
        nextRow = []
        for i in range(nextlen):
            nextRow.append(boxSomation(previousRaw[i] , previousRaw[i+1]))

        return nextRow


def Tree(Base : list) -> str: 

    if Base is not None :
        compacted = Base
        for i in range(len(Base)-1):
            compacted = rowSomation(compacted)

        return compacted[0]

    else : return None  


def printing(StringValue : str) :

    container = Counter(StringValue)
    finalString = ''
    
    for key in container.keys() :
        print(f'{key:3} : {container[key]}')
        finalString += f'{container[key]}{key}+'

    finalString = finalString[:-1]
    print(finalString)




printing(Tree(Base = ['a','b','c','d','e','f','g','h']))

