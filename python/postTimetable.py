#Updates timetables on the database
#Andre Torres 25.01.2025

from parseTimetable import *
import requests
from definitions import BASE_URL

def uselessLayer(table):
    i=offset
    data=""
    for row in table:
        if row:
            for t in row:
                a=str(i)+":"+t
                if data=="":
                    data=a
                else:
                    data=data+","+a
        i+=1
    return data

url_GET=BASE_URL+"/API/exportLegs.php"
url_POST=BASE_URL+"/API/updateTimetable.php"

if __name__=="__main__":
    get = requests.get(url_GET, data = {},timeout=3)
    rc=get.status_code
    if rc!=200:
        print("ERROR getting data")
        exit(1)
    legs=get.json()
    #run through all legs
    for leg in legs:
        legObj = {'id': str(leg["id"])}
        raw1=parseHtml(leg["line"],leg["stop_from_direction"],leg["stop_from_idx"])
        raw2=parseHtml(leg["line"],leg["stop_to_direction"],leg["stop_to_idx"])
        table1=processTable(raw1)
        table2=processTable(raw2)
        data1=uselessLayer(table1)
        data2=uselessLayer(table2)
        legObj.update({"times_from": data1})
        legObj.update({"times_to": data2})
        post = requests.post(url_POST, data = legObj,timeout=3)
        rc=post.status_code
        if rc!=200:
            print("ERROR: id=",leg["id"],"rc=",rc)
