import json
import urllib.request
import pandas as pd

client_id = 'cTWUGiJR/GRNsWP1Zvpr6EfojgF2NzRo6pzKHUXZplHewa1M8A9dkuiqnqsbVFTvix8hc8GWw4abmLFx7YB5tA=='  # 공공데이터포탈 api key

def getRequestUrl(url):

    req = urllib.request.Request(url) # 서버에 보낼 요청객체를 생성

    try:
        response = urllib.request.urlopen(req) # 서버에 요청객체 req를 전달하여 응답을 받아 response에 저장
        if response.getcode() == 200: # 응답코드가 200이면 정상 호출
            # print('호출성공!!')
            ret = response.read().decode('utf-8')
            return ret
    except:
        # print('호출에러-호출에러코드:', response.getcode())
        # print('에러발생 주소:', url)
        print('더이상 가져올 데이터가 없거나 호출에 에러가 발생했습니다')
        return None

def getTourismStatsItem(yyyymm, national_code, ed_cd):
    baseUrl = "http://openapi.tour.go.kr/openapi/service" # 네이버 기본 api 주소

    service_url = baseUrl + '/EdrcntTourismStatsService'+'/getEdrcntTourismStatsList'

    params1 = "?serviceKey=" + client_id
    params2 = "&YM=" + yyyymm
    params3 = "&NAT_CD=" + national_code
    params4 = "&ED_CD=" + ed_cd
    params5 = "&_type=json"

    url = service_url + params1 + params2 + params3 + params4 + params5

    responseDecode = getRequestUrl(url)  # 호출성공시 디코딩된 응답 데이터를 저장
    if responseDecode == None:
        return None
    else:
        return json.loads(responseDecode)

def getTourismStatsService(nat_cd, ed_cd, nStartYear, nEndYear):

    data_flag = 0
    jsonResult = []
    return_list = []

    for year in range(nStartYear, nEndYear+1):
        for month in range(1, 13): # for(i=1;i<13:i++)
            if data_flag == 1:
                break
            yyyymm = "{0}{1:0>2}".format(year,month) # 예) 201501~201512 형식변환
            jsonData = getTourismStatsItem(yyyymm, nat_cd, ed_cd)
            # print(jsonData)
            if jsonData['response']['body']['items'] == '':
                data_flag = 1
                print('데이터가 끝났습니다.')
                print("출력데이터는 {0}년 {1}월 전까지 데이터입니다.".format(year,month))
                break

            natName = jsonData['response']['body']['items']['item']['natKorNm'] # 국가이름 추출
            num = jsonData['response']['body']['items']['item']['num'] # 방한외국관광객수
            # ed = jsonData['response']['body']['items']['item']['ed'] # 방한외래관광객

            jsonResult.append({'nat_name':natName, 'nat_cd':nat_cd, 'yyyymm':yyyymm, 'visit_cnt':num})

            return_list.append([natName,nat_cd,yyyymm,num])

    return (jsonResult, return_list, natName)

print('중국:1, 일본:2, 미국:3')
nat_num = input('내한관광객수를 알고 싶은 국가 번호를 입력하세요:')
if nat_num == '1':
    nat_code = 112
elif nat_num == '2':
    nat_code = 130
elif nat_num == '3':
    nat_code = 275

start_year = input('몇년 부터 수집할까요?:')
end_year = input('몇년 까지 수집할까요?:')

jsonResult, return_result, nat_name = getTourismStatsService(str(nat_code), 'E', int(start_year), int(end_year))

# print(jsonResult)
# print(return_result)
# print(nat_name)

result_df = pd.DataFrame(return_result, columns=['입국자국가','국가코드','입국날짜','입국자수'])
result_df.to_csv('[%s]내한관광통계.csv' % nat_name, index=False, encoding='cp949')