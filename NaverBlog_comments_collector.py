# Standard library imports
import os
import re
import time
from datetime import datetime
import math

# Third party imports
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
import openpyxl

def sleep_short():
    start_time1 = time.time()
    target_time = start_time1 + 0.2
    while time.time() < target_time:
        pass


# 사용자 정의
ver = str("2024-04-19 01:00:00")
user = os.getlogin()  # 유저 아이디(현재 자동 입력 중)

# 크롬 드라이버 디버깅 모드 실행
option = webdriver.ChromeOptions()
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36"
option.add_argument(f"user-agent={user_agent}")

# 시작
print("\n")
print("네이버 블로그 댓글수집 프로그램입니다. 네이버 전용 " + ver)
print("https://github.com/movemin03/NaverBlog_Auto\n")
print("접속할 블로그에 로그인이 필요합니까? y / n")
print("해당 블로그의 소유주일 경우에는 y 를 권장합니다 (비밀 댓글도 수집할 수 있습니다)")
a = input()
if a == "y":
    print("로그인이 필요한 것으로 확인되었습니다")
    driver = webdriver.Chrome(options=option)
    driver.get("https://nid.naver.com/nidlogin.login?url=https%3A%2F%2Fsection.blog.naver.com%2FBlogHome.naver")
    print("로그인 진행 완료 후 아무값이나 입력해주세요")
    a = input()
else:
    print("로그인이 필요 없는 것으로 확인되었습니다")
    option.add_argument('headless')
    driver = webdriver.Chrome(options=option)

wait_s = WebDriverWait(driver, 10)
print("\n접속할 네이버 블로그 게시글 url 을 입력해주세요")
url = input()
if "m.blog" in url:
    url = url.replace("m.blog", "blog")

# 저장소 생성
c_list = []

# 게시물 아이디 추출
current_url = driver.current_url

try:
    print("method1")
    blog_id = re.search(r'blogId=([^&]+)', url).group(1)
    extracted_number = re.search(r'logNo=([^&]+)', url).group(1)
    url = "https://blog.naver.com/" + blog_id + "/" + extracted_number
    print(extracted_number)
except:
    print("method2")
    try:
        pattern1 = r'\d+$'
        result = re.search(pattern1, url)
        extracted_number = str(result.group(0))
        print(extracted_number)
    except:
        print("url 패턴을 인식할 수 없습니다")
        print("엔터 입력 시 프로그램이 종료됩니다")
        a = input()
        exit()
print(url)
# 프로그램이 완전히 켜질 때까지 대기
while True:
    try:
        driver.get(url)
        driver.execute_script("var script = document.createElement('script');\
                              script.src = 'https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY&callback=initMap';\
                              script.defer = true;\
                              document.head.appendChild(script);")
        break
    except:
        sleep_short()

# iframe 변경
iframe = 'mainFrame'
wait_s.until(ec.presence_of_element_located((By.ID, iframe)))
driver.switch_to.frame(driver.find_element(By.ID, iframe))

c_btn_xpath = '//*[@id="Comi' + extracted_number + '"]'
wait_s.until(ec.presence_of_element_located((By.XPATH, c_btn_xpath)))
driver.find_element(By.XPATH, c_btn_xpath).click()

def find_data():
    pg_parent_xpath = '//div[contains(@class, "u_cbox_page_wrap")]'
    wait_s.until(ec.presence_of_element_located((By.XPATH, pg_parent_xpath)))
    pg_parent = driver.find_element(By.XPATH, pg_parent_xpath)
    pg_elements = pg_parent.find_elements(By.CLASS_NAME, 'u_cbox_page')
    global sub_page
    print("현재화면에서 ", str(len(pg_elements)), " 페이지를 탐색합니다")

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
                #대댓글 여부
                nested_comments_xpath = "./div[1]/span[@class='u_cbox_ico_reply']"
                try:
                    c_id = row.find_element(By.XPATH, nested_comments_xpath)
                    nested_comment = "O"
                except:
                    nested_comment = "X"
                # 댓글 단 사람 이름
                c_id_xpath = './div[1]/div/div[1]/span[1]/a/span/span/span'
                try:
                    c_id = row.find_element(By.XPATH, c_id_xpath).text
                except:
                    c_id = "익명"
                # 댓글 단 사람의 블로그 주소
                c_id_url_xpath = './div[1]/div/div[1]/span[1]/a'
                try:
                    c_id_url = row.find_element(By.XPATH, c_id_url_xpath).get_attribute('href')
                except:
                    c_id_url = "익명"
                # 댓글 단 날짜
                c_date_xpath = ".//span[@class='u_cbox_date']"
                try:
                    c_date_pre1 = row.find_element(By.XPATH, c_date_xpath).text
                    c_date_pre2 = datetime.strptime(c_date_pre1, '%Y.%m.%d. %H:%M')
                    c_date = c_date_pre2.strftime('%Y-%m-%d %H:%M')
                except:
                    c_date = "9999-01-01 00:00"
                    # stale element reference

                # 댓글 내용
                c_content_xpath = './div[1]/div/div[2]'
                try:
                    if str(c_date) == "9999-01-01 00:00":
                        c_content = "비밀 댓글입니다"
                        c_date_pre1 = row.find_element(By.XPATH, c_content_xpath).text
                        c_date_pre2 = datetime.strptime(c_date_pre1, '%Y.%m.%d. %H:%M')
                        c_date = c_date_pre2.strftime('%Y-%m-%d %H:%M')

                        if c_date.replace(" ", "") == "":
                            c_date = "9999-01-01 00:00"
                            c_content = "댓글이 삭제되었습니다."
                    else:
                        c_content = row.find_element(By.XPATH, c_content_xpath).text
                    if c_content is None or c_content == "":
                        c_content = "표시할 텍스트가 없습니다(이모티콘만 있는 경우)"
                except Exception as e:
                    print(e)
                    c_content = "내용을 불러올 수 없습니다"

                if "www" or "http" in c_content:
                    link_regex = r'(www\.[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})|(https?://\S+)'
                    c_links_pre = str(re.findall(link_regex, c_content))
                    remove_chars = {"[": None, "]": None, "(": None, ")": None, "'": None, '"': None}
                    c_links = c_links_pre.translate(str.maketrans(remove_chars))[2:].replace(", ,", ",")
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
                except:
                    c_likes = 0

                # 댓글 내 이미지 링크
                comment_img_xpath = './div[1]/div/div[3]/div/a/img'
                try:
                    comment_img = row.find_element(By.XPATH, comment_img_xpath).get_attribute('src')
                    if "?type=" in comment_img:
                        comment_img = comment_img.split('?type=')[0]
                except:
                    try:
                        comment_img_xpath = './div[1]/div/span/a/img'
                        comment_img = row.find_element(By.XPATH, comment_img_xpath).get_attribute('src')
                    except:
                        comment_img = "X"

                c_list.append((nested_comment, c_id, c_id_url, c_date, c_content, c_likes, c_links, c_email, comment_img))
            if c_list:
                break


total_page_xpath = '//*[@id="commentCount"]'

try:
    wait_s.until(ec.presence_of_element_located((By.XPATH, total_page_xpath)))
    total_page = driver.find_element(By.XPATH, total_page_xpath).get_attribute("textContent").replace(" ", "").replace(",", "")
    print("총 댓글 수는  ", total_page, "입니다")
    total_page = math.ceil(int(total_page) / 50)
    print("총 페이지 수는  ", total_page, "입니다")
except Exception as e:
    print("총 댓글 수 탐색 실패:", e)
    total_page = 0


for next_page in range(math.ceil(total_page/10)):
    find_data()
    previous_btn_xpath = '//*[@id="naverComment_201_' + extracted_number + '"]/div/div[4]/div/a[2]'
    attempt = 0
    while attempt < 3:
        try:
            driver.find_element(By.XPATH, previous_btn_xpath).click()
            time.sleep(1)
            break
        except Exception as e:
            print(e)
            attempt += 1
            time.sleep(1)

# 데이터프레임으로 변환
print("수집이 완료되어 바탕화면에 파일로 저장합니다")
df = pd.DataFrame(c_list, columns=["대댓글 여부", "댓쓴이", "댓쓴이 URL", "날짜", "댓글 내용", "공감 수", "댓글 내 링크", "댓글 내 이메일", "댓글 내 이미지"])

# Excel 파일로 저장
file_path = "C:\\Users\\" + user + "\\Desktop\\댓글수집.xlsx"

# Excel 파일로 저장 _ 파일명 중복 방지
n = 1
while os.path.exists(file_path):
    n += 1
    file_path = f"C:\\Users\\{user}\\Desktop\\댓글수집({n}).xlsx"

df.to_excel(file_path, index=False)
print(file_path, " 위치에 저장 완료되었습니다")

driver.quit()
a = input("아무키나 입력하면 종료됩니다")
exit()
