# whMvmntEngAndMonVer1.py
# CompLing 2 Final Project
# Dwyer Bradley

# Make a class that lets us define leaves

class leaf:
    def __init__(self, value, content = "", leftChild = None, rightChild = None, isLandingSite = False, isWHel = False):
        self.value = value              # Name of leaf
        self.content = content          # Terminal node below a string (empty string = default)
        self.leftChild = leftChild      # Is this leaf the left child of its mother (default for only child) 
        self.rightChild = rightChild    # Is this leaf the right child of its mother
        # isLandingSite used to specify waiting area in Phase Edge
        self.isLandingSite = isLandingSite  # Is this leaf a Phase mvmnt landing site/specifier of Phase (True for yes; False for no = default)
        # isWHel used to indicate node for WH movement
        self.isWHel = isWHel            # Is this leaf the maximal projection of a wh element (True for yes; False for no = default)

#_____________________________________________________________________________________________________________________________________________________
# ENGLISH TEST TREE/S

# Define a tree for an English statement sentence
# "I cook it"
engCPasRoot = leaf("CP")

# CP left child
engCPasRoot.leftChild = leaf("DP", isLandingSite=True)
specCP = engCPasRoot.leftChild

# CP right child
engCPasRoot.rightChild = leaf("C'")
cBar = engCPasRoot.rightChild 

# cBar left child
cBar.leftChild = leaf("C")
c = cBar.leftChild

# cBar right child
cBar.rightChild = leaf("TP")
tp = cBar.rightChild

# TP left child
tp.leftChild = leaf("DP")
specTP = tp.leftChild

# TP right child
tp.rightChild = leaf("T'")
tBar = tp.rightChild

# tBar left child
tBar.leftChild = leaf("PAST")# needs tense here
t = tBar.leftChild

# tBar right child
tBar.rightChild = leaf("v*P")
lilvStarP = tBar.rightChild

# lilvStarP left child
lilvStarP.leftChild = leaf("DP", isLandingSite=True)
specLilvStarP = lilvStarP.leftChild

# lilvStarP right child
lilvStarP.rightChild = leaf("vP")
lilvP = lilvStarP.rightChild

# lilvP left child
lilvP.leftChild = leaf("DP", content="I") # needs subject here
speclilvP = lilvP.leftChild

# lilvP right child
lilvP.rightChild = leaf("v'")
lilvBar = lilvP.rightChild

# lilvBar left child
lilvBar.leftChild = leaf("v", content="cook") # needs verb here
lilv = lilvBar.leftChild

# lilvBar right child
lilvBar.rightChild = leaf("VP")
bigVP = lilvBar.rightChild

# bigVP left child
bigVP.leftChild = leaf("V")
bigV = bigVP.leftChild

# bigVP right child
bigVP.rightChild = leaf("DP", content="it", isWHel=True) # needs object here
dirObj = bigVP.rightChild

# Make list of all leaves
listOfLeaves = [engCPasRoot, specCP, cBar, c, tp, specTP, tBar, t, lilvStarP, specLilvStarP, lilvP, speclilvP, lilvBar, lilv, bigVP, bigV, dirObj]

# Define a function to find the WH element and make content wh word
def findWhEL(rootLeaf):
    whLeaf = None
    for leaf in listOfLeaves:
        if leaf.isWHel:
            whLeaf = leaf
            break
    
    if whLeaf:
        whLeaf.content = "what/who"
        whCopy = whLeaf.content
        return whCopy
    else:
        print("No WH element found.")
        return None

# Define a function for wh movement and leave copies
# Give it the whCopy returned above
def whMvtWithCopies(rootLeaf, whCopy):
    currentLeaf = rootLeaf

    if whCopy is None:
        print("whCopy is None; please fix before trying again.")
    else:
        # Traverse the tree in a depth-first manner
        leafBag = [currentLeaf]
        while leafBag:
            currentLeaf = leafBag.pop()

            if currentLeaf.isLandingSite:
                currentLeaf.content = whCopy

            if currentLeaf.rightChild:
                leafBag.append(currentLeaf.rightChild)

            if currentLeaf.leftChild:
                leafBag.append(currentLeaf.leftChild)


# Define a function for T to C movement and do-support
# Call with t leaf and c leaf
def t2cDoSupport(tNode, cNode):
    if tNode.value == "PAST":
        cNode.content = "did"
    elif tNode.value == "PRESENT":
        cNode.content = "do"
    elif tNode.value == "FUTURE":
        cNode.content = "will"
    else:
        print("Error in t2cdoSupport function: could not find tense.")

# Define a function for speclilvP to specTP movement
# Leave trace
def eppMvmnt(speclilvP, specTP):
    specTP.content = speclilvP.content + "_i"
    speclilvP.content = "t_i"



# Define function to collect content
def collectContent(rootLeaf):
    def traverseLeaf(leaf):
        grabBag = []

        if leaf.content != "":
            grabBag.append(leaf.content)

        if leaf.leftChild:
            grabBag.extend(traverseLeaf(leaf.leftChild))

        if leaf.rightChild:
            grabBag.extend(traverseLeaf(leaf.rightChild))

        grabBagLower = [] 
        [grabBagLower.append(item.lower) for item in grabBag]
        return grabBag

    return traverseLeaf(rootLeaf)

# Define a function to give the string and tree for the first eng test tree
def mainEngOne():
    # Define a function to spell out tree
    def spellOutEngString():
        whCopy = findWhEL(engCPasRoot)
        whMvtWithCopies(engCPasRoot, whCopy)
        t2cDoSupport(t, c)
        eppMvmnt(speclilvP, specTP)

        # Put wh elements not pronounced at PF in parantheses

        grabBagPF = []
        for item in collectContent(engCPasRoot):
            if item == whCopy and item in grabBagPF:
                grabBagPF.append("(" + item + ")")
            else:
                grabBagPF.append(item)

        outputString = " ".join(grabBagPF)
        print(outputString)

    def spellOutEngTree(rootLeaf):
        if not rootLeaf:
            return ""

        children = [rootLeaf.leftChild, rootLeaf.rightChild]
        childrenStructure = ' '.join(spellOutEngTree(child) for child in children if child)

        if childrenStructure:
            content = f" ({rootLeaf.content})" if rootLeaf.content else ""
            return f"{rootLeaf.value}{content} \n[{childrenStructure}]"
        else:
            content = f" ({rootLeaf.content})" if rootLeaf.content else ""
            return f"{rootLeaf.value}{content}"
        
    spellOutEngString()
    print("   \n")
    print(spellOutEngTree(engCPasRoot))
    print("   \n")

#mainEngOne()

#__________________________________________________________________________________________________
# MON TEST TREE/S

# Define a tree for a Mon sentences 11a, 11b, and 12 from Gould 2021
# 11a) who MC think ASP      CM see what Q
# 11b) who MC think ASP what CM see      Q
# 12)  who MC think ASP who  CM see who  Q

monCPasRoot = leaf("CP")

# Matrix CP left child
monCPasRoot.leftChild = leaf("DP", isLandingSite= True)
specMatrixCP = monCPasRoot.leftChild

# Matrix CP right child
monCPasRoot.rightChild = leaf("C'")
matrixCBar = monCPasRoot.rightChild

# matrix CBar left child
matrixCBar.leftChild = leaf("TP")
matrixTP = matrixCBar.leftChild

# matrix CBar right child
matrixCBar.rightChild = leaf("C", content="Q")
matrixC = matrixCBar.rightChild

# matrix TP left child
matrixTP.leftChild = leaf("DP")
specMatrixTP = matrixTP.leftChild

# matrix TP right child
matrixTP.rightChild = leaf("T'")
matrixTBar = matrixTP.rightChild

# matrix TBar left child
matrixTBar.leftChlid = leaf("T")
matrixT = matrixTBar.leftChild

# matrix TBar right child
matrixTBar.rightChild = leaf("vP")
matrixLilvP = matrixTBar.rightChild

# matrix little vP left child
matrixLilvP.leftChild = leaf("DP", content="MC")
specMatrixLilvP = matrixLilvP.leftChild

# matrix little vP right child
matrixLilvP.rightChild = leaf("v'")
matrixLilvBar = matrixLilvP.rightChild

# matrix little vBar left child
matrixLilvBar.leftChild = leaf("v")
matrixLilv = matrixLilvBar.leftChild

# matrix little vBar right child
matrixLilvBar.rightChild = leaf("VP")
matrixBigVP = matrixLilvBar.rightChild

# matrix big VP left child
matrixBigVP.leftChild = leaf("V'")
matrixBigVBar = matrixBigVP.leftChild

# matrix big VP right child
matrixBigVP.rightChild = leaf("CP")
subCP = matrixBigVP.rightChild

# matrix big VBar left child
matrixBigVBar.leftChild = leaf("V", content="think")
matrixBigV = matrixBigVBar.leftChild

# matrix big Vbar right child
matrixBigVBar.rightChild = leaf("Aspect", content="ASP")
matrixAspect = matrixBigVBar.rightChild

### Subordinate clause

# subordinate CP left child
subCP.leftChild = leaf("DP", isLandingSite= True)
specSubCP = subCP.leftChild

# subordinate CP right child
subCP.rightChild = leaf("C'")
subCBar = subCP.rightChild

# sub CBar left child
subCBar.leftChild = leaf("TP")
subTP = subCBar.leftChild

# sub CBar right child
subCBar.rightChild =leaf("C")
subC = subCBar.rightChild

# sub TP left child
subTP.leftChild = leaf("DP")
specSubTP = subTP.leftChild

# sub TP right child
subTP.rightChild = leaf("T'")
subTBar = subTP.rightChild

# sub TBar left child
subTBar.leftChild = leaf("T")
subT = subTBar.leftChild

# sub TBar right child
subTBar.rightChild = leaf("v*P")
sublilvStarP = subTBar.rightChild

# sub v*P left child
sublilvStarP.leftChild = leaf("DP", isLandingSite= True)
specSublilvStar = sublilvStarP.leftChild

# sub v*P right child
sublilvStarP.rightChild = leaf("vP")
subLilvP = sublilvStarP.rightChild

# sub little vP left child
subLilvP.leftChild = leaf("DP", content= "CM")
specSubLilvP = subLilvP.leftChild

# sub little vP right child
subLilvP.rightChild = leaf("v'")
subLilvBar = subLilvP.rightChild

# sub little vBar left child
subLilvBar.leftChild = leaf("v")
subLilv = subLilvBar.leftChild

# sub little vBar right child
subLilvBar.rightChild = leaf("VP")
subBigVP = subLilvBar.rightChild

# sub big VP left child
subBigVP.leftChild = leaf("V", content="see")
subBigV = subBigVP.leftChild

# sub big VP right child
subBigVP.rightChild = leaf("DP", content= "what/who", isWHel= True)
monDirObj = subBigVP.rightChild

# Make list of all leaves
listOfLeavesMon = [monCPasRoot, specMatrixCP, matrixCBar, matrixTP, matrixC,\
                    specMatrixTP, matrixTBar, matrixT, matrixLilvP,\
                          specMatrixLilvP, matrixLilvBar, matrixLilv, matrixBigVP,\
                              matrixBigVBar, subCP, matrixBigV, matrixAspect,\
                                  specSubCP, subCBar, subTP, subC, specSubTP, subTBar,\
                                      subT, sublilvStarP, specSublilvStar, subLilvP,\
                                          subLilvBar, subLilv, subBigVP, subBigV, monDirObj, specSubLilvP]

def mainMonOne(exampleNumber):
    # Define a function to spell out string
    def spellOutMonString():
        #print("collectContent = ", collectContent(monCPasRoot))

        # Put wh elements not pronounced at PF in parantheses on tree
        # Three versions for 11a, 11b, and 12 from Gould 2021

        # 11a) wh copies overt at matrix CP spec and in original position
        if exampleNumber == "11a":
            specMatrixCP.content = "what/who"
            specSubCP.content = "(what/who)"
            specSublilvStar.content = "(what/who)"
            monDirObj.content = "what/who"

            eppMvmnt(specMatrixLilvP, specMatrixTP)
            eppMvmnt(specSubLilvP, specSubTP)

            outputString11a = " ".join(collectContent(monCPasRoot))
            print("11a: ")
            print(outputString11a)

        # 11b) wh copies overt in both CP specs
        if exampleNumber == "11b":
            specMatrixCP.content = "what/who"
            specSubCP.content = "what/who"
            specSublilvStar.content = "(what/who)"
            monDirObj.content = "(what/who)"

            eppMvmnt(specMatrixLilvP, specMatrixTP)
            eppMvmnt(specSubLilvP, specSubTP)

            outputString11b = " ".join(collectContent(monCPasRoot))
            print("11b: ")
            print(outputString11b)

        # wh copies overt everywhere except spec of little v*P
        if exampleNumber == "12":
            specMatrixCP.content = "what/who"
            specSubCP.content = "what/who"
            specSublilvStar.content = "(what/who)"
            monDirObj.content = "what/who"

            eppMvmnt(specMatrixLilvP, specMatrixTP)
            eppMvmnt(specSubLilvP, specSubTP)

            outputString12 = " ".join(collectContent(monCPasRoot))
            print("12: ")
            print(outputString12)
        
    # Define a function to show tree structure
    def spellOutMonTree(rootLeaf):
        if not rootLeaf:
            return ""

        children = [rootLeaf.leftChild, rootLeaf.rightChild]
        childrenStructure = ' '.join(spellOutMonTree(child) for child in children if child)

        if childrenStructure:
            content = f" ({rootLeaf.content})" if rootLeaf.content else ""
            return f"{rootLeaf.value}{content} \n[{childrenStructure}]"
        else:
            content = f" ({rootLeaf.content})" if rootLeaf.content else ""
            return f"{rootLeaf.value}{content}"

    whMvtWithCopies(monCPasRoot, "whCopy")   
    spellOutMonString()
    print("   \n")
    print(spellOutMonTree(monCPasRoot))
    print("   \n")

#mainMonOne("11a")
#mainMonOne("11b")
#mainMonOne("12")

def main():
    print("Hello, I can show you examples of WH-movement in English (one overt copy)")
    print("or in Mon (multiple overt copies).")
    xyz = input("Enter: 'English' or 'Mon' to continue")

    if xyz.lower() == "english":
        print("Here is an example of WH-movement in English.")
        print("Elements in parentheses are covert copies:")
        mainEngOne()

    elif xyz.lower() == "mon":
        print("Examples for Mon are based on data from Gould 2021")
        print("Enter '11a', '11b', or '12' to see WH-movement for the")
        abc = input("corresponding data")
        if abc.lower() == "11a":
            mainMonOne("11a")
        elif abc.lower() == "11b":
            mainMonOne("11b")
        elif abc.lower() == "12":
            mainMonOne("12")

    else:
        print("I'm sorry, I don't understand. Please try again.")

main()
    