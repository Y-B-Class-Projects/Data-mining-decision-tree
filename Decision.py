import math
import json


def split(examples, used, trait):
    """
    examples is a list of lists. every list contains the attributes, the last item is the class. all items are 0/1.
    splits examples into two lists based on trait (attribute).
    updates used that trait was used.
    """
    newEx = [[], []]  # newEx is a list of two lists, list of Ex that Ex[trait]=0 and list of Ex that Ex[trait]=1
    if trait < 0 or trait > len(examples[0]) - 2 or used[trait] == 0:
        return newEx  # illegal trait
    for e in examples:
        newEx[e[trait]] += [e]
    used[trait] = 0  # used is a list that marks trait as used
    return newEx


def isSameClass(examples, Class):
    """
    returns 0 if all the examples are classified as 0.
    returns 1 if all the examples are classified as 1.
    returns 7  if there are no examples.
    returns -2 if there are more zeros than ones.
    returns -1 if there are more or equal ones than zeros.
    """
    if examples == []:
        return 11
    zo = [0] * 10  # zo is a counter of zeros and ones in class
    for e in examples:
        zo[e[-1]] += 1

    Sort = sorted(zo)
    if sum(Sort[:-1]) == 0 and Sort[-1] >= 1:
        return zo.index(Sort[-1])

    if Class == max(zo):
        return Class - 10
    return zo.index(max(zo)) - 10


def infoInTrait(examples, i):
    """
    calculates the information in trait i using Shannon's formula
    """
    count = [0] * 10, [0] * 10  # [no. of ex. with attr.=0 and clas.=0,no. of ex. with attr.=0 and clas.=1],
    # [no. of ex. with attr.=1 and clas.=0,no. of ex. with attr.=1 and clas.=1]
    for e in examples:
        count[e[i]][e[-1]] += 1
    x = 0
    # Shannon's formula
    for i in range(2):
        allI = sum([count[i][k] for k in range(10)])
        for j in range(10):
            if count[i][j] != 0 and count[i][j] != 0:
                x += count[i][j] * math.log(allI / count[i][j])
    return x


def minInfoTrait(examples, used):
    """
    used[i]=0 if trait i was already used. 1 otherwise.

    Returns the number of the trait with max. info. gain.
    If all traits were used returns -1.
    """
    minTrait = m = -1
    for i in range(len(used)):
        if used[i] == 1:
            info = infoInTrait(examples, i)
            if info < m or m == -1:
                m = info
                minTrait = i
    return minTrait


def build(examples, d):  # builds used
    used = [1] * (len(examples[0]) - 1)  # used[i]=1 means that attribute i hadn't been used
    return [recBuild(i, examples, used[:], 0, d) for i in range(10)]  # build 10 Binary treas for 10 digits


def recBuild(Class, examples, used, parentMaj, d):
    """
    Builds the decision tree.
    parentMaj = majority class of the parent of this node. the heuristic is that if there is no decision returns parentMaj
    """
    cl = isSameClass(examples, Class)
    if 0 <= cl <= 9:  # all is belong to only one class between 0 to 9
        return [[], cl == Class, []]
    if cl == 11:  # examples is empty
        return [[], parentMaj == Class, []]
    trait = minInfoTrait(examples, used)

    isClass = (cl + 10 == Class)

    if trait == -1:  # there are no more attr. for splitting
        return [[], isClass, []]  # cl+2 - makes cl 0/1 (-2+2 / -1+2)
    if d >= 0:
        x = split(examples, used, trait)
        left = recBuild(Class, x[0], used[:], cl + 10, d)
        right = recBuild(Class, x[1], used[:], cl + 10, d)
        return [left, trait, right]
    if d == 0:
        return [[], cl, []]


def recClassifier(dtree, traits):  # dtree is the tree, traits is an example to be classified
    if dtree[0] == []:  # there is no left child, means arrive to a leaf
        return dtree[1]
    return recClassifier(dtree[traits[dtree[1]] * 2], traits)  # o points to the left child, 2 points to the right child


def classifier(dtree, traits):  # same as the former without recursion
    while dtree[0] != []:
        dtree = dtree[traits[dtree[1]] * 2]
    return dtree[1]


def convertFile(filename, num):
    """
    Convert file from arff format to txt, and normalize the values.
    :param num: the amount of rows to read
    """
    f = open(filename, "r")
    cFileName = filename.split(".")[0] + "-converted.txt"
    cf = open(cFileName, "w+")

    line = f.readline()
    count = 0
    while count < num and line != 0:
        if not line.startswith('@'):
            count += 1
            line = line.split(',')
            cLine = []

            for pixel in line[:-1]:
                if int(pixel) < 130:
                    cLine.append(0)
                else:
                    cLine.append(1)
            cf.write(','.join([str(int) for int in cLine]) + "," + line[-1])
        line = f.readline()

    f.close()
    cf.close()


def buildclassifier(filename, d):
    e = []
    f = open(filename, "r")
    line = f.readline()
    while line != "":
        e.append([int(str) for str in line.split(',')])
        line = f.readline()

    f.close()
    return build(e, d)


e = [[1, 0, 0, 0, 0],
     [0, 1, 1, 0, 1],
     [1, 1, 1, 0, 0],
     [1, 1, 0, 1, 0],
     [0, 0, 1, 1, 1],
     [1, 0, 1, 1, 0],
     [1, 0, 0, 1, 1]]


def printTree(t, tab=0):
    if t:
        print(tab * '--', t[1])
        printTree(t[0], tab + 1)
        printTree(t[2], tab + 1)


def readFileToList(fileName):
    f = open(fileName, "r")
    line = f.readline()
    ret = []
    while line != "":
        ret.append(([int(Str) for Str in line.split(',')]))
        line = f.readline()
    return ret


def tester(tree, list):
    CountT = 0
    for l in list:
        classifyAs = classify(tree, l)
        if len(classifyAs) == 1 and classifyAs[0] == l[-1]:
            CountT += 1
    return 100 * CountT / len(list)


def classify(tree, list):
    ret = []
    for Class in range(10):
        if classifier(tree[Class], list):
            ret.append(Class)
    return ret


# t = build(e)
# printT(t[1])
# print(classifier(t[1], [1, 1, 1, 0]))

isLoadTreeFromFile = False

convertFile("digits-training.arff", 60000)
convertFile("digits-testing.arff", 10000)

if not isLoadTreeFromFile:
    tree = buildclassifier("digits-training-converted.txt", 20)
    with open("save.txt", "w+") as fp:
        json.dump(tree, fp)
else:
    with open("save.txt", "r") as fp:
        tree = json.load(fp)

testingList = readFileToList("digits-testing-converted.txt")
print(tester(tree, testingList))

