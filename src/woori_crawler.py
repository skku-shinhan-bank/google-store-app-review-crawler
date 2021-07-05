from selenium import webdriver
import pandas as pd
import time
import re

class WooriCrawler:
    def __init__(self) -> None:
        pass

    # 스크롤 다운
    def scroll_down(driver):
        driver.execute_script("window.scrollTo(0, 999999999999)")
        time.sleep(1)

    def woori(self,driver, data):

        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            for n in range(4): 
                # (1) 4번의 스크롤링 
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);") 
                time.sleep(1.5)
                current_height = driver.execute_script("return window.scrollY")
                print('현재 위치',current_height)
            # (2) 더보기 클릭 
            elements = driver.find_elements_by_css_selector(".U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ.M9Bg4d")
            if len(elements) > 0:
                element = elements[0]
                driver.execute_script("arguments[0].click();", element)
            #(3) 종료 조건 
            new_height = driver.execute_script("return document.body.scrollHeight") 
            if new_height == last_height: 
                break 
            last_height = new_height

        reviewRootElements = driver.find_elements_by_xpath("//div[contains(@jsmodel, 'y8Aajc')]")
        for index, reviewRootElement in enumerate(reviewRootElements):
            if index % 10 == 0:
                print('영차영차 -', index)

            dates = reviewRootElement.find_elements_by_css_selector('.p2TkOb')
            user_names = reviewRootElement.find_elements_by_css_selector('.X43Kjb')
            star_grades = reviewRootElement.find_elements_by_xpath('//div[@class="pf5lIe"]/div[@role="img"]')
            reviews = reviewRootElement.find_elements_by_css_selector('.UD7Dzf')
            answer = reviewRootElement.find_elements_by_css_selector('.LVQB0b')

            tmp = []
            tmp.append(dates[0].text)
            tmp.append(user_names[0].text)
            tmp.append(star_grades[0].get_attribute('aria-label'))
            if len(reviews) > 0:
                tmp.append(reviews[0].text)
            else:
                tmp.append('')
            if len(answer) > 0:
                tmp.append(answer[0].text)
            else:
                tmp.append('')
            data.append(tmp)

        #print(tmp)
        print(len(data))
        return data

    def crawl(self):
        print('start')

        data = []

        # data 크롤링 해오기

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

        url="https://play.google.com/store/apps/details?id=com.wooribank.smart.npib&showAllReviews=true"
        #driver=webdriver.Chrome('C:\\chromedriver\\chromedriver.exe')
        driver.get(url)


        data=self.woori(driver, data)
        
        data.reset_index(inplace=True, drop=True)
        #data.head(100)
        data['별점'] = data['별점'].apply(lambda x: x[5:])
        m = re.compile('[0-9][\.0-9]*')
        data['별점'] = data['별점'].apply(lambda x : m.findall(x)[0])


        return data