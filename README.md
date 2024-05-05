# NaverBlog_Auto (English Description) ❤️👍

NaverBlog_Auto is an all-in-one program designed for bulk posting and comment collection on Naver blogs.

## 1. NaverBlog_comments_collector.py

**Description:**
A program designed to collect comments from Naver blogs. Simply input the blog link, and it will be automatically recognized. Developed in the Chrome 123 environment.

**Usage:**
After running the program, simply input the URL you wish to track!

**Requirements:**
```python
pip install pandas, bs4, selenium, openpyxl, lxml
```

**Exporting as Executable:**
For PyInstaller, use the following command:
```cmd
pyinstaller NaverBlog_comments_collector.py --onefile --hidden-import os --hidden-import re --hidden-import time --hidden-import datetime --hidden-import pandas --hidden-import bs4 --hidden-import selenium --hidden-import openpyxl --hidden-import lxml

```

## 2. BlogPostingAuto113.py
**IMPORTANT NOTICE:**
This program is out-dated. This program is based on Chrome Driver version 113. You need to modify some codes to use it.

**Description:**
This program is primarily intended for uploading class schedules or announcements to specific blogs. To use it for other purposes, some code modifications may be necessary. The executable is based on Chrome Driver version 113 and may not work if your Chrome version differs. In such cases, download the Chrome Driver suitable for your computer and use PyInstaller to export the .py file to an .exe file again.

**Requirements:**
```python
pip install selenium, pyperclip, certifi, urllib3, pyautoit, autoit, webdriver_manager
```
you can download "autoit" programe [here](https://www.autoitscript.com/site/autoit/downloads/).

**Exporting as Executable:**
For PyInstaller, use the following command:
```cmd
pyinstaller BlogPostingAuto113.py --onefile --add-binary "chromedriver.exe;." --add-data="AutoItX3_x64.dll;autoit\lib" --hidden-import certifi --hidden-import urllib3 --hidden-import pyperclip --hidden-import webdriver-manager --hidden-import pyautoit --hidden-import autoit
```
---
---
# NaverBlog_Auto (한국어 설명) ❤️👍

NaverBlog_Auto는 네이버 블로그 대량 포스팅 및 댓글 수집을 위한 올인원 프로그램입니다.

## 1. NaverBlog_comments_collector.py

**설명:**
네이버 블로그에서 댓글을 수집하는 프로그램입니다. 블로그 링크를 입력하면 자동으로 인식됩니다. Chrome 123 환경에서 개발되었습니다.

**사용 방법:**
프로그램을 실행한 후 추적하려는 URL을 입력하십시오!

**요구 사항:**
```python
pip install pandas, bs4, selenium, openpyxl, lxml
```

**실행 파일로 내보내기:**
그 이후 아래 예시 코드를 활용해주세요.
```cmd
pyinstaller NaverBlog_comments_collector.py --onefile --hidden-import os --hidden-import re --hidden-import time --hidden-import datetime --hidden-import pandas --hidden-import bs4 --hidden-import selenium --hidden-import openpyxl --hidden-import lxml
```
## 2. BlogPostingAuto113.py
**중요 알림:**
이 프로그램은 오래된 버전입니다. 이 프로그램은 크롬 드라이버 버전 113을 기반으로 합니다. 코드를 사용하려면 일부 코드를 수정해야 합니다.

**설명**:
이 프로그램은 특정 블로그에 반별 시간표나 공지사항을 업로드하는 데 사용됩니다. 다른 목적으로 이용하기 위해서는 일부 코드 수정이 필요합니다. 실행 파일은 크롬 드라이버 버전 113을 기반으로 하며, 본인의 크롬 버전과 다를 경우 작동하지 않을 수 있습니다. 이 경우에는 본인의 컴퓨터에 맞는 크롬 드라이버를 다운로드하고 PyInstaller를 사용하여 .py 파일을 다시 .exe 파일로 내보내십시오.

**요구 사항**:
```python
pip install selenium, pyperclip, certifi, urllib3, pyautoit, autoit, webdriver_manager
```
"autoit" 프로그램은 [여기](https://www.autoitscript.com/site/autoit/downloads/) 에서 다운로드할 수 있습니다.

**실행 파일로 내보내기:**
그 이후 아래 예시 코드를 활용해주세요.
```cmd
pyinstaller BlogPostingAuto113.py --onefile --add-binary "chromedriver.exe;." --add-data="AutoItX3_x64.dll;autoit\lib" --hidden-import certifi --hidden-import urllib3 --hidden-import pyperclip --hidden-import webdriver-manager --hidden-import pyautoit --hidden-import autoit
```





