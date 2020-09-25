#!/usr/bin/python3

import os
import re
import glob
import time
import sys
from html.parser import HTMLParser
import base64
import simplejson
import math
import pathlib


if sys.getdefaultencoding() != 'utf-8':
    reload(sys)
    sys.setdefaultencoding('utf-8')

splashMatchKey = '{#splash}'
settingMatchKey = '{#settings}'
mainMatchKey = '{#main}'
configInternalMatchKey = '{#configInternal}'
configMainMatchKey = '{#configMain}'
engineMatchKey = '{#cocosengine}'
projectMatchKey = '{#project}'
resMapMatchKey = '{#resMap}'
ttfMapMatchKey = '{#ttfMap}'

fileByteList = ['.png', '.jpg', '.mp3', '.ttf', '.plist', 'txt']

base64PrefixList = {
    '.png': 'data:image/png;base64,',
    '.jpg': 'data:image/jpeg;base64,',
    '.mp3': '',
    '.ttf': '',
    '.plist': 'data:text/plist;base64,'
}


def clarifyFilename(path):
    path = os.path.abspath(path)
    print(path)
    return glob.glob(path)[0]


def read_in_chunks(filePath):
    extName = os.path.splitext(filePath)[1]
    if extName in fileByteList:
        file_object = open(filePath, 'rb')
        base64Str = base64.b64encode(file_object.read())
        base64Prefix = base64PrefixList[extName]
        if base64Prefix != None:
            base64Str = bytes(base64Prefix, 'utf-8') + base64Str
            return base64Str
    elif extName == '':
        return None

    file_object = open(filePath, encoding='utf-8')
    return file_object.read()


def writeToPath(path, data):
    with open(path, 'w', encoding='utf-8') as f:
        f.write(data)


def getResMap(jsonObj, path, resPath):
    fileList = os.listdir(path)
    for fileName in fileList:
        absPath = path + '/' + fileName

        if (os.path.isdir(absPath)):
            getResMap(jsonObj, absPath, resPath)
        elif (os.path.isfile(absPath) and not "main/index." in absPath):
            dataStr = read_in_chunks(absPath)
            if dataStr != None:
                absPath = absPath.replace(resPath + '/', '')
                jsonObj[absPath] = dataStr


def getResMapScript(resPath):
    jsonObj = {}
    getResMap(jsonObj, resPath, resPath)
    jsonStr = simplejson.dumps(jsonObj)
    resStr = str("window.resMap = ") + jsonStr
    return resStr

# This issue is fixed in Cocos Creator 2.x


def fixEngineError(engineStr):
    newEngineStr = engineStr.replace(
        "t.content instanceof Image", "t.content.tagName === \"IMG\"", 1)
    return newEngineStr


def addPlistSupport(mainStr):
    newMainStr = mainStr.replace(
        "json: jsonBufferHandler,", "json: jsonBufferHandler, plist: jsonBufferHandler,", 1)
    return newMainStr


def integrate(projectRootPath):
    htmlPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/index.html')
    pathlib.Path('./build/playable').mkdir(parents=True, exist_ok=True) 
    newHtmlPath = './build/playable/index.html'
    settingScrPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/src/settings.*js')
    mainScrPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/main.*js')
    engineScrPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/cocos2d-js-min.*js')
    projectScrPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/assets/main/index.*js')
    resPath = projectRootPath + '/build/web-mobile/assets'
    indexInternalScrPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/assets/internal/index.*js')
    splashScrPath = clarifyFilename(
        projectRootPath + '/build/web-mobile/splash*.png')
    configInternalFilename = os.path.basename(clarifyFilename(
        projectRootPath + '/build/web-mobile/assets/internal/config*.json'))
    configMainFilename = os.path.basename(clarifyFilename(
        projectRootPath + '/build/web-mobile/assets/main/config*.json'))

    htmlStr = read_in_chunks(htmlPath)
    settingsStr = read_in_chunks(settingScrPath)
    htmlStr = htmlStr.replace(settingMatchKey, settingsStr, 1)

    splashStr = read_in_chunks(splashScrPath).decode("utf-8")
    htmlStr = htmlStr.replace(splashMatchKey, splashStr, 1)

    projectStr = read_in_chunks(projectScrPath)
    htmlStr = htmlStr.replace(projectMatchKey, projectStr, 1)

    mainStr = read_in_chunks(mainScrPath)
    mainStr = addPlistSupport(mainStr)
    htmlStr = htmlStr.replace(mainMatchKey, mainStr, 1)

    htmlStr = htmlStr.replace(configInternalMatchKey, configInternalFilename, 1)
    htmlStr = htmlStr.replace(configMainMatchKey, configMainFilename, 1)

    engineStr = read_in_chunks(engineScrPath)
    engineStr = fixEngineError(engineStr)
    htmlStr = htmlStr.replace(engineMatchKey, engineStr, 1)

    resStr = getResMapScript(resPath)
    htmlStr = htmlStr.replace(resMapMatchKey, resStr, 1)

    writeToPath(newHtmlPath, htmlStr)

    targetFileSize = os.path.getsize(newHtmlPath)
    targetFileSizeInMegabyte = math.ceil(
        targetFileSize * 1000 / (1024 * 1024)) / 1000

    print("===================  All Done! =================== ")
    print("Target file = {}, with size {}M".format(
        newHtmlPath, targetFileSizeInMegabyte))


if __name__ == '__main__':
    workDir = os.getcwd() + ""
    integrate(workDir)
