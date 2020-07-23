import requests
from bs4 import BeautifulSoup
import os
import sys
import threading
import datetime

txt_directory = 'C:\\Users\\Bymtech\\Desktop\\CMS_list\\'
ii = 0

def time_now():
    now =datetime.datetime.now()
    return now

def weather_crawling():        
    #크롤링 주소 설정
    source = requests.get("https://search.naver.com/search.naver?sm=tab_hty.top&where=nexearch&query=%EB%8C%80%EC%A0%84+%EB%91%94%EC%82%B0%EB%8F%99+%EB%82%A0%EC%94%A8&oquery=%EB%8C%80%EC%A0%84+%EC%A4%91%EA%B5%AC+%EB%91%94%EC%82%B0%EB%8F%99+%EB%82%A0%EC%94%A8&tqi=UXVjWsprvN8ssLWyAsNssssssE0-163158").text
    soup = BeautifulSoup(source, "html.parser")

    # 긁어올 데이터 설정 soup.select("tag.class")
    temper = soup.select("span.todaytemp")
    #weather = soup.select("p.cast_txt")
    dust = soup.select("span.num")
    moisture=soup.find_all('dd',{'class' : 'weather_item _dotWrapper'})
   
    today_temp = temper[0].text.strip()
    today_dust = dust[4].text.strip()
    today_moisture = moisture[24].text.strip()
    print('현재시간: ', time_now())
    print('현재온도: ',today_temp)
    #print('오늘날씨: ',weather[0].text)
    print('미세먼지: ',today_dust)
    print('현재습도: ',today_moisture)
   
    # weather 파일 확인, 없으면 재생성
    if not os.path.exists(txt_directory + 'weather.txt'):
        print("don't exsist weather.txt")
        try:
            f = open(txt_directory + 'weather.txt', 'w', encoding='utf8')
            f.close()
        except OSError:
            print('failed make weather.txt')
            sys.exit(1)
        else:
            print('maked weather.txt') 

    # weather.txt 새로 작성
    with open(txt_directory + 'weather.txt', 'w', encoding='utf8') as add_weather:
        add_weather.write(",".join([today_temp, today_dust,today_moisture]))
        add_weather.write("\r\n")
        #add_weather.write(weather[0])

    # 온습도, 미세먼지 값을 확인하여 null이 있으면 weather파일 삭제
    if today_temp == None or today_dust == None or today_moisture == None:
        os.remove(txt_directory + 'weather.txt')
        print("오류가 있어 파일이 삭제되었습니다.")
    threading.Timer(7200, weather_crawling).start()

if __name__ == '__main__':
    weather_crawling()