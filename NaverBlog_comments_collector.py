# Standard library imports
import os
import subprocess
import re
import time

# Third party imports
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# 사용자 정의
ver = str("2024-03-30 18:00:00")
user = os.getlogin()  # 유저 아이디(현재 자동 입력 중)

# 크롬 드라이버 디버깅 모드 실행
subprocess.Popen(
    r'C:\Program Files\Google\Chrome\Application\chrome.exe --remote-debugging-port=9222 --user-data-dir="C:\\Users\\' + user + r'\\AppData\\Local\\Google\\Chrome\\User Data"')
option = Options()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
option.add_argument(f"user-agent={user_agent}")
option.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
driver = webdriver.Chrome(options=option)
wait_s = WebDriverWait(driver, 10)

# 시작
print("\n")
print("네이버 블로그 댓글수집 프로그램입니다. 네이버 전용 " + ver)
print("https://github.com/movemin03/NaverBlog_Auto")
print("접속할 네이버 블로그 게시글 url 을 입력해주세요")

#"https://blog.naver.com/xsimplex/223368614115"
url = "https://blog.naver.com/knoc3/221609564938"
driver.get(url)

# 저장소 생성
c_list = []

# 게시물 아이디 추출
current_url = driver.current_url
pattern = r'\d+$'
result = re.search(pattern, url)
extracted_number = str(result.group(0))

# iframe 변경
iframe = 'mainFrame'
wait_s.until(ec.presence_of_element_located((By.ID, iframe)))
driver.switch_to.frame(driver.find_element(By.ID, iframe))

a = input("댓글 창을 열고 엔터!!")
pg_parent = driver.find_element(By.XPATH, '//div[contains(@class, "u_cbox_page_wrap")]')
pg_elements = pg_parent.find_elements(By.CLASS_NAME, 'u_cbox_page')
print("탐색할 총 페이지 수는 ", str(len(pg_elements)), " 페이지 입니다")


def sleep_short():
    start_time1 = time.time()
    target_time = start_time1 + 0.2
    while time.time() < target_time:
        pass


for pg_i in range(len(pg_elements)):
    print(str(pg_i + 1), " 페이지를 탐색합니다")
    pg_parent2 = driver.find_element(By.XPATH, '//div[contains(@class, "u_cbox_page_wrap")]')
    pg_elements2 = pg_parent2.find_elements(By.CLASS_NAME, 'u_cbox_page')
    pg_elements2[pg_i].click()
    sleep_short()
    c_list_xpath = '//*[@id="naverComment_201_' + extracted_number + '_wai_u_cbox_content_wrap_tabpanel"]/ul'  # c = comments 약자로 사용
    wait_s.until(ec.presence_of_element_located((By.XPATH, c_list_xpath)))
    c_rows_xpath = c_list_xpath + "//li"

    attempt = 0
    while attempt < 3:
        rows = driver.find_elements(By.XPATH, c_rows_xpath)
        for row in rows:
            # 댓글 단 사람 이름
            c_id_xpath = './div[1]/div/div[1]/span[1]/a/span/span/span'
            try:
                c_id = row.find_element(By.XPATH, c_id_xpath).text
            except NoSuchElementException:
                c_id = "익명"
            # 댓글 단 사람의 블로그 주소
            c_id_url_xpath = './div[1]/div/div[1]/span[1]/a'
            try:
                c_id_url = row.find_element(By.XPATH, c_id_url_xpath).get_attribute('href')
            except NoSuchElementException:
                c_id_url = "익명"
            # 댓글 단 날짜
            c_date_xpath = './div[1]/div/div[3]/span[1]'
            try:
                c_date = row.find_element(By.XPATH, c_date_xpath).text
            except NoSuchElementException:
                c_date = "9999.99.99 00:00"
                # stale element reference

            # 댓글 내용
            c_content_xpath = './div[1]/div/div[2]'
            try:
                if c_date == "9999.99.99 00:00":
                    c_content = "비밀 댓글입니다"
                    c_date = row.find_element(By.XPATH, c_content_xpath).text
                    if c_date.replace(" ", "") == "":
                        c_date = "9999.99.99 00:00"
                        c_content = "댓글이 삭제되었습니다."

                else:
                    c_content = row.find_element(By.XPATH, c_content_xpath).text
            except NoSuchElementException:
                c_content = "내용을 불러올 수 없습니다"
            if "www" or "http" in c_content:
                link_regex = r'(www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})|(https?://\S+)'
                c_links_pre = str(re.findall(link_regex, c_content))
                remove_chars = {"[": None, "]": None, "(": None, ")": None, "'": None, '"': None}
                c_links = c_links_pre.translate(str.maketrans(remove_chars))
                if not c_links:
                    c_links = "X"
            else:
                c_links = "X"
            if "@" in c_content[1:]:
                email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                c_email_pre = str(re.findall(email_regex, c_content))
                remove_chars = {"[": None, "]": None, "(": None, ")": None, "'": None, '"': None}
                c_email = c_email_pre.translate(str.maketrans(remove_chars))
                if not c_email:
                    c_email = "X"
            else:
                c_email = "X"

            # 댓글 좋아요 수
            c_likes_xpath = './div[1]/div/div[4]/div/a/em'
            try:
                c_likes = int(row.find_element(By.XPATH, c_likes_xpath).text)
            except NoSuchElementException:
                c_likes = 0
            c_list.append((c_id, c_id_url, c_date, c_content, c_likes, c_links, c_email))
        if c_list:
            break

# 데이터프레임으로 변환
print("수집이 완료되어 바탕화면에 파일로 저장합니다")
df = pd.DataFrame(c_list, columns=["댓쓴이", "댓쓴이 URL", "날짜", "댓글 내용", "공감 수", "댓글 내 링크", "댓글 내 이메일"])

# Excel 파일로 저장
file_path = "C:\\Users\\" + user + "\\Desktop\\댓글수집.xlsx"

# Excel 파일로 저장 _ 파일명 중복 방지
n = 1
while os.path.exists(file_path):
    n += 1
    file_path = f"C:\\Users\\{user}\\Desktop\\댓글수집({n}).xlsx"

df.to_excel(file_path, index=False)
print(file_path, " 위치에 저장 완료되었습니다")
