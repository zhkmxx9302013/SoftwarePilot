import sys
import csv
from sklearn.neighbors import NearestNeighbors
import numpy as np

imagedata = []
knndata = None


def readInData():
    global imagedata, knndata
    with open(sys.argv[1], 'rt', encoding="utf-8") as data:
        reader = csv.reader(data)
        imagedata.append(list(reader))

    imagedata = imagedata[0]
    knndata = np.genfromtxt(sys.argv[2], delimiter=',')

def findSamples(points):
    global imagedata
    samples = []
    for p in points:
        samples.append(imagedata[p])
    return samples

def getFeatures(image):
    feat = image[12][1:-1].split(',')
    knnfeat = ""
    for f in feat:
        knnfeat += str(f.split('=')[1]) + ','
    return np.fromstring(knnfeat[:-1], sep=',')

def findUGList(n):
    return [x / knndata[n][11] for x in knndata[n][12:16]]

def findDirection(ug, image):
    direct = -1
    nextPic = []
    for i in range(0,4):
        if ug[i] > direct:
            direct = ug[i]
            nextPic = image[i+4]
    return nextPic

def findNext(image):
    query = getFeatures(image)
    #print(query)
    nbors = NearestNeighbors(9)
    nbors.fit(knndata[:,0:11])
    knn = nbors.kneighbors([query[0:11]])
    knn = knn[1][0]
    dirs = [[0,0],[0,0],[0,0],[0,0]]
    for n in knn:
        ug = findUGList(n)
        for d in range(0,4):
            if(ug[d] > 0):
                dirs[d][0] += 1
                dirs[d][1] += ug[d]

    utilityGain = [d[1] / (d[0]-.00001) for d in dirs]

    gainMap = []
    for i in range (0,4):
        gainMap.append([utilityGain[i], image[i+4]])

    gainMap.sort(key=lambda gain: gain[0], reverse=True)
    return gainMap

def findUtil(currentIm):
    #print(currentIm)
    return float(currentIm[12].split(',')[11].split('=')[1][:-1])

def getImage(imID):
    for d in imagedata:
        if d[1] == imID:
            return d
    return []

def findTrace(im):
    image = im
    trace = []
    moves = []
    for i in range(0,10):
        gainMap = findNext(image)
        for i in range(0,4):
            try:
                image = getImage(gainMap[i][1])
                move = gainMap[i][1][1:-1].split(",")
                moves.append([int(move[0]),int(move[1])])
                break;
            except:
                pass
    for move in moves:
        start = im[1][1:-1].split(',')
        trace.append([int(move[0])-int(start[0]),int(move[1])-int(start[1])])

    return trace
if __name__ == '__main__':
    readInData()
    #find 10 sample points
    #sampleVec = [2000,2050,2100,2150,2200,2250,2300,2350,2400,2450]
    #sampleVec = [s + int(sys.argv[4]) for s in sampleVec]

    sampleVec = [i for i in range(1900,len(imagedata))]
    #print(r)

    #print(sampleVec)
    sampleImages = findSamples(sampleVec);
    threshold = float(sys.argv[3])

    wpoints = 0
    missions = 0

    trace = findTrace(sampleImages[0])
    #count = 0
    for image in sampleImages:
        if(missions % 10 == 0):
            try:
                trace = findTrace(image)
                #print(trace)
            except:
                pass
        start = image[1][1:-1].split(',')
        currentIm = image
        curUtil = findUtil(currentIm)
        count = 0
        for i in range(0,10):
            if curUtil > threshold:
                count += 1
                break;
            nextIm = [int(start[0]) - trace[i][0], int(start[1]) - trace[i][1]]
            currentIm = getImage(str(nextIm))
            try:
                curUtil = findUtil(currentIm)
            except:
                curUtil = 0
            if(currentIm == []):
                count = 10
                break;
            else:
                count += 1
        if count > -1:
            wpoints += count
            missions += 1
        print(count)

    print("Waypoints: "+str(wpoints) + " Missions: "+str(missions))
