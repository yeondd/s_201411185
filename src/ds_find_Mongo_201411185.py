#!/usr/bin/env python
# coding: utf-8
import pymongo
from pymongo import MongoClient
import src.ds_open_save_201411185 as gokr
import matplotlib.pyplot as plt
totalCount = []

def getData():
    gokr.getPeople()
    for YMD in gokr.DEAL_YMD:
	findMongo(YMD)
 
def findMongo(YMD):
    client = MongoClient()
    db = client.myProject
    collectionName = 'date_'+YMD
    collection = db[collectionName]
    findCount = collection.find({"totalCount":{"$gt": 0}})
    for i in findCount:
	totalCount.append(i['totalCount'])

def drawGraph():
    plt.stem(totalCount, linefmt='g:', markerfmt='ro', basefmt='g--')
    plt.stem(gokr.moving, linefmt='g:', markerfmt='bo', basefmt='g--') 
    plt.grid(True)
    plt.title('APT trading number go after population transition of Seoul', size = 30)
    plt.text(0 , 8700, 'total ATP trading', size = 20)
    plt.text(0 , -13000, 'population transition', size = 20)
    tick_date = gokr.DEAL_YMD 
    tick_n = range(len(gokr.DEAL_YMD))
    plt.xticks(tick_n, tick_date)
    xlab = 'DATE(201201 ~ '+gokr.DEAL_YMD[-1]+')'
    plt.xlabel(xlab, size = 20)
    plt.show()


if __name__ == "__main__":
    getData()
    drawGraph()    
 
