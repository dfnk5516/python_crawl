# Section02-2
# 파이썬 크롤링 기초
# urlopen  함수 기초 사용법

import urllib.request as req
from urllib.error import URLError, HTTPError


# 다운로드 경로 및 파일명
path_list = ['C:/test1.jpg', 'C:/index.html']

# 다운로드 리소스 url
target_url = ['http://blogfiles.naver.net/MjAxNzExMjZfMTc2/MDAxNTExNjY5Njk0Nzgx.Ab1d1dF2B7N32eiJg7M54Yzu51_hUUcr7u1_m-d2ERQg.5p30egP3gD9h3o0ghVg_mQ0IQYDUTwmp3QczmsyUix8g.JPEG.imuuri/godntalk_com_20170509_091945.jpg',
'http://naver.com']

for i, url in enumerate(target_url):
    # 예외 처리
    try:
        # 웹 수신 정보 읽기
        response = req.urlopen(url)
        #print(response.info())

        # 수신 내용
        contents = response.read()
        print('---------------------------------------')
        # 상태 정보 중간 출력
        print('Header Info-{}'.format(i, response.info()))
        print('HTTP Status Code : {}'.format(response.getcode()))
        print()
        print('---------------------------------------')

        with open(path_list[i], 'wb') as c: #write binary
            c.write(contents) 
    except HTTPError as e:
        print('Download failed')
        print('HTTPError Code : ', e.code)
    except URLError as e:
        print('Download failed')
        print('URL Error Reason : ', e.reason)
    else:
        print()
        print('Download Succed')