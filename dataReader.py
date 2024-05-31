from urllib.request import urlopen
from urllib.request import urlretrieve
from pathlib import Path
import os
import scipy
import pandas as pd
import numpy as np
import csv
import json
import re
from collections import defaultdict
import matplotlib.pyplot as plt


# Web Functions

def checkForMatFiles(link, choice):
    noMatFiles = []
    
    if choice == 'year':
        pattern = r'/(\d{4})/'
        year = re.search(pattern, link).group(1)
        noMatFiles.append(downloadYearFolder(link, checking = True))
        if noMatFiles:
            with open(f'{year}MissingMatFiles', 'w') as fileOut:
                for link in noMatFiles:
                    fileOut.write(link)
    elif choice == 'month':
        pattern = r'/(\d{2})/'
        month = re.search(pattern, link).group(1)
        noMatFiles.append(downloadMonthFolder(link, checking = True))
        if noMatFiles:
            with open(f'{month}MissingMatFiles', 'w') as fileOut:
                for link in noMatFiles:
                    fileOut.write(link)
    elif choice == 'day':
        pattern = r'/(\d{2})/'
        day = re.search(pattern, link).group(1)
        noMatFiles.append(downloadDayFolder(link, checking = True))
        if noMatFiles:
            with open(f'{day}MissingMatFiles', 'w') as fileOut:
                for link in noMatFiles:
                    fileOut.write(link)
    else:
        print('Invalid Choice')



def downloadYearFolder(yearLink):
    page = urlopen(yearLink)
    html = page.read().decode('utf-8')

    pattern = r'href\s*=\s*["\']([^"\']+)["\']'
    links = re.findall(pattern, html)
    fullLinks = [f'{yearLink}{link}' for link in links]
    
    for link in fullLinks:
        downloadMonthFolder(link)
        
    
    
def downloadMonthFolder(monthLink):
    page = urlopen(monthLink)
    html = page.read().decode('utf-8')

    pattern = r'href\s*=\s*["\']([^"\']+)["\']'
    links = re.findall(pattern, html)
    fullLinks = [f'{monthLink}{link}' for link in links]
    
    for link in fullLinks:
        downloadDayFolder(link)


def downloadDayFolder(dayLink):
    page = urlopen(dayLink)
    html = page.read().decode('utf-8')

    pattern = r'href\s*=\s*["\']([^"\']+)["\']'
    links = re.findall(pattern, html)
    fullLinks = [f'{dayLink}{link}' for link in links]
    
    for link in fullLinks:
        downloadFile(link)


def downloadFile(fileLink):
    page = urlopen(fileLink)
    html = page.read().decode('utf-8')

    pattern = r'href\s*=\s*["\']([^"\']+\.mat)["\']'
    links = re.findall(pattern, html)
    fullLinks = [f'{fileLink}{link}' for link in links]

    if (not fullLinks):
        return fileLink
    else:
        i = 0
        for link in fullLinks:
            urlretrieve(f'{link}', f'C:\\Users\\imort\\OneDrive\\Documents\\Personal Projects\\VizLab\\dataReader\\matFiles\\{links[i]}')
            print(f'{link} has been successfully downloaded')
            i += 1
    

# Local Directory Functions

# WIP
def addToDirectory(fileName):
    if Path('directory.csv').exists():
        rows = []
        with open('directory.csv', 'r') as fileIn:
            reader = csv.reader(fileIn)
            header = next(reader)
            for row in reader:
                rows.append(row)
        with open('directory.csv', 'w', newline = '') as fileOut:
            writer = csv.writer(fileOut)
            writer.writerow(header)
            for row in rows:
                writer.writerow(row)
            _, extension = os.path.splitext(fileName)
            writer.writerow([extension, fileName])
    else:
        with open('directory.csv', 'w', newline = '') as fileOut:
            writer = csv.writer(fileOut)
            writer.writerow(['fileType', 'fileName'])
            _, extension = os.path.splitext(fileName)
            writer.writerow([extension, fileName])


# WIP
def displayLocalDirectory():
    with open('directory.csv', 'r') as fileIn:
        reader = csv.reader(fileIn)
        header = next(reader)
        fileName = header.index('fileName')
        fileList = []

        for row in reader:
            fileList.append(row[fileName])
        
        for fileName in fileList:
            print (fileName)


# Inspired by https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
class NumpyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, np.ndarray):
                return obj.tolist()
            elif isinstance(obj, np.void):
                return {name: obj[name] for name in obj.dtype.names}
            elif isinstance(obj, bytes):
                return obj.decode('utf-8')
            elif isinstance(obj, np.generic):
                return obj.item()
            return json.JSONEncoder.default(self, obj)

# Converts a .mat file into a JSON file and returns a dictionary containing the contents of the .mat file
def convertFile(fileInName):   
    with open(fileInName, 'r') as fileIn:
        fileContents = scipy.io.loadmat(fileInName)
        covisDict = {}
        covisDict['header'] = fileContents['__header__'].decode('utf-8')
        covisDict['version'] = fileContents['__version__']
        covisDict['globals'] = fileContents['__globals__']
        covis = fileContents['covis'][0][0]
        for name in covis.dtype.names:
            covisDict[name] = covis[name][0]
        
        print(f'{fileInName} has been converted')
        return covisDict
    

def createJSONFromFile(fileInName, fileOutName):
    with open(fileInName) as fileIn, open(fileOutName, 'w') as fileOut:
        json.dump(convertFile(fileInName), fileOut, indent = 4, cls = NumpyEncoder)
        print(f'Created JSON file for {fileInName}')

# WIP

def readCoords2D(fileInName):
    with open(fileInName) as fileIn:
        covisDict = convertFile(fileInName)
        xList = [x for x in covisDict['grid'][0][0][0]['x']]
        yList = [y for y in covisDict['grid'][0][0][0]['y']]
        vList = [v for v in covisDict['grid'][0][0][0]['v']]
        wList = [w for w in covisDict['grid'][0][0][0]['w']]
        coordsDict = {'xList': xList, 'yList': yList, 'vList': vList, 'wList': wList}



def loadJSONFile(fileInName):
    with open(fileInName) as fileIn:
        fileContents = json.loads(fileInName)
        # covisDict = np.asarray(fileContents["a"])
        return fileContents



# Menu and main method
def main():
    



main()