# BlogPostingAuto

 네이버 블로그에 대량으로 글 포스팅을 하는 프로그램입니다. 
 본 프로그램은 특정 블로그에 반별 시간표나 공지사항을 업로드하는 것에 본래 목적을 두고 있습니다. 다른 목적으로 이용하기 위해선 코드를 일부 수정해야 합니다. 
 exe 는 크롬 드라이버 113을 기반으로 하고 있으며 크롬 버전이 다른 경우 작동되지 않을 수 있습니다. 이 경우, 본인의 컴퓨터에 맞는 크롬 드라이버를 다운로드한 후 pyinstaller를 통해 py 파일을 exe 파일로 다시 내보내기 하십시오.

-------------------------------
주의사항
-------------------------------
불법적인 목적으로 남용될 경우, 네이버 봇에 의해 계정이 될 가능성이 있으니 조심하시길 바랍니다.

-------------------------------
Pyinstaller 관련
-------------------------------
본 프로그램에는
selenium, pyperclip, certifi, urllib3, pyautoit, autoit, webdriver_manager 라이브러리가 사용되었습니다.

본인의 경우 pyinstaller 사용 시 다음 명령을 사용하였습니다:

pyinstaller BlogPostingAuto113.py --onefile --add-binary "chromedriver.exe;." --add-data="AutoItX3_x64.dll;autoit\lib" --hidden-import certifi --hidden-import urllib3 --hidden-import pyperclip --hidden-import webdriver-manager --hidden-import pyautoit --hidden-import autoit
