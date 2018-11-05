import urllib.request
import datetime
import json
import math
from Tour_Analysis import *

access_key = "mCMm44itfuyVU%2BFbA2UfUkg5e0mhiGe8cfc9MeGkjna99yT90ezvAOPMqZnYBczZRSliXsaBpyfIV9ic1Bpjmw%3D%3D"

sido = '서울특별시'
gungu = ''
nStartYear = 2017
nEndYear = 2018

def get_request_url(url):
    req = urllib.request.Request(url)

    try:
        response = urllib.request.urlopen(req)
        if response.getcode() == 200:
            print("[%s] Url Request Success" % datetime.datetime.now())
            return response.read().decode('utf-8')
    except Exception as e:
        print(e)
        print("[%s] Error for URL : %s" % (datetime.datetime.now(), url))
        return None

# [CODE 1]
def getTourPointVisitor(yyyymm, sido, gungu, nPagenum, nItems):

    end_point = "http://openapi.tour.go.kr/openapi/service/TourismResourceStatsService/getPchrgTrrsrtVisitorList"

    parameters = "?_type=json&serviceKey=" + access_key
    parameters += "&YM=" + yyyymm
    parameters += "&SIDO=" + urllib.parse.quote(sido)
    parameters += "&GUNGU=" + urllib.parse.quote(gungu)
    parameters += "&RES_NM=&pageNo=" + str(nPagenum)
    parameters += "&numOfRows=" + str(nItems)

    url = end_point + parameters
    retData = get_request_url(url)
    if (retData == None):
        return None
    else:
        return json.loads(retData)

# [CODE 2]
def getTourPointData(item, yyyymm, jsonResult):
    addrCd = 0 if 'addrCd' not in item.keys() else item['addrCd']        # 지역 코드
    gungu = '' if 'gungu' not in item.keys() else item['gungu']          # 시군구
    sido = '' if 'sido' not in item.keys() else item['sido']             # 시도
    resNm = '' if 'resNm' not in item.keys() else item['resNm']          # 관광지
    rnum = 0 if 'rnum' not in item.keys() else item['rnum']              # 관광지 인덱스
    ForNum = 0 if 'csForCnt' not in item.keys() else item['csForCnt']    # 외국인 방문객 수
    NatNum = 0 if 'csNatCnt' not in item.keys() else item['csNatCnt']    # 내국인 방문객 수

    jsonResult.append({'yyyymm':yyyymm, 'addrCd':addrCd, 'gungu':gungu, 'sido':sido,
                       'resNm':resNm, 'rnum':rnum, 'ForNum':ForNum, 'NatNum':NatNum})

    return

def main():
    global sido, gungu, nStartYear, nEndYear

    jsonResult = []
    nPagenum = 1
    nTotal = 0
    nItems = 100

    for year in range(nStartYear, nEndYear):
        for month in range(1, 13):
            yyyymm = "{0}{1:0>2}".format(str(year), str(month))
            nPagenum = 1

            # [CODE 3]
            while True:
                jsonData = getTourPointVisitor(yyyymm, sido, gungu, nPagenum, nItems)

                if (jsonData['response']['header']['resultMsg'] == 'OK'):
                    nTotal = jsonData['response']['body']['totalCount']

                    if nTotal == 0:
                        break

                    for item in jsonData['response']['body']['items']['item']:
                        getTourPointData(item, yyyymm, jsonResult)

                    nPage = math.ceil(nTotal / 100)

                    if (nPagenum == nPage):
                        break

                    nPagenum += 1

                else:
                    break

    with open('%s_관광지입장정보_%d_%d.JSon' % (sido, nStartYear, nEndYear-1), 'w', encoding='utf8') as outfile:
        retJson = json.dumps(jsonResult, indent=4, sort_keys=True, ensure_ascii=False)
        outfile.write(retJson)

    print('%s_관광지입장정보_%d_%d.JSon SAVED' % (sido, nStartYear, nEndYear-1))

    Make_Graph()

if __name__ == '__main__':
    main()
