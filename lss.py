#!/usr/bin/python
#
# Copyright (C) 2021 by Burak Ertekin.
#
# Permission to use, copy, modify, and distribute this software and its
# documentation under the terms of the GNU General Public License is hereby
# granted. No representations are made about the suitability of this software
# for any purpose. It is provided "as is" without express or implied warranty.
# See the GNU General Public License for more details.
#

import sys
import os
import re

def groupByStrLength(fileList):
    """
    Group file list according to filename length.

    Returns list of file list groups.

    i.e. [['abc.txt', 'abd.txt'], ['file1.101.exr'], ['file1.102.2405.exr', 'file1.102.2406.exr', 'file1.102.2407.exr']]
    """
    dic = {}
    for item in fileList:
        dic.setdefault(len(item),[]).append(item)
    return dic.values()

def splitGroup(fileList):
    """
    Splitting grouped filenames according to numbers found in file.
    Iterates file list and compares filename with previous item, hence printing
    findings one item delayed.

    i.e. [1, 2, 3]
    Assign 1 to prevItem, check 2 with 1 if good add to list and assign 2 to prevItem,
    check 3 with 2 if good add to list and report. if bad report 1-2 as range then report 3
    as single.
    """
    fileList.sort()
    digitFinderRegex = r"([\d])+"

    prevItem = None
    tmpNumList = []
    tmpFileName = ""
    printed = False
    for item in fileList:
        numList = re.findall("[0-9]+", item)
        printed = False
        # found numbers in filename. lets find a pattern
        if numList:
            if prevItem:
                # check according to number element count in filename
                if len(numList) == len(prevItem[0]):
                    # same number elements count, now compare numList
                    for numIndex, i in enumerate(numList):
                        # found framerange like pattern. check filenames
                        j = prevItem[0][numIndex]
                        if i != j  and len(i) == len(j):
                            # matching pattern! add to tmp range list
                            if item.replace(i, j, 1) == prevItem[1]:
                                if not tmpFileName:
                                    padding = "%0{}d".format(len(i)) if len(i) > 1 else "%d"
                                    tmpFileName = item.replace(i, padding)
                                tmpNumList.append(i)
                                tmpNumList.append(j)
                                break
                            # not matching anymore. print the range
                            else:
                                printRange(tmpNumList, tmpFileName, prevItem)
                                printed = True
                                tmpNumList = []
                                tmpFileName = ""
                                break
                # number elements are not matching with previous item
                else:
                    if tmpNumList:
                        printRange(tmpNumList, tmpFileName, prevItem)
                        printed = True
                        tmpNumList = []
                        tmpFileName = ""
                # print missed single files
                if not printed and not tmpNumList:
                    print("1  {}".format(prevItem[1]))
                    printed = True
            prevItem = (numList, item)
        # no numList found in filename, print single file and forget about it
        else:
            print("1  {}".format(item))
            printed = True
            prevItem = None
    # filelist finished but didnt printed saved range
    if tmpNumList:
        printRange(tmpNumList, tmpFileName, prevItem)
    else:
        # if we printed in last round, it means we are missing the last item in list
        # since we are printing item delayed
        if printed:
            print("1  {}".format(prevItem[1]))

def getNumRangeStr(numbers):
    """
    Formatting given number list to a range format given in the task.

    i.e. [101, 102, 103, 105, 106, 108] >> 101-103 105-106 108
    """
    prevNum = None
    index = 0
    dic = {}

    numList = sorted(numbers)

    for num in numList:
        if prevNum and prevNum + 1 != int(num):
            index += 1
        dic.setdefault(index, []).append(num)
        prevNum = int(num)

    rangeStr = ""
    itemCount = 0
    for itemList in dic.values():
        if len(itemList) == 1:
            rangeStr += "{} ".format(int(itemList[0]))
        else:
            rangeStr += "{}-{} ".format(int(itemList[0]), int(itemList[-1]))
        itemCount += len(itemList)

    return rangeStr, itemCount

def printRange(numList, fileName, match):
    """
    Print formatted report.

    i.e. 4  file02_%04d.rgb      44-47
    """
    numList = set(numList)
    rangeStr, itemCount = getNumRangeStr(numList)
    print("{count}  {str}\t{range}".format(count=itemCount, str=fileName, range=rangeStr))


def lss(fileNames):
    """
    Main function. Group filenames by length and print according to item count of
    these groups.
    """
    groupedFileNames = groupByStrLength(fileNames)
    for group in groupedFileNames:
        if len(group) == 1:
            print("1  {}".format(group[0]))
        else:
            splitGroup(group)

if __name__ == '__main__':
    if len(sys.argv) == 1:
        dirPath = "."
    elif len(sys.argv) == 2:
        dirPath = sys.argv[1]
    else:
        print("How to use:\ni.e. >>> lss /path/to/dir\nIf no directory specified, it'll use current working dir.")
        sys.exit()

    if os.path.isdir(dirPath):
        fileNames = os.listdir(dirPath)
        lss(fileNames)
    else:
        print("Not a valid directory: {}".format(dirPath))
        sys.exit(1)