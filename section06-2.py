# Section06-2
# Selenium
# Selenium 사용 실습(2) - 실습 프로젝트(1)

# selenium 임포트
from selenium import webdriver
import time
from selenium.webdriver.common.by import By # 언제까지 기다리게할때
from selenium.webdriver.support.ui import WebDriverWait # 브라우저 로딩다될때까지 기다리게할때 by랑 같이 씀
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup

chrome_options = Options()
chrome_options.add_argument('--headless') #브라우저 실행안되게할때 쓰는 옵션

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

time.sleep(2)

# bs4 초기화
soup = BeautifulSoup(browser.page_source, 'html.parser')

# 소스코드 정리
# print(soup.prettify())

pro_list = soup.select('div.main_prodlist.main_prodlist_list > ul > li')

# 상품 리스트 확인
# print(pro_list)

# 필요 정보 추출
for v in pro_list:
    # 임시 출력
    # print(v)

    if not v.find('div', class_='ad_caster'):
        # 상품명, 이미지, 가격
        # print(v.select('p.prod_name > a')[0])
        print(v.select('p.prod_name > a')[0].text.strip())
        # print(v.select('a.thumb_link > img')[0]['data-original'])
        print(v.select('a.thumb_link > img')[0].attrs.get('data-original'))

        img_tag = v.select('a.thumb_link > img')[0]
        if "data-original" in img_tag.attrs.keys():
            print(img_tag['data-original'])
        else:
            print(img_tag['src'])
        print(v.select('p.price_sect > a')[0].text.strip())
    
    print()

# 브라우저 종료
browser.close()