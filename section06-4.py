# Section06-4
# Selenium
# Selenium 사용 실습(4) - 실습 프로젝트(3)

# selenium 임포트
from selenium import webdriver
import time
from selenium.webdriver.common.by import By # 언제까지 기다리게할때
from selenium.webdriver.support.ui import WebDriverWait # 브라우저 로딩다될때까지 기다리게할때 by랑 같이 씀
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
# 엑셀 처리 임포트
import xlsxwriter
# 이미지 바이트 처리
from io import BytesIO
import urllib.request as req

chrome_options = Options()
chrome_options.add_argument('--headless') #브라우저 실행안되게할때 쓰는 옵션

# 엑셀 처리 선언
workbook = xlsxwriter.Workbook('D:/crawling_result.xlsx')

# 워크 시트
worksheet = workbook.add_worksheet()

# webdriver 설정(Chrome, Firefox 등) - Headless 모드
browser = webdriver.Chrome('./webdriver/chrome/chromedriver.exe', options=chrome_options)

# webdriver 설정(Chrome, Firefox 등) - 일반 모드
# browser = webdriver.Chrome('./webdriver/chrome/chromedriver.exe')

# 크롬 브라우저 내부 대기
browser.implicitly_wait(5)

# 브라우저 사이즈
browser.set_window_size(1920, 1280)

# 페이지 이동
browser.get('http://prod.danawa.com/list/?cate=112758')

# 1차 페이지 내용
# print('Before Page Contents : {}'.format(browser.page_source))

# 제조사별 더 보기 클릭1
# Explicitly wait
WebDriverWait(browser, 3).until(EC.presence_of_element_located((By.XPATH,'//*[@id="dlMaker_simple"]/dd/div[2]/button[1]'))).click()

# 제조사별 더 보기 클릭2 #비권장
# Implicitly wait
# time.sleep(2) 
# browser.find_element_by_xpath('//*[@id="dlMaker_simple"]/dd/div[2]/button[1]').click()

# 원하는 모델 카테코리 클릭
WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.XPATH,'//*[@id="selectMaker_simple_priceCompare_A"]/li[20]/label'))).click()

# 2차 페이지 내용
# print('After Page Contents : {}'.format(browser.page_source))

# 2초간 대기
time.sleep(2)

# 현재 페이지
cur_page = 1

# 크롤링 페이지 수
target_crawl_num = 5

# 엑셀 행 수 
ins_cnt = 1

while cur_page <= target_crawl_num:


    # bs4 초기화
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # 소스코드 정리
    # print(soup.prettify())

    pro_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

    # 상품 리스트 확인
    # print(pro_list)

    # 페이지 번호 출력
    print('****** Current Page : {}'.format(cur_page), '******')
    print()

    # 필요 정보 추출
    for v in pro_list:
        # 임시 출력
        # print(v)

        if not v.find('div', class_='ad_caster'):
            # 상품명, 이미지, 가격
            prod_name = v.select('p.prod_name > a')[0].text.strip()
            prod_price = v.select('p.price_sect > a')[0].text.strip()

            # 이미지 요청 후 바이트 변환
            img_data = None

            # print(v.select('p.prod_name > a')[0])
            print(v.select('p.prod_name > a')[0].text.strip())
            # print(v.select('a.thumb_link > img')[0]['data-original'])
            print(v.select('a.thumb_link > img')[0].attrs.get('data-original'))

            img_tag = v.select('a.thumb_link > img')[0]
            if "data-original" in img_tag.attrs.keys():
                print(img_tag['data-original'])
                fakeReq = req.Request(img_tag['data-original'], headers={'User-Agent': 'Mozilla/5.0'})
                img_data = BytesIO(req.urlopen(fakeReq).read())
                worksheet.insert_image('C%s'% ins_cnt, prod_name, {'image_data' :img_data})
            else:
                print(img_tag['src'])
                fakeReq = req.Request(img_tag['src'], headers={'User-Agent': 'Mozilla/5.0'})
                img_data = BytesIO(req.urlopen(fakeReq).read())
                worksheet.insert_image('C%s'% ins_cnt, prod_name, {'image_data' :img_data})
            # print(v.select('p.price_sect > a')[0].text.strip())

            # 이 부분에서 엑셀 저장(파일, DB 등)

            # 엑셀 저장(텍스트)
            worksheet.write('A%s'% ins_cnt, prod_name)
            worksheet.write('B%s'% ins_cnt, prod_price)

            # 엑셀 저장(이미지)

            ins_cnt += 1
        print()
    print() 

    # 페이지 별 스크린 샷 저장
    browser.save_screenshot('D:/target_page{}.png'.format(cur_page))

    # 페이지 증가
    cur_page += 1
    
    if cur_page > target_crawl_num:
        print('Crawling Succed.')
        break
    # 페이지 이동 클릭
    WebDriverWait(browser, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div.number_wrap > a:nth-child({})'.format(cur_page)))).click()

    # BeautifulSoup 인스턴스 삭제
    del soup

    # 3초간 대기
    time.sleep(3)

# 브라우저 종료
browser.close()

# 엑셀 파일 닫기
workbook.close()