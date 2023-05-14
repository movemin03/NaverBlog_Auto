import glob
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
import time
import pyperclip
from webdriver_manager.chrome import ChromeDriverManager
import autoit
import sys
import os.path

if getattr(sys, 'frozen', False):
    chromedriver_path = os.path.join(sys._MEIPASS, "chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome(chromedriver_path, options=options)
else:
    options = webdriver.ChromeOptions()
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    driver = webdriver.Chrome('chromedriver', options=options)
# 안내
print("\n")
print("금천 아발론 자동 업로드 프로그램입니다.")
print("https://github.com/movemin03/BlogPostingAuto")
print("ver.230512.1454")

def addmap():
    driver.find_element(By.XPATH, '//button[contains(@class,"se-map")]').click()
    time.sleep(1)
    place = "아발론 랭콘 잉글리쉬 금천"
    pyperclip.copy(place)
    driver.find_element(By.XPATH, '//input[contains(@placeholder,"장소명을")]').send_keys(Keys.CONTROL + 'v')
    time.sleep(1)
    driver.find_element(By.XPATH, '//button[contains(@class,"se-place-search-button")]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//strong[contains(@class,"se-place-map-search-result-title")]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//span[contains(@class,"se-place-map-search-add-button-text")]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//span[contains(@class,"se-popup-button-text")]').click()
    time.sleep(1)

# 로그인
# uid 와 upw 부분이 아이디 패스워드므로 자신의 것으로 수정해야함. 나머지는 건들지 말기
print("\n")
print("아이디를 입력하세요:")
uid = input()
print("비밀번호를 입력하세요:")
upw = input()
url = ('https://nid.naver.com/nidlogin.login?mode=form&url=https://blog.naver.com/' + str(uid))

driver.get(url)

try:
    tag_id = driver.find_element(By.NAME, 'id')
    tag_pw = driver.find_element(By.NAME, 'pw')
except:
    print("로그인 1/2: 로그인 창 불러오기 실패")
    input()
    exit()

pyperclip.copy(uid)
driver.find_element(By.ID, 'id').send_keys(Keys.CONTROL + 'v')
pyperclip.copy(upw)
driver.find_element(By.ID, 'pw').send_keys(Keys.CONTROL + 'v')
login_btn = driver.find_element(By.ID, 'log.login')
login_btn.click()
print("로그인 2/2: 로그인 완료")

# 반복문구 받기, 반 리스트 받기

post_category = input('포스팅할 카테고리의 숫자를 입력해주세요.\n 1.드림래터 2.각종공지 3.라이팅스타 4.프레젠테이션스타 5.기타\n')
if post_category == ('1'):
    post_category_re = ('//label[contains(@for, "Dream Letter")]')
elif post_category == ('2'):
    post_category_re = ('//label[contains(@for, "각종공지")]')
elif post_category == ('3'):
    post_category_re = ('//label[contains(@for, "Writing Star")]')
elif post_category == ('4'):
    post_category_re = ('//label[contains(@for, "PresentationStar")]')
elif post_category == ('5'):
    post_category_re = ('//label[contains(@for, "기타")]')
else:
    post_category = input

upload_path = input('업로드할 사진이 들어있는 폴더 경로를 붙여넣어주세요')
upload_path_re = upload_path + "\\"

target = (str(upload_path_re) + '*.jpg')
target_2 = (str(upload_path_re) + '*.png')
png_list = glob.glob(target_2)
jpg_list = glob.glob(target)

title_name_re = input('\n제목에서 반복되는 문구가 있다면 써주고 없다면 띄어쓰기 후 엔터. \n 예를 들어 2022 fall 시즌\n')
print(
    '\n사용자의 폴더에는 다음과 같은 png와 jpg 파일이 있습니다. 반명 입력에 참고해주세요. \n 이름이 같고 확장자만 다른 경우 png 파일만 업로드 됩니다. 예를 들어 HA.png 와 HA.jpg  가 있는 경우 png 만 업로드')
print(png_list)
print(jpg_list)

List = [x for x in input('\n반명을 입력해주세요. 업로드할 사진명과 반명이 같아야 합니다. 띄어쓰기로 반을 구분합니다 예를 들어, HA MA 같이. \n').split()]
for i in List:
    class_name = i

    img_path = (str(upload_path_re) + str(class_name) + ".png")
    img_path_2 = (str(upload_path_re) + str(class_name) + ".jpg")

    if img_path in png_list:
        pass
    elif img_path_2 in jpg_list:
        pass
    else:
        print('\n경고: 현재 작업 중인 ' + str(
            class_name) + ' 반에 업로드할 사진 파일이 없습니다. 업로드할 사진명과 반명이 같아야 합니다. 해당 오류는 다음과 같은 원인으로 발생할 수 있습니다.  \n 1.해당 반의 사진 파일이 누락되었습니다. \n 2.반명을 잘못 입력하였습니다 \n 3.대소문자 구분이 잘못되었습니다.')
        b = input('경고를 무시하고 계속하시려면 엔터, 중지하려면 프로그램을 다시 실행해주세요')
    # 페이지 이동

    driver.get("https://blog.naver.com/" + str(uid) + "/postwrite")
    print("글쓰기 1/4: 글쓰기 창 불러오기 완료")
    time.sleep(3)

    # 팝업 창 닫기
    try:
        driver.find_element(By.XPATH, "//span[@class='se-popup-button-text']").click()
    except:
        pass

    try:
        hp_close_btn = driver.find_element(By.CLASS_NAME, 'se-help-panel-close-button')
        hp_close_btn.click()
    except:
        pass

    # 본문 작성
    driver.find_element(By.XPATH, '//span[contains(text(),"제목")]').click()
    action = ActionChains(driver)
    action.send_keys(str(title_name_re) + " " + str(class_name)).perform()
    print("글쓰기 2/4: 제목 입력 완료")

    if img_path in png_list:
        try:
            driver.find_element(By.XPATH, '//button[contains(@class,"se-")]').click()
            time.sleep(2)
            handle = "[CLASS:#32770; TITLE:열기]"
            autoit.control_send(handle, "Edit1", img_path)
            time.sleep(1)
            autoit.control_click(handle, "Button1")
            time.sleep(1)
            print("글쓰기 3/4: png 이미지 불러오기 완료")
        except:
            print("글쓰기 3/4: png 이미지 불러오기 오류")
            input()
            exit()
        try:
            # 지도 넣기
            addmap()
        except:
            print("지도 넣기 실패")
            pass
        try:
            driver.find_elements(By.XPATH, '//p[contains(@class,"se-text-paragraph se-text-paragraph-align-left")]')[1].click()
            action = ActionChains(driver)
            content = ("#금천구어학원 #금천구영어학원 #금천아발론 #아발론 #랭콘 #금천랭콘 #아발론금천 #랭콘금천 #금천초등영어 #금천중등영어 #금천고등영어 #관악어학원 #안양어학원 #광명어학원")
            action.send_keys(content).perform()
            print("글쓰기 4/4: 해시태그 입력 완료")
        except:
            print("글쓰기 4/4: 해시태그 입력 실패:png")
            print("네이버 블로그 업데이트로 내용 입력 칸의 xpath 가 변경되었을 가능성이 있습니다.")
            print("DevTools에서 ctrl+shift+c 로 찾아서 코드를 수정하거나")
            print('내용을 수동으로 입력해주십시오')
            print("추천내용:")
            print("#금천구어학원 #금천구영어학원 #금천아발론 #아발론 #랭콘 #금천랭콘 #아발론금천 #랭콘금천 #금천초등영어 #금천중등영어 #금천고등영어 #관악어학원 #안양어학원 #광명어학원")
            print("계속하시려면 아무 내용 입력 후 enter 키 입력")
            input()

    elif img_path_2 in jpg_list:
        try:
            driver.find_element(By.XPATH, '//button[contains(@class,"se-")]').click()
            time.sleep(2)
            handle = "[CLASS:#32770; TITLE:열기]"
            autoit.control_send(handle, "Edit1", img_path_2)
            time.sleep(1)
            autoit.control_click(handle, "Button1")
            time.sleep(1)
            print("글쓰기 3/4: png 이미지 불러오기 완료")
        except:
            print("글쓰기 3/4: png 이미지 불러오기 오류")
            input()
            exit()
        try:
            # 지도 넣기
            addmap()
        except:
            print("지도 넣기 실패")
            pass
        try:
            driver.find_elements(By.XPATH, '//p[contains(@class,"se-text-paragraph se-text-paragraph-align-left")]')[1].click()
            action = ActionChains(driver)
            content = ("#금천구어학원 #금천구영어학원 #금천아발론 #아발론 #랭콘 #금천랭콘 #아발론금천 #랭콘금천 #금천초등영어 #금천중등영어 #금천고등영어 #관악어학원 #안양어학원 #광명어학원")
            action.send_keys(content).perform()
            print("글쓰기 4/4: 해시태그 입력 완료")

        except:
            print("글쓰기 4/4: 해시태그 입력 실패:jpg")
            print("네이버 블로그 업데이트로 내용 입력 칸의 xpath 가 변경되었을 가능성이 있습니다.")
            print("DevTools에서 ctrl+shift+c 로 찾아서 코드를 수정하거나")
            print('내용을 수동으로 입력해주십시오')
            print("추천내용:")
            print("#금천구어학원 #금천구영어학원 #금천아발론 #아발론 #랭콘 #금천랭콘 #아발론금천 #랭콘금천 #금천초등영어 #금천중등영어 #금천고등영어 #관악어학원 #안양어학원 #광명어학원")
            print("계속하시려면 enter 키 입력")
            input()
    else:
        driver.find_element(By.XPATH, '//span[contains(text(),"본문에")]').click()
        action = ActionChains(driver)
        posting_text = input('포스팅할 내용을 입력해주세요')
        action.send_keys(posting_text).perform()
        time.sleep(1)
        print("글쓰기 3/4: 이미지 입력 pass")
        print("글쓰기 4/4: 내용 입력 완료")
        print("\n")
        # 지도 넣기
        addmap()

    # 발행
    try:
        publish_btn_1 = driver.find_element(By.CLASS_NAME, 'publish_btn__Y5mLP')
        publish_btn_1.click()
        print("발행단계 1/3: 발행 버튼 누르기 완료")
    except:
        print("발행단계 1/3: 발행 버튼 누르기 오류")
        print("도움말 등의 창이 켜져 있을 가능성이 있습니다. 도움말을 닫은 후 브라우저에서 발행버튼을 한번 눌러주십시오")
        print("계속 하려면 아무 내용이나 입력 후 엔터")
        input()

    try:
        category_btn = driver.find_element(By.CLASS_NAME, 'selectbox_button__y_UvS')
        category_btn.click()
        print("발행단계 2/3: 카테고리 버튼 누르기 완료")
        time.sleep(1)
        driver.find_element(By.XPATH, post_category_re).click()
        print("발행단계 2/3: 게시판 변경 완료")
    except:
        print("발행단계 2/3: 카테고리 설정 오류")
        print("카테고리 수동 설정한 후, 계속 하려면 아무 내용이나 입력 후 엔터")
        input()

    try:
        time.sleep(1)
        publish_btn_2 = driver.find_element(By.CLASS_NAME, 'confirm_btn__Dv9du')
        publish_btn_2.click()
        time.sleep(1)
        print("발행단계 3/3: 발행 완료")
    except:
        print("발행단계 3/3: 발행 버튼 누르기 실패")
        print("수동 설정하고 계속 하려면 아무 내용이나 입력 후 엔터")
        input()

print("\n")
print('모든 작업이 완료되었습니다')
a = input()
