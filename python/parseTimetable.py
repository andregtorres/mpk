#Parse timetables from MPK website
#Andre Torres 25.01.2025

import urllib.request
import requests
from bs4 import BeautifulSoup as bs
from http.cookiejar import CookieJar

offset=5 #5am = idx 0
cj = CookieJar()
def parseHtml(line,direction,stop, verbose=False):
    data_raw=[]
    table_idx=15
    tries =0
    n=0
    base_url = "http://rozklady.mpk.krakow.pl/?lang=EN&linia="
    url = base_url+str(line)+"__"+str(direction)+"__"+str(stop)
    while tries < 2 and n<=10:
        tries+=1
        try:
            req=urllib.request.Request(url, None, {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; G518Rco3Yp0uLV40Lcc9hAzC1BOROTJADjicLjOmlr4=) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8','Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3','Accept-Encoding': 'gzip, deflate, sdch','Accept-Language': 'en-US,en;q=0.8','Connection': 'keep-alive'})
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
            page = opener.open(req)
            soup = bs(page.read(), "html.parser")
            page.close()
            n=len(soup.find_all("table"))
            table=soup.find_all("table")[table_idx]
            rows = table.find_all('tr')
            for row in rows[1:-2]:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                data_raw.append([ele for ele in cols if ele]) # Get rid of empty values
        except:
            if verbose:
                print("try {} - Error parsing HTML".format(tries))
            else:
                pass
    return data_raw

def processTable(raw,day=0):
    '''
    processes the output of parlseHtml()
    day is 0 for weekday, 1 for saturday, 2 for sunday
    this might be vunerable to a bus that does not operate on week or saturday
    for a given hour
    '''
    data=[None]*(25-offset) #25 because the timetables have the 0 hour after 24
    if day>2:
        day=0
    i=offset
    for row in raw:
        if len(row)>(1+day):
            j=int(row[0])
            if j>=i:
                timesString=row[day+1]
                data[j-offset]=timesString.split(" ")
                if j==i:
                    i+=1
                else:
                    i = j +1
    return data

if __name__ == "__main__":
    raw1=parseHtml(140,1,1,True)
    raw2=parseHtml(105,1,1,True)
    print(raw1)
    print(processTable(raw1))
    print(processTable(raw2,1))
