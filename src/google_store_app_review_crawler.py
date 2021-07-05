from selenium import webdriver
import time

class GoogleStoreAppReviewCrawler:
    def __init__(self) -> None:
        pass
    
    def crawl(self, store_url):
        data = []

        print('Initialize Drive')
        driver = self.initDrive(store_url)

        print('Start Scrpll')
        self.scrollToEnd(driver)

        print('Start parsing')
        data = self.parse(driver)

        print('data 수:', len(data))

        return data

    def initDrive(self, store_url):
        chrome_options = webdriver.ChromeOptions()

        chrome_options.add_argument('--headless') #내부 창을 띄울 수 없으므로 설정

        chrome_options.add_argument('--no-sandbox')

        chrome_options.add_argument('--disable-dev-shm-usage')

        driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
        driver.get(store_url)

        return driver
    
    def scrollToEnd(self, driver):
        # Get scroll height  
        last_height = driver.execute_script("return document.body.scrollHeight")   

        SCROLL_PAUSE_TIME = 1.5


        while True:
            # Scroll down to bottom  
            for n in range(4):                                                  
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                current_height = driver.execute_script("return window.scrollY")
                print('현재 위치',current_height)
                time.sleep(SCROLL_PAUSE_TIME)
            
            elements = driver.find_elements_by_css_selector(".U26fgb.O0WRkf.oG5Srb.C0oVfc.n9lfJ.M9Bg4d")
            if len(elements) > 0:
                element = elements[0]
                driver.execute_script("arguments[0].click();", element)

            # Calculate new scroll height and compare with last scroll height            
            new_height = driver.execute_script("return document.body.scrollHeight")

            if new_height == last_height:                                                
                break

            last_height = new_height

    def parse(self, driver):
        data = []
        reviewRootElements = driver.find_elements_by_xpath("//div[contains(@jsmodel, 'y8Aajc')]")
        for index, reviewRootElement in enumerate(reviewRootElements):
            if index % 10 == 0:
                print('영차영차 -', index)
            dates = reviewRootElement.find_elements_by_css_selector('.p2TkOb')
            user_names = reviewRootElement.find_elements_by_css_selector('.X43Kjb')
            star_grade = len(reviewRootElement.find_elements_by_css_selector('.vQHuPe.bUWb7c'))
            reviews = reviewRootElement.find_elements_by_css_selector('.UD7Dzf')
            answer = reviewRootElement.find_elements_by_css_selector('.LVQB0b')

            tmp = []
            tmp.append(dates[0].text)
            tmp.append(user_names[0].text)
            tmp.append(star_grade)
            if len(reviews) > 0:
                tmp.append(reviews[0].text)
            else:
                tmp.append('')
            if len(answer) > 0:
                tmp.append(answer[0].text)
            else:
                tmp.append('')
            data.append(tmp)

        return data