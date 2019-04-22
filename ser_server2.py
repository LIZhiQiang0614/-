import socket
import ssl
import threading


class WSGIServer(object):

    # 初始化，实例化类的时候直接加载
    def __init__(self,ip,port):
        """初始化对象"""
        # 生成SSL上下文               # 指定ssl版本
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        # 加载信任根证书                       注意关键字传参！！！！
        self.context.load_cert_chain(certfile="cert/ca.crt", keyfile="cert/ca.key")
        # self.context.load_verify_locations('cert.pem')  # server端的证书
        # self.context.load_verify_locations('key.pem')  # server端的
        print("现在证书啥的都加载完成了")
        # 创建套接字
        print(self.context)
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 解决程序端口占用问题
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定本地ip地址
        self.tcp_server_socket.bind((ip, port))
        # 将套接字变为监听套接字，最大连接数量为100
        self.tcp_server_socket.listen(100)
        print("最大连接数是100昂")

    # 程序的主要函数，创建连接线程
    def run_forever(self):
        """设备连接"""
        print("等待设备的链接ing。。。")
        print("等待生产新的套接字。。。")

        with self.context.wrap_socket(self.tcp_server_socket, server_side=True) as ssock:
            while 1:
                # 等待设备的链接，获取链接后的套接字new_socket
                new_socket, client_addr = ssock.accept()
                print("设备{0}已连接".format(client_addr))

                # 2.创建线程处理设备的需求            线程处理的函数           需要的参数
                t1 = threading.Thread(target=self.service_machine, args=(new_socket, client_addr))
                t1.start()

    # 业务处理的主要函数
    def service_machine(self, new_socket, client_addr):
        """业务处理"""
        while 1:
            # 3.接收设备发送的数据，单次最大1024字节，按‘gbk’格式解码
            receive_data = new_socket.recv(1024).decode("utf-8")
            # 4.如果设备发送的数据不为空
            if receive_data:
                # 4.1 打印接收的数据，这里可以将设备发送的数据写入到文件中
                # 获取设备的ID信息
                print(receive_data)
                if receive_data[0:6] == "report":
                    response = "SET OK:" + receive_data
                else:
                    receive_data = receive_data[6:].split(",")[0]
                    # 拼接响应数据
                    response = "alarm=" + receive_data + ",Switch:clear"
                print(response)
                # 4.2 返回原数据作为应答，按‘utf-8’格式编码
                new_socket.send(response.encode("utf-8"))
            # 5.当设备断开连接时，会收到空的字节数据，判断设备已断开连接
            else:
                print('设备{0}断开连接...'.format(client_addr))
                break

        # 关闭套接字
        new_socket.close()


# 主执行文件
def main(ip,port):
    """创建一个WEB服务器"""
    wsgi_server = WSGIServer(ip,port)
    print("服务器已开启")
    wsgi_server.run_forever()

# 程序执行的开始 指定ip及port
if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8005
    main(ip,port)
