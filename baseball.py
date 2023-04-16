import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from time import sleep
import os

Msrc_list = []

URL = "https://baseball.yahoo.co.jp/npb/game/2021006290/top"
res = requests.get(URL)
soup = BeautifulSoup(res.content, "html.parser")

Lsrc = soup.find_all("a", class_="bb-gameScoreTable__score")

# リンクをリスト化
for element in Lsrc:
  Msrc = element.get("href")
  Msrc_list.append("https://baseball.yahoo.co.jp" + str(Msrc))

# print(Msrc_list)


# 回ごとのぺージ処理
cnt = 1
half = len(Msrc_list) / 2
Tout = ""
# # フォルダを作成
os.makedirs("表の内容", exist_ok=True)
os.makedirs("裏の内容", exist_ok=True)
os.makedirs("表 投球内容の画像/", exist_ok=True)
os.makedirs("裏 投球内容の画像/", exist_ok=True)

for i in Msrc_list:
  u_cnt = 1
  u_cnt2 = 1
  df = pd.read_html(i, encoding="utf-8")
  while not "●●●●" in Tout: #わざと間違っている
  # データ取得
    
    if half+1 > cnt:
      # 前半
      condf =pd.concat([df[13], df[14]], axis=1)
      nandf =condf.fillna(method='ffill', limit=8)
      nandf.to_csv("表の内容//"+str(cnt)+"回表_"+str(u_cnt)+"打席目"+".csv", " ", index=False, encoding="utf-8")

    else:
      # 後半   
      cnt2 = cnt - half
      condf =pd.concat([df[13], df[14]], axis=1)
      nandf =condf.fillna(method='ffill', limit=8)
      nandf.to_csv("裏の内容//"+str(int(cnt2))+"回裏_"+str(u_cnt2)+"打席目"+".csv", " ", index=False, encoding="utf-8")
      
    u_cnt += 1
    u_cnt2 += 1
    
    # print("End For")
    
    # 3アウトの識別
    res = requests.get(i)
    soup = BeautifulSoup(res.content, "html.parser")
    out = soup.find("p", class_="o")
    Tout = out.find("b")
    if "●●●" in Tout:
      print("3out")
      break
            
    else :
      # 次の打者へ
      next = soup.find("a", id="btn_next")
      link_next = next.get("href")
      i = "https://baseball.yahoo.co.jp" + link_next
      print(i)
      df = pd.read_html(i, encoding="utf-8")
  cnt += 1 
print("データ取得終了") 



# スクリーンショット処理
print("スクリーンショット開始")
options = Options()
options.add_argument("--headless")

service = Service("C:\chromedriver_win32\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
cnt = 1
u_cnt = 1
u_cnt2 = 1
half = len(Msrc_list) / 2
Ssrc_list = []
Tout = ""
for i in Msrc_list:
  u_cnt = 1
  u_cnt2 = 1
  driver.get(i)
  sleep(2)

  while not "●●●●" in Tout: #わざと間違っている
    
    if half+1 > cnt:
      # 前半
      # ページのサイズを取得してドライバーに設定
      w = driver.execute_script('return document.body.scrollWidth')
      h = driver.execute_script('return document.body.scrollHeight')
      driver.set_window_size(w, h)

      # 範囲を指定してスクリーンショットを撮る
      if driver.find_elements(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--leftBatter'):
        png = driver.find_element(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--leftBatter').screenshot_as_png
      elif driver.find_elements(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--rightBatter'):
        png = driver.find_element(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--rightBatter').screenshot_as_png

      # フォルダに保存
      with open("表 投球内容の画像/"+ str(cnt) +"回表_" + str(u_cnt) + "打席目" + '.png', 'wb') as f:
        f.write(png)
     
    else:
      # 後半   
      # ページのサイズを取得してドライバーに設定
      w = driver.execute_script('return document.body.scrollWidth')
      h = driver.execute_script('return document.body.scrollHeight')
      driver.set_window_size(w, h)

      # 範囲を指定してスクリーンショットを撮る
      if driver.find_elements(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--leftBatter'):
        png = driver.find_element(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--leftBatter').screenshot_as_png
      elif driver.find_elements(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--rightBatter'):
        png = driver.find_element(By.CLASS_NAME, 'bb-splitsTable__data.bb-splitsTable__allocationChartBg--rightBatter').screenshot_as_png

      # フォルダに保存
      cnt2 = cnt-half
      with open("裏 投球内容の画像/"+ str(int(cnt2)) +"回裏_" + str(u_cnt2) + "打席目" + '.png', 'wb') as f:
        f.write(png)

    u_cnt += 1
    u_cnt2 += 1
      # 3アウトの識別
    res = requests.get(i)
    soup = BeautifulSoup(res.content, "html.parser")
    out = soup.find("p", class_="o")
    Tout = out.find("b")
    if "●●●" in Tout:
      print("3out")
      break
            
    else :
      # 次の打者へ
      next = soup.find("a", id="btn_next")
      link_next = next.get("href")
      i = "https://baseball.yahoo.co.jp" + link_next
      print(i)
      driver.get(i)
      sleep(1)

  cnt+=1

driver.close()
driver.quit()
print("スクリーンショット終了")

# #画像リンクを表に追加
# cnt=1
# for i in range(1,9):
#   df = pd.read_csv("naiyou"+str(cnt)+".csv", " " ,encoding="Shift_JIS")
#   df.insert(1,"詳しい投球内容", 'C:/Users/joyun/OneDrive/デスクトップ/base-scrape/base_image/screenshot' + str(cnt)+'.png')
#   pd.DataFrame(df).to_csv("naiyou"+str(cnt)+".csv", " " ,encoding="Shift-JIS")
#   cnt+=1
# # print("リンク")