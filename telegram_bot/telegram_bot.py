#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta
import csv
import webbrowser
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import InlineKeyboardMarkup as MU
from telepot.namedtuple import InlineKeyboardButton as BT
from selenium import webdriver
import time
import schedule
from qbittorrent import Client
from dateutil.relativedelta import *


# # 1. 준비
# ### header||

# In[2]:


# pc용 및 모바일용
headers_pc = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"}
headers = {"User-Agent":"Mozilla/5.0 (iPhone; CPU iPhone OS 14_0_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1"}
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("disable-gpu")


# ### creat soup

# In[3]:


def create_soup_pc(url):
    res = requests.get(url,headers = headers_pc)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "lxml")
    return soup
def create_soup(url):
    browser = webdriver.Chrome("/usr/bin/chromedriver", chrome_options=options)
    browser.get(url)
    time.sleep(1)
    req = browser.page_source
    soup = BeautifulSoup(req, "lxml")
    return soup


# ### 텔레봇 관련

# In[4]:


token = "1391325068:AAEC4BDnp-iNMdc5S8kva-M8o2oQSizVhdQ"  #봇의 정체성?
mc = "1320457181"  # 이건 나!!
bot = telepot.Bot(token) # 봇을 실행하는 명령


# ### Qbittorrent 관련

# In[5]:


qb = Client("http://192.168.1.84:8080")
qb.login("hwanys2", "dnfwlq1352!")
# qb.download_from_link(magnet_link)


# # 2. riss 논문 검색

# In[6]:


# 학위 논문 검색
global num
num =30
def find_riss_uni(key, num):
    url = "http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query={keyword}&queryText=&iStartCount=0&iGroupView=5&icate=all&colName=bib_t&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale={number}".format(keyword = key, number=num)
    soup = create_soup_pc(url)
    riss_list = soup.find("div", attrs = {"class":"srchResultListW"}).select("div.srchResultListW > ul > li")
    title = "학위논문" + key + "검색 결과 \n"
    for riss in riss_list:
        riss_title = riss.select_one("div.cont > p.title > a").get_text()
        title = title + riss_title + "\n"
    return title
# 학술논문 제목검색
def find_riss_ko(key, num):
    url = "http://www.riss.kr/search/Search.do?isDetailSearch=N&searchGubun=true&viewYn=OP&query={keyword}&queryText=&iStartCount=0&iGroupView=5&icate=all&colName=re_a_kor&exQuery=&exQueryText=&order=%2FDESC&onHanja=false&strSort=RANK&pageScale={number}".format(keyword = key, number=num)
    soup = create_soup_pc(url)
    riss_list = soup.find("div", attrs = {"class":"srchResultListW"}).select("div.srchResultListW > ul > li")
    title = "학위논문" + key + "검색 결과 \n"
    for riss in riss_list:
        riss_title = riss.select_one("div.cont > p.title > a").get_text()
        title = title + riss_title + "\n"
    return title


# # 3. PPOM 게시판 알리미

# In[7]:


# 뽐뿌 최신 게시글 번호 불러오기
with open("/home/pi/coding/git_rasp/telegram_bot/ppom_max_num.txt", "r") as f:
    max_num = int(f.readline().replace("'",""))
# 뽐뿌 최신 게시글 번호 불러오기
def update_ppom_max_num():
    with open("/home/pi/coding/git_rasp/telegram_bot/ppom_max_num.txt", "w") as f:
        f.write(str(max_num))
def ppom():
    global max_num
    url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu"
    soup = create_soup_pc(url)
    posts = soup.find_all("tr", attrs = {"class":["list0", "list1"]})
    posts.reverse()
    for post in posts:
        recommend_num = post.find_all("td", attrs = {"class":"eng list_vspace"})[2].get_text().split(" ")[0]
        if recommend_num == "":
            recommend_num = 0
        if int(recommend_num) > 4 :
            num = post.find("td", attrs = {"class" : "eng list_vspace"}).get_text()
            if max_num < int(num) :
                title = post.find("font", attrs = {"class" : "list_title"})
                if title == None :
                    title = "종료된 게시글 입니다."
                    continue
                title = title.get_text()
                max_num = int(num)
                update_ppom_max_num()
                link_box = post.find("td", attrs = {"valign" : "middle"})
                link = "http://www.ppomppu.co.kr/zboard/" + link_box.find("a")["href"]
                message = title + "\n 링크 주소 : " + link 
                print(message)
                bot.sendMessage(mc, message)
# 뽐뿌 해외게시판 알리미
# 해외뽐뿌 최신 게시글 번호 불러오기
with open("/home/pi/coding/git_rasp/telegram_bot/global_ppom_max_num.txt", "r") as f:
    max_num_global = int(f.readline())
# 해외뽐뿌 최신 게시글 번호 불러오기
def update_globalppom_max_num():
    with open("/home/pi/coding/git_rasp/telegram_bot/global_ppom_max_num.txt", "w") as f:
        f.write(str(max_num_global))
def ppomglobal():    
    global max_num_global
    url = "http://www.ppomppu.co.kr/zboard/zboard.php?id=ppomppu4"
    soup = create_soup_pc(url)
    posts = soup.find_all("tr", attrs = {"class":["list0", "list1"]})
    posts.reverse()
    for post in posts:
        recommend_num = post.find_all("td", attrs = {"class":"eng list_vspace"})[2].get_text().split(" ")[0]
        if recommend_num == "":
            recommend_num = 0
        if int(recommend_num) > 4 :
            num = post.find("td", attrs = {"class" : "eng list_vspace"}).get_text()
            if max_num_global < int(num) :
                title = post.find("font", attrs = {"class" : "list_title"})
                if title == None :
                    title = "종료된 게시글 입니다."
                    continue
                title = title.get_text()
                max_num_global = int(num)
                update_globalppom_max_num()
                link_box = post.find("td", attrs = {"valign" : "middle"})
                link = "http://www.ppomppu.co.kr/zboard/" + link_box.find("a")["href"]
                message = title + "\n 링크 주소 : " + link
                print(message)
                bot.sendMessage(mc, message)


# # 4. Torrent 검색

# ### torrentz에서 검색하기

# In[8]:


max_find = 5
def find_torrent(keyword):
    magnets = []
    for i in range(max_find):
        magnets.append({"title" : "없어요.", "magnet":""})
    url = "http://torrentz.com/search?f={}".format(keyword)
    time.sleep(0.01)
    res = requests.get(url, headers=headers_pc)
    soup = BeautifulSoup(res.content, "lxml")
    results = soup.find("div", attrs = {"class":"results"}).find_all("dl", limit = max_find)
    results.reverse()
    try :
        for result in results:
            title = result.find("a").get_text()
            magnet = "magnet:?xt=urn:btih:" + result.find("a")["href"][1:]
            magnets.insert(0,{
                "title": title,
                "magnet": magnet,
            })
        return magnets
    except :
        bot.sendMessage(mc, "토렌트 검색 중 오류가 발생했습니다.")


# ### 텔레봇 버튼박스로 응답받기 - 버튼박스만드는 것은 텔레봇함수안에

# In[9]:


def query_ans(msg):
   query_id = msg['id']      # 팝업을 띄울때만 
   query_data = msg["data"]
   for i in range(max_find):
       if query_data == "download" + str(i):
           qb.download_from_link(magnets[i]["magnet"])
           bot.answerCallbackQuery(query_id, text = "다운로드 시작합니다")


# ### 네이버 vod 순위 검색

# In[10]:


# 영화 다운로드 리스트 만들고 열기
with open("/home/pi/coding/git_rasp/telegram_bot/movietop10.txt", "r") as f:
    movie_list=[]
    lines = f.readlines()
    for movie in lines:
        movie_list.append(movie.strip())

# 영화리스트 업데이트
def update_movie_list():
    with open("/home/pi/coding/git_rasp/telegram_bot/movietop10.txt", "w") as f:
        for movie in movie_list:
            data = movie + "\n"
            f.write(data)
            
# 영화 제목 평점 크롤링해오기
def find_movie():
    url = "https://serieson.naver.com/movie/top100List.nhn?rankingTypeCode=PC_M"
    soup = create_soup_pc(url)
    movie_box = soup.find("div", attrs={"class":"lst_thum_wrap"}).find_all("li", limit=10)
    for movie in movie_box:
        # 평점찾기
        score_num = float(movie.find("em", attrs={"class":"score_num"}).get_text())
        if score_num > 8:
            title = "".join(movie.find("strong").get_text().split()[1:])
            if title not in movie_list:
                magnets = find_torrent(title)
                if magnets == []:
                    continue
                for magnet in magnets:
                    msg_title = str(magnet['title']) + "/n 을 다운로드에 추가하였습니다."
                    msg_magnet = str(magnet['magnet'])
                    qb.download_from_link(msg_magnet)
                    bot.sendMessage(mc, msg_title)
                movie_list.append(title)
                update_movie_list()
# 영화 월간 순위 크롤링
def movie_rank_month():
    url = "https://serieson.naver.com/movie/top100List.nhn?rankingTypeCode=PC_M"
    soup = create_soup_pc(url)
    movie_box = soup.find("div", attrs={"class":"lst_thum_wrap"}).find_all("li", limit=10)
    movie_rank = "월간 영화 순위 \n"
    i=0
    for movie in movie_box:
        i+=1
        title = "".join(movie.find("strong").get_text().split()[1:])
        movie_rank = movie_rank + str(i) +"위 :" + title + "\n"    
    return movie_rank


# # 5. 네이버 기업 뉴스 크롤링

# ### 종목 리스트 관리

# In[11]:


# 관심종목 불러오기
with open("/home/pi/coding/git_rasp/telegram_bot/inter_company.txt", "r") as f:
    com_list=[]
    lines = f.readlines()
    for com in lines:
        com_list.append(com.strip())

# 관심종목 업데이트
def update_inter():
    with open("/home/pi/coding/git_rasp/telegram_bot/inter_company.txt", "w") as f:
        for com in com_list:
            data = com + "\n"
            f.write(data)
            
# 종목 및 코드 dcit 만들기 csv파일에서 읽어와서 만들기
stock_dict = {}
f = open("/home/pi/coding/git_rasp/telegram_bot/data.csv", "r")
reader = csv.DictReader(f)
for row in reader:
    stock_dict[row['기업명']] = row['종목코드']
f.close()


# ### 종목뉴스 가져오기

# In[12]:


all_news = ""
today = str(datetime.today())
month = today[5:7]
day = today[8:10]
# 종목명 넣고 뉴스 가져오기 함수
def company_news(company):
    company_code = stock_dict[company]
    url = "https://m.stock.naver.com/item/main.nhn#/stocks/{}/news".format(company_code)
    soup = create_soup(url)
    news_list = soup.find("ul", attrs={"class":"news_lst _list_wrap"}).find_all("li", limit=6)
    company_title_link = {}
    for news in news_list:
        date = news.find("em").get_text().strip()
        if date[0] == "오":
            title = news.find("strong", attrs={"class":"title"}).get_text().strip()
            link = "https://m.stock.naver.com/item/main.nhn" + news.find("a")["href"]
            company_title_link[title + "      작성일 : " + date] = [link]
        elif date[-1] == "전":
            title = news.find("strong", attrs={"class":"title"}).get_text().strip()
            link = "https://m.stock.naver.com/item/main.nhn" + news.find("a")["href"]
            company_title_link[title + "      작성일 : " + date] = [link]            
        elif  date[-5:-3] == month and date[-2:] == str(int(day)-1).zfill(2):
            title = news.find("strong", attrs={"class":"title"}).get_text().strip()
            link = "https://m.stock.naver.com/item/main.nhn" + news.find("a")["href"]
            company_title_link[title + "      작성일 : " + date] = [link]
        else:
            break
    print(company_title_link)
    return company_title_link
# 뉴스 최대4개만 합치기
def send_news(compane_name):
    global all_news
    if compane_name == {}:
        None
    elif len(compane_name) > 0:
        all_news = all_news + "\n" + str(list(compane_name.keys())[0]) + "\n" + str(list(compane_name.values())[0])[2:-2]+ "\n"
        if len(compane_name) > 1:
            all_news = all_news + "\n" + str(list(compane_name.keys())[1]) + "\n" + str(list(compane_name.values())[1])[2:-2]+ "\n"

            if len(compane_name) > 2:
                all_news = all_news + "\n" + str(list(compane_name.keys())[2]) + "\n" + str(list(compane_name.values())[2])[2:-2]+ "\n"

                if len(compane_name) > 3:    
                    all_news = all_news + "\n" + str(list(compane_name.keys())[3]) + "\n" + str(list(compane_name.values())[3])[2:-2]+ "\n"
                    
# 텔레그램으로 모아진 뉴스 보내기(관심종목에있는 모든 뉴스)
def sendtelegram():
    global all_news
    global com_list
    for com in com_list:
        all_news = all_news + "\n" + com + "의 새로운 뉴스입니다." + "\n" 
        samsung = company_news(com)
        send_news(samsung)
        print(com, " 뉴스 검색 완료")
    bot.sendMessage(mc, all_news,disable_web_page_preview=True)


# # 6. 텔레그램 대화봇

# In[13]:


def handle(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
 
    if content_type == 'text':
        # 안녕메세지보내기
        hello_list =['안녕','HELLO','반가워','NICE TO MEET YOU', '반갑습니다', "하이","안녕하세요","헬로우"]
        if msg['text'].upper() in hello_list:
            bot.sendMessage(chat_id, 'Hello')
        # 도움말
        elif msg['text'].upper() == '도움말':
            msg = "특정 종목 뉴스 보여주기 : 종목명 \n 관심종목 추가하기 : 종목추가종목명\n 관심종목 삭제하기 : 종목삭제종목명                \n 관심종목 목록보기 : 관심종목 \n 관심종목 뉴스보기 : 전체뉴스 \n 토렌트 검색 방법 : 토렌트 파일명 \n                 토렌트 검색 페이지 변경 : 페이지 숫자 \n 페이지확인 : 현재페이지 \n                 토렌트 검색 개수 변경 : 검색개수 숫자 \n 페이지확인 : 현재검색개수 \n 영화순위 \n 학위논문-검색키워드- \n 논문검색개수20" 

            bot.sendMessage(chat_id, msg)
        # 종목명을 입력하면 종목 뉴스 보여주기
        elif msg['text'].upper() in stock_dict.keys():
            com_news = company_news(msg['text'])
            send_msg = ""
            if com_news == {}:
                send_msg = "최신 뉴스가 없습니다."
                bot.sendMessage(chat_id, send_msg)
            else:
                for key, val in com_news.items():
                    send_msg = send_msg + "\n" + str(key) + str(val)[2:-2] + "\n"
                bot.sendMessage(chat_id, send_msg, disable_web_page_preview=True)
        # 관심종목 추가하기
        elif msg['text'][0:4] == "종목추가":
            if msg['text'][4:].upper().strip() in stock_dict.keys():
                com_list.append(msg['text'][4:].upper().strip())
                bot.sendMessage(chat_id, "종목이 추가 되었습니다.")
                update_inter()
            else:
                bot.sendMessage(chat_id, "종목명을 다시 확인하십시요.")
                print(com_list)
        # 관심종목 삭제하기
        elif msg['text'][0:4] == "종목삭제":
            if msg['text'][4:].upper().strip() in com_list:
                com_list.remove(msg['text'][4:].upper().strip())
                bot.sendMessage(chat_id, "종목이 삭제되었습니다.")
                update_inter()
            else:
                bot.sendMessage(chat_id, "종목명을 다시 확인하십시요.")
        # 관심종목 목록 보내기
        elif msg['text'] == "관심종목":
            inter_com = ""
            for com in com_list:
                inter_com = inter_com + " " + com
            bot.sendMessage(chat_id, inter_com)
        # 전체 뉴스 보내주기
        elif msg['text'] == "전체뉴스":
            sendtelegram()
        # 토렌트 검색해주기
        elif msg['text'].startswith("토렌트") is True:
            global magnets
            global max_find
            magnets = find_torrent(msg['text'][3:].strip())
            arr = []
            for i in range(max_find):
                arr.append([BT(text=magnets[i]["title"], callback_data = "download" + str(i))])
                mu = MU(inline_keyboard = arr)
            bot.sendMessage(mc, "뭘 받을까?", reply_markup=mu)
        # 토렌트 최대 검색 개수 변경하기
        elif msg['text'][0:4] == "검색개수":
            try:
                max_find= int(msg['text'][4:].strip())
                bot.sendMessage(chat_id, "토렌트 최대 검색개수 변경하였습니다.")
            except:
                bot.sendMessage(chat_id, "명령어를 다시 확인하세요")
        # 토렌트 최대 검색 개수 확인하기
        elif msg['text'] == "현재검색개수":
            bot.sendMessage(chat_id, max_find) 
        # 영화순위
        elif msg['text'] == "영화순위":
            movie_rank = movie_rank_month()
            bot.sendMessage(chat_id, movie_rank)            
        # 학위논문 검색
        elif msg['text'][0:4] == "학위논문":
            global num
            title = find_riss_uni(msg['text'][4:], num)
            bot.sendMessage(chat_id, title)
        # 학술논문 검색
        elif msg['text'][0:4] == "학술논문":
            title = find_riss_ko(msg['text'][4:], num)
            bot.sendMessage(chat_id, title)

        # 논문 최대 검색 개수 변경하기
        elif msg['text'][0:6] == "논문검색개수":
            try:
                num= int(msg['text'][6:].strip())
                bot.sendMessage(chat_id, "논문 최대 검색개수를 변경하였습니다.")  
            except:
                bot.sendMessage(chat_id, "명령어를 다시 확인하세요")
        else:
            bot.sendMessage(chat_id, '지원하지 않는 기능입니다')


# # 7. 알림 관련

# In[14]:


# 날씨 정보
def scrape_weather():
    url = "https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=광양읍+날씨&oquery=광양+날씨&tqi=UGp1owp0J14ssfhvaKNssssstQd-346753"
    soup = create_soup_pc(url)
    # 흐림, 어제보다 OO˚ 높아요
    cast = soup.find("p", attrs={"class":"cast_txt"}).get_text()
    # 현재 OO℃  (최저 OO˚ / 최고 OO˚)      
    curr_temp = soup.find("p", attrs={"class":"info_temperature"}).get_text().replace("도씨", "") # 현재 온도
    min_temp = soup.find("span", attrs={"class":"min"}).get_text() # 최저 온도
    max_temp = soup.find("span", attrs={"class":"max"}).get_text() # 최고 온도
    # 오전 강수확률 OO% / 오후 강수확률 OO%
    morning_rain_rate = soup.find("span", attrs={"class":"point_time morning"}).get_text().strip() # 오전 강수확률
    afternoon_rain_rate = soup.find("span", attrs={"class":"point_time afternoon"}).get_text().strip() # 오후 강수확률

    # 미세먼지 OO㎍/㎥좋음
    # 초미세먼지 OO㎍/㎥좋음
    dust = soup.find("dl", attrs={"class":"indicator"})
    pm10 = dust.find_all("dd")[0].get_text() # 미세먼지
    pm25 = dust.find_all("dd")[1].get_text() # 초미세먼지

    # 출력
    we_cast = cast + "\n" + "현재 {} (최저 {} / 최고 {})".format(curr_temp, min_temp, max_temp)     + "\n" + "오전 {} / 오후 {}".format(morning_rain_rate, afternoon_rain_rate)     + "\n" + "미세먼지 {}".format(pm10) + "\n" + "초미세먼지 {}".format(pm25) + "\n" + "\n"
    return we_cast

def morning_alarm():
    dasl_time = (datetime.today() - datetime(2020,2,22)).days
    now = datetime.now()
    year, month, day = 2020, 2, 23
    hwan_year, hwan_month, hwan_day = 1987, 4, 14
    day = relativedelta(now, datetime(year, month, day))
    hwan_day = relativedelta(now, datetime(hwan_year, hwan_month, hwan_day))
    wedding_time = (datetime.today() - datetime(2019,1,4)).days
    t = ["월", "화", "수", "목", "금", "토", "일"]
    r = datetime.today().weekday()
    weather = scrape_weather()
    today = str(datetime.today().month) + "월 " + str(datetime.today().day) + "일 " + t[r] +"요일 입니다."
    msg = today + "\n"*2 + "다슬이 생후 " + str(dasl_time) + "일 \n"     + '%s 년 %s 개월 %s 일' %(day.years, day.months, day.days) + "일 되는 날입니다. \n"     + "내가 태어난지 " + '%s 년 %s 개월 %s 일' %(hwan_day.years, hwan_day.months, hwan_day.days) + " 되는 날입니다. \n"     + "결혼한지 " + str(wedding_time) + "일 되는 날입니다. \n \n" + weather
    bot.sendMessage(mc, msg)



# # 8. 반복

# In[ ]:


# 반복 및 스케쥴 관리
schedule.every(11).minutes.do(ppom)
schedule.every(17).minutes.do(ppomglobal)
schedule.every().day.at("08:30").do(sendtelegram)
schedule.every().day.at("07:00").do(morning_alarm)
schedule.every().friday.at("17:00").do(find_movie)

bot = telepot.Bot(token)
MessageLoop(bot, {'chat' : handle, 'callback_query' : query_ans}).run_as_thread()

while True:
    schedule.run_pending()
    time.sleep(50)

