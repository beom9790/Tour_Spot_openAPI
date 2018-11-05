import json
from Tour_Spot_Base import *

def Read_Tourist_Json():        ## 방문객 JSon 파일을 불러오는(읽는) 함수
    global sido, nStartYear, nEndYear

    total_tourist = []          ## 관광지 별 방문객 수 반환
    with open("%s_관광지입장정보_%d_%d.JSon"  % (sido, nStartYear, nEndYear-1), encoding='UTF8') as json_file:
        json_object = json.load(json_file)
        json_string = json.dumps(json_object)
        total_tourist = json.loads(json_string)

    return total_tourist

def Combination_Tourist():
    tour_spot = {}                   ## {관광지:방문객수} 담을 딕셔너리

    raw_data = Read_Tourist_Json()   ## 관광지 별 방문객 수 반환

    number_spot = 0                  ## 관광지 개수 - 변수 선언
    count = 0                        ## json 파일에 들어 있는 자료 개수
    for i in raw_data:
        count += 1

    number_spot = int(count / 12)    ## json 파일은 1~12월까지 있음 -> 12로 나눠 주면 관광지 개수가 됨

    for per_data in raw_data:
        ## tour_spot 딕셔너리에 해당 관광지가 없다면
        if not per_data['resNm'] in tour_spot:     ## resNm : 관광지명, ForNum : 외국인 방문객 수, NatNum : 내국인 방문객 수
            tour_spot[per_data['resNm']] = per_data['ForNum'] + per_data['NatNum']   ## 해당 {관광지:방문객수} 추가
        ## tour_spot 딕셔너리에 해당 관광지가 이미 있다면(json에 각 관광지마다 1~12월 각각 방문객이 있으므로, 모든 달의 방문객 수를 더함)
        else:
            tour_spot[per_data['resNm']] += per_data['ForNum'] + per_data['NatNum']  ## 해당 {관광지:방문객수} 추가

    ## {관광지:방문객수} 딕셔너리 반환
    return tour_spot