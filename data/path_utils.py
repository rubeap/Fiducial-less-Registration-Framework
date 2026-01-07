import os
import sys

def dirData():

    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirData = generalDir + "\\data\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirData = generalDir + "/data/"
    elif sys.platform.startswith('darwin'):
        dirData = generalDir + "/data/"

    return dirData

def dirProfiles():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirProfiles = generalDir + "\\profiles\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirProfiles = generalDir + "/profiles/"
    elif sys.platform.startswith('darwin'):
        dirProfiles = generalDir + "/profiles/"

    return dirProfiles

def dirLanguages():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirLanguages = generalDir + "\\languages\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirLanguages = generalDir + "/languages/"
    elif sys.platform.startswith('darwin'):
        dirLanguages = generalDir + "/languages/"

    return dirLanguages

def dirResults():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirResults = generalDir + "\\results\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirResults = generalDir + "/results/"
    elif sys.platform.startswith('darwin'):
        dirResults = generalDir + "/results/"

    return dirResults

def dirImg():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirImg = generalDir + "\\img\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirImg = generalDir + "/img/"
    elif sys.platform.startswith('darwin'):
        dirImg = generalDir + "/img/"

    return dirImg

def dirCalibI():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirCalibI = generalDir + "\\img\\calibI\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirCalibI = generalDir + "/img/calibI/"
    elif sys.platform.startswith('darwin'):
        dirCalibI = generalDir + "/img/calibI/"

    return dirCalibI

def dirCalibD():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirCalibD = generalDir + "\\img\\calibD\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirCalibD = generalDir + "/img/calibD/"
    elif sys.platform.startswith('darwin'):
        dirCalibD = generalDir + "/img/calibD/"

    return dirCalibD

def dirScope():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirScope = generalDir + "\\data\\scope\\data\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirScope = generalDir + "/data/scope/data/"
    elif sys.platform.startswith('darwin'):
        dirScope = generalDir + "/data/scope/data/"

    return dirScope

def dirScopeSS():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirScopeSS = generalDir + "\\data\\scope\\screenshots\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirScopeSS = generalDir + "/data/scope/screenshots/"
    elif sys.platform.startswith('darwin'):
        dirScopeSS = generalDir + "/data/scope/screenshots/"

    return dirScopeSS

def dirMasks():
    generalDir = os.getcwd()

    if sys.platform.startswith('win'):
        dirMasks = generalDir + "\\data\\masks\\"
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        dirMasks = generalDir + "/data/masks/"
    elif sys.platform.startswith('darwin'):
        dirMasks = generalDir + "/data/masks/"

    return dirMasks