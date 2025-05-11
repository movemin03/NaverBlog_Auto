# Standard library imports
import os
import re
import time
import threading
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from datetime import datetime
import queue

# Third party imports
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import subprocess


class NaverBlogCommentCollector:
    def __init__(self, root):
        self.root = root
        self.root.title("네이버 블로그 댓글 수집기 v2025.05.12")
        self.root.geometry("700x550")
        self.root.resizable(True, True)

        # 변수 설정
        self.version = "2025-05-12 00:00:00"
        self.user = os.getlogin()
        self.is_running = False
        self.driver = None
        self.log_queue = queue.Queue()
        self.default_save_path = os.path.join(os.path.expanduser("~"), "Desktop", "naver_blog_댓글수집.xlsx")

        # 스타일 설정
        style = ttk.Style()
        style.configure("TButton", padding=6, relief="flat", background="#ccc")
        style.configure("TLabel", padding=6)
        style.configure("TFrame", padding=10)

        self.create_widgets()
        self.setup_logging()

    def create_widgets(self):
        # 메인 프레임
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # URL 입력 섹션
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=5)

        ttk.Label(url_frame, text="블로그 게시글 URL:").pack(side=tk.LEFT)
        self.url_entry = ttk.Entry(url_frame, width=50)
        self.url_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        # 옵션 섹션
        option_frame = ttk.Frame(main_frame)
        option_frame.pack(fill=tk.X, pady=5)

        ttk.Label(option_frame, text="블로그 소유주 여부:").pack(side=tk.LEFT)
        self.owner_var = tk.StringVar(value="n")
        ttk.Radiobutton(option_frame, text="예", variable=self.owner_var, value="y").pack(side=tk.LEFT, padx=5)
        ttk.Radiobutton(option_frame, text="아니오", variable=self.owner_var, value="n").pack(side=tk.LEFT, padx=5)

        # 파일 저장 위치 섹션
        save_frame = ttk.Frame(main_frame)
        save_frame.pack(fill=tk.X, pady=5)

        ttk.Label(save_frame, text="저장 위치:").pack(side=tk.LEFT)
        self.save_path_var = tk.StringVar(value=self.default_save_path)
        self.save_path_entry = ttk.Entry(save_frame, textvariable=self.save_path_var, width=50)
        self.save_path_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)

        browse_btn = ttk.Button(save_frame, text="찾아보기", command=self.browse_save_location)
        browse_btn.pack(side=tk.LEFT, padx=5)

        # 로그 창
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        ttk.Label(log_frame, text="로그:").pack(anchor=tk.W)
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True)
        self.log_text.config(state=tk.DISABLED)

        # 버튼 섹션
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        self.start_btn = ttk.Button(button_frame, text="실행", command=self.start_collection)
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = ttk.Button(button_frame, text="중지", command=self.stop_collection, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        self.open_file_btn = ttk.Button(button_frame, text="파일 위치 열기", command=self.open_file_location,
                                        state=tk.DISABLED)
        self.open_file_btn.pack(side=tk.LEFT, padx=5)

        # 상태 표시줄
        self.status_var = tk.StringVar(value="준비됨")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def setup_logging(self):
        # 로그 업데이트 함수
        def update_log():
            while True:
                try:
                    record = self.log_queue.get(block=False)
                    self.log_text.config(state=tk.NORMAL)
                    self.log_text.insert(tk.END, record + "\n")
                    self.log_text.see(tk.END)
                    self.log_text.config(state=tk.DISABLED)
                    self.log_queue.task_done()
                except queue.Empty:
                    break
            self.root.after(100, update_log)

        # 로그 업데이트 시작
        self.root.after(100, update_log)

    def log(self, message):
        self.log_queue.put(f"[{datetime.now().strftime('%H:%M:%S')}] {message}")

    def browse_save_location(self):
        filename = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(self.save_path_var.get()),
            initialfile=os.path.basename(self.save_path_var.get()),
            defaultextension=".xlsx",
            filetypes=[("Excel 파일", "*.xlsx"), ("모든 파일", "*.*")]
        )
        if filename:
            self.save_path_var.set(filename)

    def start_collection(self):
        if not self.url_entry.get().strip():
            self.log("오류: URL을 입력해주세요.")
            return

        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.open_file_btn.config(state=tk.DISABLED)
        self.status_var.set("실행 중...")

        # 별도 스레드에서 실행
        threading.Thread(target=self.collect_comments, daemon=True).start()

    def stop_collection(self):
        self.is_running = False
        self.log("사용자에 의해 작업이 중지되었습니다.")
        self.status_var.set("중지됨")

        if self.driver:
            try:
                self.driver.quit()
            except:
                pass
            self.driver = None

        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)

    def open_file_location(self):
        save_path = self.save_path_var.get()
        if os.path.exists(save_path):
            try:
                # 파일 탐색기에서 파일 선택하여 열기
                if os.name == 'nt':  # Windows
                    subprocess.Popen(f'explorer /select,"{save_path}"')
                elif os.name == 'posix':  # macOS, Linux
                    if 'darwin' in os.sys.platform:  # macOS
                        subprocess.Popen(['open', '-R', save_path])
                    else:  # Linux
                        subprocess.Popen(['xdg-open', os.path.dirname(save_path)])
            except Exception as e:
                self.log(f"파일 위치를 열 수 없습니다: {str(e)}")
        else:
            self.log("파일이 존재하지 않습니다.")

    def collect_comments(self):
        try:
            self.log(f"네이버 블로그 댓글수집 프로그램 v{self.version} 시작")

            # 크롬 드라이버 설정
            options = Options()
            user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
            options.add_argument(f"user-agent={user_agent}")

            # 로그인 필요 여부 확인
            is_owner = self.owner_var.get() == "y"

            if is_owner:
                self.log("블로그 소유주 모드로 실행합니다 (로그인 필요)")
                # 로그인을 위해 헤드리스 모드 비활성화
                self.driver = webdriver.Chrome(options=options)
                self.driver.get("https://nid.naver.com/nidlogin.login?mode=form&url=https://www.naver.com/")

                # 로그인 대기
                self.log("네이버 로그인 페이지가 열렸습니다. 로그인을 완료해주세요.")
                self.root.after(0, lambda: self.show_login_dialog())
                return
            else:
                self.log("비소유주 모드로 실행합니다 (로그인 불필요)")
                options.add_argument("--headless")  # 헤드리스 모드
                self.driver = webdriver.Chrome(options=options)
                self.process_url()

        except Exception as e:
            self.log(f"오류 발생: {str(e)}")
            self.stop_collection()

    def show_login_dialog(self):
        login_dialog = tk.Toplevel(self.root)
        login_dialog.title("로그인 확인")
        login_dialog.geometry("300x150")
        login_dialog.transient(self.root)
        login_dialog.grab_set()

        ttk.Label(login_dialog, text="네이버 로그인을 완료하셨나요?").pack(pady=20)

        btn_frame = ttk.Frame(login_dialog)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="완료", command=lambda: self.login_completed(login_dialog)).pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="취소", command=lambda: self.login_cancelled(login_dialog)).pack(side=tk.LEFT, padx=10)

    def login_completed(self, dialog):
        dialog.destroy()

        # 로그인 완료 후 쿠키 수집
        self.log("로그인 정보 저장 중...")
        cookies = self.driver.get_cookies()

        # 기존 브라우저 종료
        self.driver.quit()
        self.driver = None

        # 새로운 headless 브라우저 생성
        options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        options.add_argument(f"user-agent={user_agent}")
        options.add_argument("--headless=new")  # 최신 headless 모드 사용

        self.log("백그라운드 모드로 전환 중...")
        self.driver = webdriver.Chrome(options=options)

        # 네이버 도메인 방문 (쿠키 설정을 위해)
        self.driver.get("https://www.naver.com")

        # 저장된 쿠키 적용
        for cookie in cookies:
            # 일부 쿠키 속성은 추가할 때 문제를 일으킬 수 있어 제거
            if 'expiry' in cookie:
                del cookie['expiry']
            try:
                self.driver.add_cookie(cookie)
            except Exception as e:
                self.log(f"쿠키 설정 중 오류 발생: {str(e)}")

        self.log("로그인 정보 적용 완료")
        self.process_url()

    def login_cancelled(self, dialog):
        dialog.destroy()
        self.stop_collection()

    def process_url(self):
        if not self.is_running:
            return

        url = self.url_entry.get().strip()
        self.log(f"입력된 URL: {url}")

        try:
            # 게시물 아이디 추출
            try:
                self.log("URL 형식 분석 중 (method1)")
                blog_id = re.search(r'blogId=([^&]+)', url).group(1)
                extracted_number = re.search(r'logNo=([^&]+)', url).group(1)
                url = f"https://blog.naver.com/{blog_id}/{extracted_number}"
                self.log("URL 변환 완료")
            except:
                self.log("method1 실패, method2 시도 중")
                try:
                    split_url = url.split("com/")[1]
                    blog_id, extracted_number = split_url.split("/")
                    self.log("URL 변환 완료")
                except:
                    self.log("URL 패턴을 인식할 수 없습니다.")
                    self.stop_collection()
                    return

            # 모바일 댓글 페이지로 변환
            mobile_url = f"https://m.blog.naver.com/CommentList.naver?blogId={blog_id}&logNo={extracted_number}"
            self.log(f"모바일 댓글 페이지 URL: {mobile_url}")

            # 페이지 로드
            self.log("댓글 페이지 로딩 중...")
            self.driver.get(mobile_url)

            # 스크롤하여 모든 댓글 로드
            self.log("모든 댓글을 로드하기 위해 스크롤 중...")
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, 0);")

            last_height = 0
            for _ in range(10):  # 최대 10번 스크롤 시도
                if not self.is_running:
                    return

                current_height = self.driver.execute_script("return document.body.scrollHeight")
                if current_height == last_height:
                    break

                # 페이지 끝까지 스크롤
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)
                last_height = current_height

            # 댓글 데이터 수집
            self.log("댓글 데이터 수집 중...")
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 드라이버 종료
            self.driver.quit()
            self.driver = None

            # 댓글 파싱
            c_save = self.parse_comments(soup)

            if not c_save:
                self.log("수집된 댓글이 없습니다.")
                self.stop_collection()
                return

            # 데이터프레임으로 변환
            self.log(f"총 {len(c_save)}개의 댓글을 수집했습니다.")
            df = pd.DataFrame(c_save, columns=["대댓글 여부", "댓쓴이", "댓쓴이 URL", "날짜", "댓글 내용", "공감 수", "댓글 내 링크", "댓글 내 이메일",
                                               "댓글 내 이미지"])

            # 파일 저장
            save_path = self.save_path_var.get()
            save_path = self.ensure_unique_filename(save_path)

            df.to_excel(save_path, index=False)
            self.log(f"파일 저장 완료: {save_path}")

            # 작업 완료 후 UI 업데이트
            self.root.after(0, self.collection_completed, save_path)

        except Exception as e:
            self.log(f"오류 발생: {str(e)}")
            if self.driver:
                self.driver.quit()
                self.driver = None
            self.root.after(0, self.stop_collection)

    def parse_comments(self, soup):
        c_save = []

        try:
            c_list_css_selector = '#naverComment_wai_u_cbox_content_wrap_tabpanel > ul'
            c_list = soup.select(c_list_css_selector)

            if not c_list:
                self.log("댓글 목록을 찾을 수 없습니다.")
                return c_save

            # c_list 내의 각 li 요소 선택
            rows = c_list[0].find_all('li')
            self.log(f"댓글 {len(rows)}개 발견")

            for idx, row in enumerate(rows):
                if not self.is_running:
                    return c_save

                self.log(f"댓글 {idx + 1}/{len(rows)} 처리 중")

                # 대댓글 여부 확인
                if row.find('div').find(class_="u_cbox_ico_reply"):
                    nested_comment = 'O'
                else:
                    nested_comment = 'X'

                # 댓글 단 사람 이름
                c_id_css_selector = "div:nth-child(1) div div:nth-child(2) span:nth-child(1)"
                c_id_element = row.select_one(c_id_css_selector)

                if c_id_element is None or c_id_element.text == "":
                    c_id_css_selector = ".u_cbox_reply_area > ul > li > div > div > div.u_cbox_info > span.u_cbox_info_main > a > span > span > span"
                    c_id_element = row.select_one(c_id_css_selector)
                    if c_id_element is None or c_id_element.text == "":
                        c_id = "익명"
                    else:
                        c_id = c_id_element.text
                else:
                    c_id = c_id_element.text

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
                    try:
                        date_format = "%Y.%m.%d. %H:%M"
                        c_date = datetime.strptime(c_content, date_format)
                        c_content = "비밀 댓글입니다."
                    except ValueError:
                        pass
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

                c_save.append(
                    (nested_comment, c_id, c_id_url, c_date, c_content, c_likes, c_links, c_email, comment_img))

        except Exception as e:
            self.log(f"댓글 파싱 중 오류 발생: {str(e)}")

        return c_save

    def ensure_unique_filename(self, filepath):
        """파일명이 중복되지 않도록 처리"""
        directory = os.path.dirname(filepath)
        filename = os.path.basename(filepath)
        name, ext = os.path.splitext(filename)

        counter = 1
        while os.path.exists(filepath):
            filepath = os.path.join(directory, f"{name}({counter}){ext}")
            counter += 1

        return filepath

    def collection_completed(self, save_path):
        self.is_running = False
        self.status_var.set("완료됨")
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.open_file_btn.config(state=tk.NORMAL)
        self.log("작업이 완료되었습니다.")


def main():
    root = tk.Tk()
    app = NaverBlogCommentCollector(root)
    root.mainloop()


if __name__ == "__main__":
    main()
