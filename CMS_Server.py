import socket
from os.path import exists
import os
import datetime
import _thread
from time import sleep


host = ""
port = 8888
txt_directory = 'C:\\Users\\Bymtech\\Desktop\\CMS_list\\'
mp4_directory = 'C:\\Users\\Bymtech\\Desktop\\CMS_video\\'

def server():

    server_socket = socket.socket()
    server_socket.bind((host, port))
    print("서버 오픈 접속 대기중")
    server_socket.listen(100)
# 단 하나의 client만 받는거에서 그치지 않고 또 다른 client의 접근에도 반응해주기 위해서
# 요청을 대기하는 listeningForClient 함수를 계속해서
# 반복을 돌려준다. 
    while True:
        listeningForClient(server_socket)
def time_now():
    now =datetime.datetime.now()
    return now

# client 로부터 받은 data 를 다시 client 에게 되돌려주는 echo 함수
def CMS_server(conn, address):
    data_transferred = 0
    bus_code = conn.recv(1024)
    bus_code = bus_code.decode() # 버스 코드
    filename = conn.recv(1024)
    filename = filename.decode() # 파일이름 이진 바이트 스트림 데이터를 일반문자열로 변환
    name_file,extention = os.path.splitext(filename)
    if extention == '.txt':
        directory = txt_directory + filename #경로설정
        print('ip: [%s] 버스 코드: [%s] 접속시간: [%s]'%(str(address),bus_code,str(time_now())))
    elif extention == '.mp4':
        print('ip: [%s] 버스 코드: [%s] 접속시간: [%s]'%(str(address),bus_code,str(time_now())))
        directory = mp4_directory + filename
    else:
        print("err")

    if not exists(directory): #파일이름이 존재하지 않으면
        print('해당파일이 없습니다.',directory)
        return #handle()함수 종료
    sleep(0.05)
    print('ip: [%s] 버스코드: [%s] 파일: [%s] 전송 시작...' %(str(address),bus_code,filename))
    with open(directory, 'rb') as f:
        try:
            data = f.read(1024) #파일을 1024바이트 읽음
            while data: #파일이 빈 문자열일때까지 반복
                data_transferred += conn.send(data)
                data = f.read(1024)
        except Exception as e:
                print(e)
    print('ip: [%s] 버스코드: [%s] 전송완료: [%s], 전송량: [%d],완료시간: [%s]' %(str(address),bus_code,filename,data_transferred,time_now()))
    
# client에서 통신이 끊어지면 소켓 서버를 닫아준다. 
    print('ip: [%s] 버스코드: [%s] 연결 종료' %(str(address),bus_code))
    conn.close()

# client를 기다리고 있는 CMS_server 서버 소켓 객체를 생성한다. 
def listeningForClient(server_socket):
    conn, address = server_socket.accept()
# echo 서버 소켓을 생성하게 되면 CMS_server 함수를 호출한다. 
    _thread.start_new_thread(CMS_server,(conn, address))


if __name__ == '__main__':
    server()