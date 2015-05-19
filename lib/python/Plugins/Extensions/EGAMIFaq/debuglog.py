import datetime
import os
import sys
import re
from Components.config import config
gLogFile = None
VERB_ERROR = 1
VERB_WARNING = 2
VERB_STARTING = 3
VERB_HIGHLIGHT = 4
VERB_ADDITIONAL = 5
VERB_CLOSING = 6
VERB_DEFAULT = 10
VERB_TOLOG = 20

def printlog(string, parent = None, verbLevel = VERB_DEFAULT):
    debugMode = 'Silent'
    type = 'I'
    if verbLevel == 'E':
        verbLevel = 1
        type = 'E'
    elif verbLevel == 'W':
        verbLevel = 2
        type = 'W'
    elif verbLevel == 'S':
        verbLevel = 3
        type = 'S'
    elif verbLevel == 'H':
        verbLevel = 4
        type = 'H'
    elif verbLevel == 'A':
        verbLevel = 5
        type = 'A'
    elif verbLevel == 'C':
        verbLevel = 6
        type = 'C'
    elif verbLevel == 'I':
        verbLevel = 10
        type = 'I'
    out = ''
    if parent is None:
        out = str(string)
    else:
        classname = str(parent.__class__).rsplit('.', 1)
        if len(classname) == 2:
            classname = classname[1]
            classname = classname.rstrip("'>")
            classname += '::'
            out = str(classname) + str(sys._getframe(1).f_code.co_name) + ' ' + str(string)
        else:
            classname = ''
            out = str(parent) + str(string)
    if verbLevel == VERB_ERROR:
        print '\x1b[1;41m' + '[MediaPortal] ' + 'E' + '  ' + str(out) + '\x1b[1;m'
        writeToLog(type, out)
    elif verbLevel == VERB_WARNING:
        print '\x1b[1;33m' + '[MediaPortal] ' + 'W' + '  ' + str(out) + '\x1b[1;m'
        writeToLog(type, out)
    elif verbLevel == VERB_STARTING and debugMode == 'High':
        print '\x1b[0;36m' + '[MediaPortal] ' + '\x1b[1;m' + '\x1b[1;32m' + 'S' + '  ' + str(out) + '\x1b[1;m'
        if debugMode != 'Silent':
            writeToLog(type, out)
    elif verbLevel == VERB_HIGHLIGHT and debugMode == 'High':
        print '\x1b[0;36m' + '[MediaPortal] ' + '\x1b[1;m' + '\x1b[1;37m' + 'H' + '  ' + str(out) + '\x1b[1;m'
        if debugMode != 'Silent':
            writeToLog(type, out)
    elif verbLevel == VERB_ADDITIONAL and debugMode == 'High':
        print '\x1b[0;36m' + '[MediaPortal] ' + '\x1b[1;m' + '\x1b[1;32m' + 'A' + '  ' + str(out) + '\x1b[1;m'
        if debugMode != 'Silent':
            writeToLog(type, out)
    elif verbLevel == VERB_CLOSING and debugMode == 'High':
        print '\x1b[0;36m' + '[MediaPortal] ' + '\x1b[1;m' + '\x1b[1;32m' + 'C' + '  ' + str(out) + '\x1b[1;m'
        if debugMode != 'Silent':
            writeToLog(type, out)
    elif verbLevel <= VERB_TOLOG:
        print '\x1b[0;36m' + '[MediaPortal] ' + 'I' + '  ' + '\x1b[1;m' + str(out)
        if debugMode != 'Silent':
            writeToLog(type, out)
    elif verbLevel > VERB_TOLOG:
        print '\x1b[0;36m' + '[MediaPortal] ' + 'only onScreen' + '  ' + str(out) + '\x1b[1;m'
    return


def writeToLog(type, out):
    global gLogFile
    if gLogFile is None:
        openLogFile()
    now = datetime.datetime.now()
    gLogFile.write('%02d:%02d:%02d.%07d ' % (now.hour,
     now.minute,
     now.second,
     now.microsecond) + str(type) + '  ' + str(out) + '\n')
    gLogFile.flush()
    return


def openLogFile():
    global gLogFile
    baseDir = '/tmp'
    logDir = baseDir + '/mediaportal'
    now = datetime.datetime.now()
    try:
        os.makedirs(baseDir)
    except OSError as e:
        pass

    try:
        os.makedirs(logDir)
    except OSError as e:
        pass

    gLogFile = open(logDir + '/MediaPortal_%04d%02d%02d_%02d%02d.log' % (now.year,
     now.month,
     now.day,
     now.hour,
     now.minute), 'w')
