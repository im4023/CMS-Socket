import socket
import os

HOST = '192.168.0.47'
PORT = 8888

def getFileFromServer(busNum,filename,downloadpath):
    data_transferred=0
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
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST,PORT))
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