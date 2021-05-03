import sys
import os
import re

def groupByStrLength(fileList):
    dic = {}
    for item in fileList:
        dic.setdefault(len(item),[]).append(item)
    return dic.values()

def splitGroup(fileList):
    fileList.sort()
    digitFinderRegex = r"[\d]+"

    lastMatch, pre, post = None
    tmpNumList = []
    for item in fileList:
        match = re.search(digitFinderRegex, item)
        # found numbers in filename. lets find a pattern
        if match:
            if lastMatch:
                # compare filenames according to their numeric sections
                for i in match.groups():
                    for j in lastMatch[0].groups():
                        # trying to find a framerange-like pattern here
                        if i != j and len(i) == len(j):
                            index = item.find(i)
                            if pre and item[:index] == pre:
                                # we found a framerange-like pattern. add frame to the list
                                if post and item[index+len(i):] == post:
                                    tmpNumList.append(i)
                                    pre = item[:index]
                                    post = item[index+len(i):]
                                    lastMatch = (match, item)
                                # part after number is different than previous filename. print existing list
                                else:
                                    rangeStr, itemCount = getNumRangeStr(tmpNumList)
                                    padding = len(lastMatch[1]) - len(pre) - len(post)
                                    printRange(padding, itemCount, rangeStr, pre, post)
                                    pre, post, lastMatch = None
                                    tmpNumList = []
                            # part before number is different than previous file name. print existing list
                            else:
                                rangeStr, itemCount = getNumRangeStr(tmpNumList)
                                padding = len(lastMatch[1]) - len(pre) - len(post)
                                printRange(padding, itemCount, rangeStr, pre, post)
                                pre, post, lastMatch = None
                                tmpNumList = []
        # no numbers found in filename, print and forget about it
        else:
            print("1\t{}\n".format(item))


def getNumRangeStr(numbers):
    prevNum = None
    index = 0
    dic = {}
    
    numbers.sort()
    for num in numbers:
        if not prevNum and prevNum + 1 != num:
            index += 1
        dic.setdefault(index, []).append(num)
        prevNum = num

    rangeStr = ""
    itemCount = 0
    for itemList in dic.values():
        if len(itemList) == 1:
            rangeStr += "{} ".format(itemList[0])
        else:
            rangeStr += "{}-{} ".format(itemList[0], itemList[-1])
        itemCount += len(itemList)
    
    return rangeStr, itemCount

def printRange(padding, itemCount, rangeStr, pre, post):
    padding = "%0{}d".format(padding) if padding > 2 else "%d"
    print("{count}\t{pre}{padding}{post}\t{range}\n".format(count=itemCount, pre=pre, padding=padding, post=post, range=rangeStr))

def lss(fileNames):
    groupedFileNames = groupByStrLength(fileNames)
    for group in groupedFileNames:
        if len(group) == 1:
            print("1\t{}\n".format(group))
        else:
            splitGroup(group)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dirPath = "."
    elif len(sys.argv) == 2:
        dirPath = sys.argv[1]
    else:
        print("How to use. i.e. >>> lss /path/to/dir")
        sys.exit()

    if os.path.isdir(dirPath):
        fileNames = os.listdir(dirPath)
        lss(fileNames)
    else:
        print("Not a valid directory: {}".format(dirPath))
        sys.exit(1)