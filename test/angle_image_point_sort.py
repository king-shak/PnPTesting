import numpy as np
import cv2
import collections
import time

horizontal = [1., 0.]

# corners = np.array([
#     [211, 132],
#     [100, 141],
#     [108, 100],
#     [198, 94]
# ], dtype=np.float32)

corners = np.array([
    [211, 132],
    [199, 136],
    [114, 142],
    [100, 141],
    [108, 100],
    [123, 103],
    [186, 98],
    [198, 94]
], dtype=np.float32)

NUM_OF_CORNERS = len(corners)

def getPrincipalAxes(imgp):
    mean = np.empty((0))
    mean, eigen = cv2.PCACompute(imgp, mean)
    x = [eigen[0][0], eigen[1][0]]
    y = [eigen[0][1], eigen[1][1]]
    rotation = getAngle(horizontal, x, False)
    return x, y, np.ravel(mean), rotation

def rotatePoint(pt, angle):
    x = (pt[0] * np.cos(angle)) - (pt[1] * np.sin(angle))
    y = (pt[1] * np.cos(angle)) + (pt[0] * np.sin(angle))
    return [x, y]

def dot(a, b):     
    return (a[0] * b[0]) + (a[1] * b[1])

def norm(vector):
    return vector / np.linalg.norm(vector)

def getLength(vector):
    return np.sqrt((np.power(vector[0], 2) + np.power(vector[1], 2)))

def getAngle(a, b, mode = None):
    rotation = np.arccos(dot(a, b) / (getLength(a) * getLength(b)))
    if mode is not None:
        if (b[1] < 0):
            if mode:
                rotation = (2 * np.pi) - rotation
            else :
                rotation*=-1
    return rotation

def sortImgPts(imgpts, x, y, midpt, rotation):
    # angles = np.zeros(4, dtype=np.float32)
    # pts = np.zeros((4, 2), dtype=np.float32)
    # for i in range(len(imgpts)):
    #     pts[i] = norm([imgpts[i][0] - midpt[0], midpt[1] - imgpts[i][1]])
    #     angle = getAngle(pts[i], x) + rotation
    #     if (pts[i][1] < 0):
    #         angle = (2 * np.pi) - angle
    #     angles[i] =  angle

    # angles = np.zeros(4, dtype=np.float32)
    # pts = np.zeros((4, 2), dtype=np.float32)
    # for i in range(len(imgpts)):
    #     pts[i] = norm(rotatePoint([imgpts[i][0] - midpt[0], midpt[1] - imgpts[i][1]], -1 * rotation))
    #     angles[i] = getAngle(horizontal, pts[i], True)

    # # This is just for debugging
    # for i in range(len(imgpts)):
    #     print(np.degrees(angles[i]))

    pts = {}
    for i in range(len(imgpts)):
        pt = norm(rotatePoint([imgpts[i][0] - midpt[0], midpt[1] - imgpts[i][1]], -1 * rotation))
        angle = getAngle(horizontal, pt, True)
        pts[angle] = imgpts[i]
    
    pts = collections.OrderedDict(sorted(pts.items()))
    
    test = np.zeros((NUM_OF_CORNERS, 2), dtype=np.float32)
    j = 0
    for i in pts:
        test[j] = pts[i]
        j+=1

    return test

# start = time.time()
x, y, midPoint, rotation = getPrincipalAxes(corners)
corners = sortImgPts(corners, x, y, midPoint, rotation)
print(corners)
# end = time.time()
# print(end - start)