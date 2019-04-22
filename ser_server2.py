import socket
import ssl
import threading


class WSGIServer(object):

    # ��ʼ����ʵ�������ʱ��ֱ�Ӽ���
    def __init__(self,ip,port):
        """��ʼ������"""
        # ����SSL������               # ָ��ssl�汾
        self.context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        # �������θ�֤��                       ע��ؼ��ִ��Σ�������
        self.context.load_cert_chain(certfile="cert/ca.crt", keyfile="cert/ca.key")
        # self.context.load_verify_locations('cert.pem')  # server�˵�֤��
        # self.context.load_verify_locations('key.pem')  # server�˵�
        print("����֤��ɶ�Ķ����������")
        # �����׽���
        print(self.context)
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # �������˿�ռ������
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # �󶨱���ip��ַ
        self.tcp_server_socket.bind((ip, port))
        # ���׽��ֱ�Ϊ�����׽��֣������������Ϊ100
        self.tcp_server_socket.listen(100)
        print("�����������100��")

    # �������Ҫ���������������߳�
    def run_forever(self):
        """�豸����"""
        print("�ȴ��豸������ing������")
        print("�ȴ������µ��׽��֡�����")

        with self.context.wrap_socket(self.tcp_server_socket, server_side=True) as ssock:
            while 1:
                # �ȴ��豸�����ӣ���ȡ���Ӻ���׽���new_socket
                new_socket, client_addr = ssock.accept()
                print("�豸{0}������".format(client_addr))

                # 2.�����̴߳����豸������            �̴߳���ĺ���           ��Ҫ�Ĳ���
                t1 = threading.Thread(target=self.service_machine, args=(new_socket, client_addr))
                t1.start()

    # ҵ�������Ҫ����
    def service_machine(self, new_socket, client_addr):
        """ҵ����"""
        while 1:
            # 3.�����豸���͵����ݣ��������1024�ֽڣ�����gbk����ʽ����
            receive_data = new_socket.recv(1024).decode("utf-8")
            # 4.����豸���͵����ݲ�Ϊ��
            if receive_data:
                # 4.1 ��ӡ���յ����ݣ�������Խ��豸���͵�����д�뵽�ļ���
                # ��ȡ�豸��ID��Ϣ
                print(receive_data)
                if receive_data[0:6] == "report":
                    response = "SET OK:" + receive_data
                else:
                    receive_data = receive_data[6:].split(",")[0]
                    # ƴ����Ӧ����
                    response = "alarm=" + receive_data + ",Switch:clear"
                print(response)
                # 4.2 ����ԭ������ΪӦ�𣬰���utf-8����ʽ����
                new_socket.send(response.encode("utf-8"))
            # 5.���豸�Ͽ�����ʱ�����յ��յ��ֽ����ݣ��ж��豸�ѶϿ�����
            else:
                print('�豸{0}�Ͽ�����...'.format(client_addr))
                break

        # �ر��׽���
        new_socket.close()


# ��ִ���ļ�
def main(ip,port):
    """����һ��WEB������"""
    wsgi_server = WSGIServer(ip,port)
    print("�������ѿ���")
    wsgi_server.run_forever()

# ����ִ�еĿ�ʼ ָ��ip��port
if __name__ == '__main__':
    ip = '127.0.0.1'
    port = 8005
    main(ip,port)
