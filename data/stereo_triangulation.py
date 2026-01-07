import cv2 as cv
import numpy as np
from . import path_utils
import math

def triangulation(imgpointsL,imgpointsR,img):
    a=0.085
    Hsensor=4.61
    Vsensor=2.59

    dirData = path_utils.dirData()

    cv_file = cv.FileStorage()
    cv_file.open(dirData +  'stereo_rectification_map.xml', cv.FileStorage_READ)
    cameraL = cv_file.getNode('cameraL').mat()
    #cameraR = cv_file.getNode('cameraR').mat()

    temp = img.shape
    if len(temp)==3:
        img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    V,H = img.shape
    fx = cameraL[0,0]
    fy = cameraL[1,1]

    Hsensor = Hsensor / 1000
    Vsensor = Vsensor / 1000

    #Parametros del lente
    f_mmx = fx * (Hsensor/H)
    f_mmy = fy * (Vsensor/V)
    FOV_H = 2*math.degrees(math.atan(Hsensor/(2*f_mmx)))
    FOV_V = 2*math.degrees(math.atan(Vsensor/(2*f_mmy)))

    theta_H = (180-FOV_H)/2
    theta_V = (180-FOV_V)/2

    pointCloud = []

    for pointL,pointR in zip(imgpointsL,imgpointsR):
        d = abs(pointL[0]-pointR[0])
        #print(d)
        xi_H = theta_H + (pointL[0] * FOV_H) / H
        xi_V = theta_V + (pointR[1] * FOV_V) / V

        x = fx * a / d
        y = (x / math.tan(math.radians(xi_H)))+a/2
        z = x / math.tan(math.radians(xi_V))

        pointCloud.append([x,y,z])

    return pointCloud