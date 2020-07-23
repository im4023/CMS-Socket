import socket
import os

HOST = '192.168.0.47'
PORT = 8888

def getFileFromServer(busNum,filename,downloadpath):
    # data_transferred 초기화
    data_transferred=0
    # downloadpath 경로 확인
    if not os.path.exists(downloadpath):
        print("don't exsist ad")
        try:
            os.makedirs(downloadpath)
        except OSError:
            print('failed make dir')
            return
        else:
            print('maked ad')
        
        
    try:
        # 소켓 설정                
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            # 서버 연결
            sock.connect((HOST,PORT))
            # 인코딩 후 전송
            sock.sendall(busNum.encode())
            sock.sendall(filename.encode())
            
            data = sock.recv(1024)
            if not data:
                print('파일[%s]: 서버에 존재하지 않거나 전송중 오류발생' %filename)
                return
            
            with open(downloadpath +'/'+ filename,'wb')as f:
                try:
                    while data:
                        f.write(data)
                        data_transferred += len(data)
                        data = sock.recv(1024)
                except Exception as e:
                    print(e)
                    
            print('파일[%s] 전송종료. 전송량 [%d]' %(filename, data_transferred))
        return True
    except Exception:
        return False        