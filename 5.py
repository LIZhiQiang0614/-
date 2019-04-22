#import socket               # 导入 socket 模块
#import ssl
#host = '192.168.0.194'  #socket.gethostname() 
#s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # 创建 socket 对象
# # 获取本地主机名
#             # 设置端口号
#s_ssl = ssl.wrap_socket(s,
#                cert_reqs=ssl.CERT_REQUIRED,
#                ca_certs = 'ca.crt')   #cert.pem
#s_ssl.connect((host, 8005))
#s_ssl.send(b'hello!')
#print ("成功连接")
#print (s_ssl.recv(1024))
#s_ssl.close()
# 1024


import socket
import ssl


class client_ssl:
    ip = "127.0.0.1"
    port = 8005
    def send_hello(self,):
        # 生成SSL上下文
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        # 加载信任根证书
        context.load_verify_locations('cert.pem')


        # 与服务端建立socket连接
        with socket.create_connection((self.ip,self.port)) as sock:
            # 将socket打包成SSL socket
            # 一定要注意的是这里的server_hostname不是指服务端IP，而是指服务端证书中设置的CN，我这里正好设置成127.0.1而已
            with context.wrap_socket(sock, server_hostname='127.0.0.1') as ssock:
                # 向服务端发送信息
                msg = "你好吗 ?".encode("utf-8")
                ssock.send(msg)
                # 接收服务端返回的信息
                msg = ssock.recv(1024).decode("utf-8")
                print("receive msg from server :" , msg)
                ssock.close()


if __name__ == "__main__":
    client = client_ssl()
    client.send_hello()
