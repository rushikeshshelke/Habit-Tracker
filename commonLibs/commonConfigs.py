from genericpath import isdir
import json
import os
import datetime

class CommonConfigs:
    
    def createDir(self,path):
        if os.path.isdir(path) == False:
            os.makedirs(path)
    
    def readJson(self,filename):
        with open(filename,'r') as file:
            return json.load(file)
    
    def getTodayDate(self):
        todayDate = datetime.datetime.today()
        
        return datetime.datetime(todayDate.year,todayDate.month,todayDate.day)