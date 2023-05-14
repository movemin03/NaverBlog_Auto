# BlogPostingAuto

have to pip install: selenium pyautoit webdriver_manager pyperclip certifi urllib3

I use like this to make exe file with Pyinstaller pyinstaller BlogPostingAuto113.py --onefile --add-binary "chromedriver.exe;." --add-data="AutoItX3_x64.dll;autoit\lib" --hidden-import certifi --hidden-import urllib3 --hidden-import pyperclip --hidden-import webdriver-manager --hidden-import pyautoit --hidden-import autoit
