# Section02-1
# 파이썬 크롤링 기초
# urllib 사용법 및 기본 스크랩핑

import urllib.request as req

# 파일 url
img_url = 'https://postfiles.pstatic.net/20130815_44/qls456456_13765403568621Hn5Y_JPEG/1f106134fb4bb8ad4210f7db128beff7.jpg?type=w1'
html_url = 'http://google.com'

# 다운받을 경로
save_path1 = 'C:/test1.jpg'
save_path2 = 'C:/index.html'

# 예외 처리
try:
    file1, header1 = req.urlretrieve(img_url, save_path1)
    file2, header2 = req.urlretrieve(html_url, save_path2)
except Exception as e:
    print('Download failed')
    print(e)
else:
    # Header 정보 출력
    print(header1)
    print(header2)

    #다운로드 파일 정보
    print('Filename1 {}'.format(file1))
    print('Filename2 {}'.format(file2))
    print()

    #성공
    print('Download Succeed')