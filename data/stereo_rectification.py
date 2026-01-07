import cv2 as cv
import numpy as np
from . import path_utils # LO HICE ASÍ PORQUE ES PAQUETE, SOLO FUNCIONA LLAMANDOLO FUERA DE DATA
from os.path import exists


def run(imI,imD):
    dirData = path_utils.dirData()

    if exists(dirData + 'stereo_rectification_map.xml') == True:
        cv_file = cv.FileStorage()
        cv_file.open(dirData +  'stereo_rectification_map.xml', cv.FileStorage_READ)

        stereoMapL_x = cv_file.getNode('stereoMapL_x').mat()
        stereoMapL_y = cv_file.getNode('stereoMapL_y').mat()
        stereoMapR_x = cv_file.getNode('stereoMapR_x').mat()
        stereoMapR_y = cv_file.getNode('stereoMapR_y').mat()

        imD = cv.remap(imD, stereoMapR_x, stereoMapR_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)
        imI = cv.remap(imI, stereoMapL_x, stereoMapL_y, cv.INTER_LANCZOS4, cv.BORDER_CONSTANT, 0)

    return imI, imD
