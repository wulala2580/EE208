import cv2
import numpy as np
from code import *
import os
import pickle as pk


def countMatchNumber(kp1, des1, data):
    res = 0
    KPDESlist = data["KPDESlist"]
    for i in range(len(KPDESlist)):
        des2 = KPDESlist[i]["des"]
        shape2 = KPDESlist[i]["gsize"]
        bf = cv2.BFMatcher()
        matches = bf.knnMatch(des1, des2, k=2)
        nice_match = []
        for m, n in matches:
            if m.distance < 0.75 * n.distance:
                nice_match.append([m])
        if len(nice_match) > res:
            res = len(nice_match)
    print("Matched Points:", res)
    return res


def showBestMatch(img_target, kp1, des1, dataID):
    f = open(dataID, "rb")
    data = pk.load(f)
    f.close()
    img_data = data["img"]
    imgName = data["filename"]
    print()
    print("Match Best: '{0}' ".format(imgName))
    KPDESlist = data["KPDESlist"]
    maxNum = 0
    maxID = 0
    bf = cv2.BFMatcher()
    for i in range(len(KPDESlist)):
        des2 = KPDESlist[i]["des"]
        shape2 = KPDESlist[i]["gsize"]
        matches = bf.knnMatch(des1, des2, k=2)
        nice_match = []
        for m, n in matches:
            if m.distance < 0.8 * n.distance:
                nice_match.append([m])
        if len(nice_match) > maxNum:
            maxNum = len(nice_match)
            maxID = i
    drawKPDES(img_target, kp1, des1, img_data, KPDESlist[maxID])


if __name__ == "__main__":
    tofind = "2.jpg"
    img_target_color = cv2.imread(tofind, cv2.IMREAD_COLOR)
    img_target = cv2.imread(tofind, cv2.IMREAD_GRAYSCALE)
    kp1, des1 = getKPandDES(img_target, 200)
    dataListName = []
    rootPath = "./dataset"
    print("Reading dataset ... ")
    for dirpath, dirnames, filenames in os.walk(rootPath):
        for filename in filenames:
            filename = os.path.join(dirpath, filename)
            if filename.endswith("pkl"):
                dataListName.append(filename)
    print("Done.")
    maxMatch = 0
    matchID = ""
    for dataname in dataListName:
        f = open(dataname, "rb")
        data = pk.load(f)
        f.close()
        # cv2.imshow("IMG", data["img"])
        # cv2.waitKey(0)
        imgName = data["filename"]
        print("Comparing with {0} ...".format(imgName))
        count = countMatchNumber(kp1, des1, data)
        if count > maxMatch:
            maxMatch = count
            matchID = dataname
    print()
    print("Number of Best Matched KPoints:", maxMatch)
    showBestMatch(img_target_color, kp1, des1, matchID)