#!/usr/bin/env python
# coding: utf-8
import os
import requests
import urlparse
import urllib
import src.mylib
import csv
import re
import pymongo
from pymongo import MongoClient
   
DEAL_YMD = []
moving = []
orimoving = []
localCode = []
localName = []
totalCount = []
urlList = []
aptParamList = []
_d=dict()

# get my service key
keyPath = os.path.join(os.getcwd(), 'src', 'key.properties')
key = src.mylib.getKey(keyPath)
keygokr = key['gokr']
    
def getPeople():
    temp = []
    # (1) open csv file(seoul people 201201~201501)
    path = os.path.join(os.getcwd(),'src', 'seoul_people.csv')
    f = open(path, 'r')
    csvReader = csv.reader(f)

    for row in csvReader:
        temp.append(row)
    f.close()

    # (2) make list
    for row in temp[0]:
        DEAL_YMD.append(row)
    for row in temp[1]:
	orimoving.append(row)
        moving.append(row)
    
    del(DEAL_YMD[0])
    del(moving[0])
    del(orimoving[0])
    del(temp)

def mkAptApiUrl(localCode, ym):
    # use API
    _url='http://openapi.molit.go.kr:8081/OpenAPI_ToolInstallPackage/service/rest/'
    
    # (1) service + operation
    SERVICE='RTMSOBJSvc'
    OPERATION_NAME='getRTMSDataSvcAptTrade'
    params1=SERVICE + '/' + OPERATION_NAME

    # (2) make query params
    for date in ym:
        _d['DEAL_YMD']=date
        for code in localCode:
            _d['LAWD_CD']=code
            params2 = urllib.urlencode(_d)
            params = params1+'?'+'serviceKey='+keygokr+'&'+params2
            aptParamList.append(params)

    # (3) make a full url
    for pa in aptParamList:
        url = urlparse.urljoin(_url,pa)
        # check the path mark
        url.replace('\\', '/')
        urlList.append(url)
    return urlList

def getAptCount():
    # (1) open code file
    path = os.path.join(os.getcwd(), 'src', 'LAWD_CD.txt')
    f = open(path, 'r')
    line = f.readlines()

    # and make local code
    for i in line:
        localCode.append((i.split('\t')[0]).strip())
        localName.append((i.split('\t')[1]).strip())
    f.close()

    # (2) make url
    url = mkAptApiUrl(localCode, DEAL_YMD)

    r = re.compile('<totalCount>(\d+)</totalCount>')
    YMDidx = 0 
    localNameidx = 0
    sum = 0
    for i, url_real in enumerate(url):
    # (3) open API
        data = requests.get(url_real).text
    # (4) get data by parsing
        res = r.findall(data)
	
	print "DATE: ", YMDidx, DEAL_YMD[YMDidx]  
	print "local Name: ", localNameidx, localName[localNameidx]  
	
	saveMongo(DEAL_YMD[YMDidx], localName[localNameidx], res[0])
	localNameidx = localNameidx + 1
	sum = sum + int(res[0])
		
	if (localNameidx >= len(localName)):
		saveMongo(DEAL_YMD[YMDidx], 'totalCount', sum)
		saveMongo(DEAL_YMD[YMDidx], 'movingPeople', moving[YMDidx])
		#updateMongo(DEAL_YMD[YMDidx], 'movingPeople', moving[YMDidx], orimoving[YMDidx])
		totalCount.append(sum)
		localNameidx = 0 
		YMDidx = YMDidx + 1
		sum = 0	

	print '\ttotal: ' + res[0] + '\n'
    del(url)
    return totalCount

def saveMongo(YMD, key, TotalCount):
    client = MongoClient()
    db = client.myProject
    collectionName = 'date_'+YMD
    collection = db[collectionName]
    db[collectionName].insert({
	key:TotalCount
    }) 

def updateMongo(YMD, key, predata, update):
    client = MongoClient()
    db = client.myProject
    collectionName = 'date_'+YMD
    collection = db[collectionName]
    db[collectionName].update(
	{key:predata}, {key:update}
    ) 

if __name__ == "__main__":
    getPeople()
    getAptCount()


