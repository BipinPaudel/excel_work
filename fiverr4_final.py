import requests
import pandas as pd
from datetime import datetime


def readUrlsListFromFile(path):
    with open(path,'r',encoding='utf8') as f:
        lines= f.read().splitlines()
        return list(lines)

def prepareUrl(url):
    lists=url.split(':')
    if not lists[0].startswith('http'):
        return 'https://'+url
    return url

def getStatusCode(url):
    try:
        url= prepareUrl(url)
        r = requests.get(url)
        print(r.status_code)
        if r.status_code==200:
            return 'PASS'
        else:
            return 'FAIL'
    except requests.ConnectionError:
        print("failed to connect")
        return 'FAIL'
        
def statusCodeListFromUrlList(urlList):
    statusCodeList=[]
    for url in urlList:
        statusCodeList.append(getStatusCode(url))
    return statusCodeList


def writeFromL2InCsv(code_list,csvfile):
    df= pd.read_csv(csvfile)
    current_date=datetime.today().strftime('%d-%b')
    df=df.dropna(axis=0, how='all', thresh=None, subset=None, inplace=False).reset_index(drop=True)
    df[current_date]= pd.Series(code_list)
    df.to_csv(csvfile,index=False)

urlfile='urls.txt'
csvfile='CashFlow DQ Results.csv'

urlList=readUrlsListFromFile(urlfile)

statusCodeList= statusCodeListFromUrlList(urlList)

writeFromL2InCsv(statusCodeList,csvfile)


