from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
from selenium.webdriver.chrome.options import Options


class LostItemFinder:
    def __init__(self, item, distinct, startDate, endDate):
        self.find_item = item
        self.distinct = distinct
        self.year1, self.year2  = int(startDate[:4]) , int(endDate[:4])
        self.month1, self.month2 = int(startDate[4:6]), int(endDate[4:6])
        self.day1, self.day2 = int(startDate[6:]) , int(endDate[6:])
        # Chrome 옵션 설정
        chrome_options = Options()
        chrome_options.add_argument("--start-maximized")  # 전체 화면으로 시작
        
        self.driver = webdriver.Chrome(chrome_options)
        
    def open_website(self, url):
        self.driver.get(url)
        self.driver.implicitly_wait(1)  # 페이지 로딩 대기

    def input_item(self):
        input_element = self.driver.find_element(By.XPATH, '//*[@id="prdtNm"]')
        input_element.send_keys(self.find_item)

    def select_date(self):
        date_button1 = self.driver.find_element(By.XPATH, '//*[@id="commandMap"]/div[1]/fieldset[2]/button[1]')
        date_button1.click()
        self.driver.implicitly_wait(2) 
        
        #계산을 위해 현재 날짜 추출
        nowdate_ = self.driver.find_element(By.XPATH, '//*[@id="CalendarControl"]/div/div[1]/div[2]')
        nowdate = nowdate_.text.replace('\xa0', '').replace(' ', '') 
        nowdate_year1, nowdate_month1 = int(nowdate[:4]), int(nowdate[4:])
        
        #start 시점
        self.button_of_year_change_xpath = '//*[@id="CalendarControl"]/div/div[1]/div[1]/button[1]'
        self.left_button_of_month_change_xpath = '//*[@id="CalendarControl"]/div/div[1]/div[1]/button[2]'
        self.right_button_of_month_change_xpath = '//*[@id="CalendarControl"]/div/div[1]/div[3]/button[1]'
        
        self.adjust_date(nowdate_year1, nowdate_month1, self.year1, self.month1, self.day1)
        
        #end시점
        date_button2 = self.driver.find_element(By.XPATH, '//*[@id="commandMap"]/div[1]/fieldset[2]/button[2]') 
        date_button2.click()
        #현재 날짜 추출
        nowdate_ = self.driver.find_element(By.XPATH, '//*[@id="CalendarControl"]/div/div[1]/div[2]')
        nowdate = nowdate_.text.replace('\xa0', '').replace(' ', '') 
        nowdate_year2, nowdate_month2 = int(nowdate[:4]), int(nowdate[4:])
        self.driver.implicitly_wait(2)
        
        self.adjust_date(nowdate_year2, nowdate_month2, self.year2, self.month2, self.day2) 
          
        # button_of_year_change_xpath1 = '//*[@id="CalendarControl"]/div/div[1]/div[1]/button[1]'
        # left_button_of_month_change_xpath1 = '//*[@id="CalendarControl"]/div/div[1]/div[1]/button[2]'
        # right_button_of_month_change_xpath1 = '//*[@id="CalendarControl"]/div/div[1]/div[3]/button[1]'
        
        
    def click_button(self,button_xpath):
        try:
            button = self.driver.find_element(By.XPATH, button_xpath)
            self.driver.execute_script("arguments[0].click();", button)
            #상태가 변경되면 다시 파싱
        except StaleElementReferenceException:
            button = self.driver.find_element(By.XPATH, button_xpath)
            self.driver.execute_script("arguments[0].click();", button)

    def adjust_date(self, nowYear, nowMonth, year, month, day):
        year_diff = nowYear - year
        month_diff = nowMonth -  month
        ###현재 문제: 달력의 달 버튼을 누르면 달력이 초기화? 되는거 같음 그래서 ㅅㅂ 무슨 요소가 없대
        # button_of_year_change = self.driver.find_element(By.XPATH, '//*[@id="CalendarControl"]/div/div[1]/div[1]/button[1]') #//button[@class='m_prev' and @title='Previous Month']
        # left_button_of_month_change = self.driver.find_element(By.XPATH, '//*[@id="CalendarControl"]/div/div[1]/div[1]/button[2]')
        # right_button_of_month_change = self.driver.find_element(By.XPATH,'//*[@id="CalendarControl"]/div/div[1]/div[3]/button[1]')
        
        
        if year_diff != 0: 
            for _ in range(year_diff): # year difference 만큼 반복
                self.click_button(self.button_of_year_change_xpath)
                self.driver.implicitly_wait(1)

        if month_diff > 0:       
            for _ in range(month_diff):
                self.click_button(self.left_button_of_month_change_xpath)
                self.driver.implicitly_wait(1)
                
        elif month_diff < 0:
            for _ in range(-month_diff):
                self.click_button(self.right_button_of_month_change_xpath)
                self.driver.implicitly_wait(1)

        day_element = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//a[text()='{day}']"))
        )
        day_element.click()
        self.driver.implicitly_wait(1)       

    def search_items(self): 
        results = []
        button_element = self.driver.find_element(By.XPATH, '//*[@id="searchMain"]')
        button_element.click()
        self.driver.implicitly_wait(1)
        

        indeX = 2
        End = False
        
        while not End:
            try:
                for index in range(1, 11):
                    sub_find_link = self.driver.find_element(By.XPATH, f'//*[@id="contents"]/div[3]/table/tbody/tr[{index}]/td[2]/div/a')
                    sub_find_link.click()
                    self.driver.implicitly_wait(1)
                    soup2 = BeautifulSoup(self.driver.page_source, 'html.parser')
                    
                    if self.distinct in soup2.get_text():
                        element = self.driver.find_element(By.XPATH, '//*[@id="contents"]/div[2]/div[1]/div[3]/ul/li[1]/p[2]')
                        text = element.text 
                        results.append(f"관리번호: {text[:17]}")
                    
                    
                    
                    self.driver.back()
                    self.driver.implicitly_wait(1)
                    
                if indeX == 11:
                    next_button = self.driver.find_element(By.XPATH, '//*[@id="paging"]/span[2]/a[1]')
                    next_button.click()
                    indeX = 1
                
                index_button = self.driver.find_element(By.XPATH, f'//*[@id="paging"]/a[{indeX}]')
                index_button.click()
                indeX += 1

            except NoSuchElementException: 
                # print("요소를 찾을 수 없습니다. 브라우저를 종료합니다.")
                End = True
                break
            
        return results
    
    def close_browser(self):
        self.driver.quit()
#

if __name__ == "__main__":
    find_item = input("찾을 물건을 입력하세요: ")
    distinct = input("찾을 물건의 특징을 입력하세요: ")
    year_month_day = input("일,년,월,일을 입력하세요(입력 예시: 20240427): ")

    finder = LostItemFinder(find_item, distinct, year_month_day)
    finder.open_website("https://www.lost112.go.kr/find/findList.do")
    finder.input_item()
    finder.select_date()
    finder.search_items()
    finder.close_browser()
