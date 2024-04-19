# Standard library imports
import os
import re
import time
from datetime import datetime

# Third party imports
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
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
    driver = webdriver.Chrome(options=option)

wait_s = WebDriverWait(driver, 10)
print("\n접속할 네이버 블로그 게시글 url 을 입력해주세요")
url = input()

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
        split_url = url.split("com/")[1]
        blog_id, extracted_number = split_url.split("/")
    except:
        print("url 패턴을 인식할 수 없습니다")
        print("엔터 입력 시 프로그램이 종료됩니다")
        a = input()
        exit()
url = "https://m.blog.naver.com/CommentList.naver?blogId=" + blog_id + "&logNo=" + extracted_number

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

time.sleep(2)
driver.execute_script("window.scrollTo(0, 0);")
while True:
    last_height = driver.execute_script("return document.body.scrollHeight")
    driver.execute_script("window.scrollTo(0, 0);")
    time.sleep(1)
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break

time.sleep(2)

html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
driver.quit()

# 저장소 생성
c_save = []


def find_data():
    c_list_css_selector = '#naverComment_wai_u_cbox_content_wrap_tabpanel > ul'
    c_list = soup.select(c_list_css_selector)

    # c_list 내의 각 li 요소 선택
    rows = c_list[0].find_all('li')

    for row in rows:
        # 대댓글 여부 확인 egarggg
        if row.find('div').find(class_="u_cbox_ico_reply"):
            nested_comment = 'O'
        else:
            nested_comment = 'X'
        print("대댓글 여부:", nested_comment)

        # 댓글 단 사람 이름
        c_id_css_selector = "div:nth-child(1) div div:nth-child(2) span:nth-child(1)"
        c_id_element = row.select_one(c_id_css_selector)
        c_id = c_id_element.text
        if c_id is None or c_id == "":
            c_id_css_selector = ".u_cbox_reply_area > ul > li > div > div > div.u_cbox_info > span.u_cbox_info_main > a > span > span > span"
            c_id_element = row.select_one(c_id_css_selector)
            c_id = c_id_element.text
            if c_id is None or c_id == "":
                c_id = "익명"

        # 댓글 단 사람의 블로그 주소
        c_id_url_css_selector = '.u_cbox_comment_box.u_cbox_type_profile > div > div.u_cbox_info > span.u_cbox_info_main > a'
        c_id_url_element = row.select_one(c_id_url_css_selector)
        c_id_url = str(c_id_url_element['href']) if c_id_url_element else "익명"

        # 댓글 단 날짜
        try:
            c_date_css_selector = "div:nth-child(1) div div:nth-child(3) span"
            c_date_pre1 = row.select_one(c_date_css_selector).text
            c_date_pre2 = datetime.strptime(c_date_pre1, '%Y.%m.%d. %H:%M')
            c_date = str(c_date_pre2.strftime('%Y-%m-%d %H:%M'))
        except:
            try:
                c_date_css_selector = "div:nth-child(1) > div > div:nth-child(4) > span"
                c_date_pre1 = row.select_one(c_date_css_selector).text
                c_date_pre2 = datetime.strptime(c_date_pre1, '%Y.%m.%d. %H:%M')
                c_date = str(c_date_pre2.strftime('%Y-%m-%d %H:%M'))
            except:
                c_date = "9999-01-01 00:00"

        # 댓글 내용
        c_content_css_selector = "div:nth-child(1) > div > div:nth-child(2) > span:nth-child(1)"
        c_content_element = row.select_one(c_content_css_selector)
        if c_content_element:
            c_content = c_content_element.text
        else:
            c_content = "내용을 불러올 수 없습니다"

        # 댓글 좋아요 수
        c_likes_css_selector = "div:nth-child(1) div div:nth-child(4) div a em"
        c_likes_element = row.select_one(c_likes_css_selector)
        c_likes = int(c_likes_element.text) if c_likes_element else 0

        # 댓글 내 이미지 링크
        comment_img_css_selector = 'div > div > div:nth-child(3) > div > a > img'
        comment_img_element = row.select_one(comment_img_css_selector)
        comment_img = str(comment_img_element['src']) if comment_img_element else "X"
        if "?type=" in comment_img:
            comment_img = comment_img.split('?type=')[0]

        # 댓글 내 링크 및 이메일 체크
        if "www" in c_content or "http" in c_content:
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
        #
        c_save.append((nested_comment, c_id, c_id_url, c_date, c_content, c_likes, c_links, c_email, comment_img))


find_data()

# 데이터프레임으로 변환
print("수집이 완료되어 바탕화면에 파일로 저장합니다")
df = pd.DataFrame(c_save, columns=["대댓글 여부", "댓쓴이", "댓쓴이 URL", "날짜", "댓글 내용", "공감 수", "댓글 내 링크", "댓글 내 이메일", "댓글 내 이미지"])

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
