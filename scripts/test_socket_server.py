import socket
import threading
from datetime import datetime
import time

HOST_IP = "163.221.44.222"  # サーバーのIPアドレス
PORT = 12345  # 使用するポート
CLIENTNUM = 3  # クライアントの接続上限数
DATESIZE = 1024  # 受信データバイト数


class SocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
    
    def conn_client(self, client_socket, address):
        with client_socket:
            while True:
                rcv_data = client_socket.recv(DATESIZE)  # クライアントからデータ受信
                set_data = 'SET_OK'
                set_data = set_data.encode('utf-8')
                if rcv_data:
                    print('[{0}] recv date : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                         rcv_data.decode('utf-8')))
                    if rcv_data.decode('utf-8') == 'initialize':
                        time.sleep(10)
                        # client_socket.send(rcv_data)  # データ受信したデータをそのままクライアントへ送信
                        client_socket.send('done_initialization'.encode('utf-8'))
                    elif rcv_data.decode('utf-8') == 'finalize':
                        time.sleep(10)
                        client_socket.send('done_finalization'.encode('utf-8'))
                    else:
                        out_data = 'SET_OK' + '_' + rcv_data.decode('utf-8')
                        out_data = out_data.encode('utf-8')
                        time.sleep(10)
                        client_socket.send(out_data)
                else:
                    break
        
        print('[{0}] disconnect client -> address : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                address))
    
    def run_server(self):
        # サーバー起動
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((self.host, self.port))
            server_socket.listen(CLIENTNUM)
            print('[{}] run server'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            
            while True:
                client_socket, address = server_socket.accept()  # クライアントからの接続要求受け入れ
                print('[{0}] connect client -> address : {1}'.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                                                                     address))
                client_socket.settimeout(60)
                t = threading.Thread(target=self.conn_client, args=(client_socket, address))
                t.setDaemon(True)
                t.start()  # クライアントごとにThread起動 send/recvのやり取りをする


if __name__ == "__main__":
    SocketServer(HOST_IP, PORT).run_server()
