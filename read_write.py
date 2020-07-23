#read_write
import file_download
import os
import sys
import time

# 노선 코드
busNum = "ex_1"
busNumSuffix = ".txt"
weather = "weather.txt"
rootdir = "/home/pi/CMS/"
downloadPath = "/home/pi/CMS/ad/"
connect_result =""

print("this busNum is [%s]" %busNum)

if not busNum.endswith(busNumSuffix):
    txtbusNum = "".join((busNum + ".txt",))

if os.path.exists(downloadPath + txtbusNum):
    # busNum.txt delete
    os.remove(downloadPath + txtbusNum)
    print("delete old ad_list")



# 노선광고파일(노선코드.txt) 다운로드
connect_result = file_download.getFileFromServer(busNum,txtbusNum,downloadPath)
if connect_result == True:
    print("downlaod new ad_list")

    stay_list =[]
    delete_list = []
    download_list=[]

    # 노선광고파일과 ad_list 비교하여 삭제, 유지, 다운로드 리스트 작성
    print("시작")
    with open (rootdir + 'ad/ex_1.txt', 'r', encoding='utf8') as base:
        if not os.path.exists(rootdir + 'ad_list.txt'):
            print("don't exsist ad_list.txt")
            try:
                f = open(rootdir + "ad_list.txt", 'w', encoding='utf8')
                f.close()
            except OSError:
                print('failed make ad_list.txt')
                sys.exit(1)
            else:
                print('maked ad_list.txt') 
        with open(rootdir + 'ad_list.txt', 'r', encoding='utf8') as ad_list:
            ad_list = ad_list.readlines()
            base = base.readlines()

            base.sort()
            ad_list.sort()

            for ad_txt in ad_list:
                for baseitem in base:
                    if ad_txt == baseitem:
                        base.remove(baseitem)
                        stay_list.append(ad_txt)
                        break
                else: #nobreak
                    delete_list.append(ad_txt)


            if base:
                download_list = base
                
    print("stay:",stay_list)
    print("delete:",delete_list)
    print("downlaod",download_list)

    # 노선광고 txt파일 삭제
    os.remove(downloadPath + txtbusNum)

    # 영상 파일 삭제
    for xx in delete_list:
        
        removePath = downloadPath + xx.strip(" \t\r\n")
        try:
            os.remove(removePath)
            print("파일 [%s] 삭제" %removePath)
        except OSError:
            print("파일 [%s] 삭제 실패" %removePath)

    # 영상 파일 다운로드
    for ii in download_list:
        connect_result = file_download.getFileFromServer(busNum,ii.strip(" \t\r\n"),downloadPath)
        if connect_result != True:
            os.remove(downloadPath+ ii.strip(" \t\r\n"))
            print("다운로드 중 오류 발생으로 삭제된 파일: ", ii)
            print("\n")

    # ad_list 새로 작성
    with open(rootdir + 'ad_list.txt', 'w', encoding='utf8') as ad_list:
        for w1 in stay_list:
            ad_list.write(w1)
        for w2 in download_list:
            ad_list.write(w2)
else:
    print("server connect err")
    pass

while True:
    # 날씨파일(weather.txt) 다운로드
    connect_result = file_download.getFileFromServer(busNum,weather,rootdir)
    if connect_result == True:
        print("download update weather")
        time.sleep(7200)
    else:
        os.remove(rootdir+ weather)
        print("download weather err")
        time.sleep(7200)