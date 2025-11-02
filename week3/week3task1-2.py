
#task1

import urllib.request as req
import json, csv


URL_CN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-ch"
URL_EN = "https://resources-wehelp-taiwan-b986132eca78c0b5eeb736fc03240c2ff8b7116.gitlab.io/hotels-en"


with req.urlopen(URL_CN) as R:
    info_cn = json.load(R)
with req.urlopen(URL_EN) as R:
    info_en = json.load(R)

data_cn = info_cn["list"]
data_en = info_en["list"]


en_by_id = {} 
for h in data_en:
    if isinstance(h, dict) and "_id" in h:
        key = h["_id"]
        en_by_id[key] = h

with open("hotels.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["ChineseName", "EnglishName", "ChineseAddress", "EnglishAddress", "Phone", "RoomCount"])

    count = 0
    for c in data_cn:
        if not isinstance(c, dict) or "_id" not in c:
            continue

        _id = c["_id"]
        if _id in en_by_id:
            e = en_by_id[_id]
        else:
            e = {}

        chinese_name = c.get("旅宿名稱", "")
        english_name = e.get("hotel name", "")
        chinese_addr = c.get("地址", "")
        english_addr = e.get("address", "")
        phone        = c.get("電話或手機號碼", "")
        if phone == "":  
            phone = e.get("tel", "")
        room_count   = c.get("房間數", "")
        if room_count == "":  
            room_count = e.get("the total number of rooms", "")
      
        w.writerow([chinese_name, english_name, chinese_addr, english_addr, phone, room_count])
        count += 1

print("hotels.csv完成。")

def extract_district(address):
    if not address:
        return ""
  
    if "臺北市" in address:
        parts = address.split("臺北市", 1)
        if len(parts) > 1:
            after = parts[1]
            if "區" in after:
                before_district = after.split("區", 1)[0]
                return before_district + "區"

    if "台北市" in address:
        parts = address.split("台北市", 1)
        if len(parts) > 1:
            after = parts[1]
            if "區" in after:
                before_district = after.split("區", 1)[0]
                return before_district + "區"
 
    if "區" in address:
        before_district = address.split("區", 1)[0]
        if len(before_district) >= 3:
            return before_district[-3:] + "區"
        else:
            return before_district + "區"

    return ""  

def to_int(value):
    try:
        return int(value)
    except:
        return 0


districts = {}  # 例如：{"中正區": {"hotels": set(), "rooms": 0}, ...}

for c in data_cn:
    if not isinstance(c, dict) or "_id" not in c:
        continue

    _id = c["_id"]
    address = c.get("地址", "")
    district = extract_district(address)
    if district == "":
        continue  
    
    rooms_cn = to_int(c.get("房間數", ""))
    
    if _id in en_by_id:
        rooms_en = to_int(en_by_id[_id].get("the total number of rooms", ""))
    else:
        rooms_en = 0

 
    rooms = rooms_cn if rooms_cn > 0 else rooms_en

    #區名第一次出現，先幫它建立一個容器
    if district not in districts:
        districts[district] = {"hotels": set(), "rooms": 0}

    #如果這個id沒出現過，才加入。
    if _id not in districts[district]["hotels"]:
        districts[district]["hotels"].add(_id)
        districts[district]["rooms"] += rooms

with open("districts.csv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f)
    w.writerow(["DistrictName", "HotelCount", "RoomCount"])


    names = list(districts.keys())
    names.sort()
    for name in names:
        hotel_count = len(districts[name]["hotels"])
        room_count = districts[name]["rooms"]
        w.writerow([name, hotel_count, room_count])

print("districts.csv完成")


#task2

import urllib.request as req
import bs4
import csv


def getTime(articleURL):
    request = req.Request(articleURL, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    })
    try:
        with req.urlopen(request) as response:
            data = response.read().decode("utf-8")
        root = bs4.BeautifulSoup(data, "html.parser")  
        singlepage = root.find_all("span",class_="article-meta-value")
        if len(singlepage) >=4: #順序分別為作者>看板>標題>時間
            return singlepage[3].text.strip()
        else:
            return "(無時間資料)"
    except Exception as e: #如果抓文章的過程中發生錯誤不要讓整個程式停止，而是回傳錯誤內容
        return f"(讀取失敗:{e})"



def getData(url,writer):#抓取一頁的標題、推文數、發文時間並寫入CSV
    request = req.Request(url, headers={
     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
        })
    with req.urlopen(request) as response:
        data = response.read().decode("utf-8")

       
    root = bs4.BeautifulSoup(data, "html.parser")  
    titles = root.find_all("div", class_="title")  # 尋找所有class="title"的div標籤
    pushs =root.find_all("div",class_="nrec")
        
    for title,push in zip(titles,pushs):
        if title.a:  # 如果標題包含a標籤(沒有被刪除)印出來
            titleName=title.a.get_text(strip=True)
            link="https://www.ptt.cc"+title.a["href"]
            push_text = push.get_text(strip=True) if push else ""
            postTime =getTime(link)
            #print(f"{titleName},{push_text},{postTime}")
            writer.writerow([titleName, push_text, postTime])

    nextLink=root.find("a",string="‹ 上頁") 
    return nextLink["href"] if nextLink else None

pageURL="https://www.ptt.cc/bbs/Steam/index.html"


with open("articles.csv", "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f)


    count = 0
    while count < 3:  # 爬 3 頁
        nextPage = getData(pageURL, writer)
        if not nextPage:
            break
        pageURL = "https://www.ptt.cc" + nextPage
        count += 1

print("已寫入 articles.csv")


