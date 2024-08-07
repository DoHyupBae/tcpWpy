import socket
import random
import time
from datetime import datetime

# 본사 서버 정보
SERVER_HOST = '192.168.0.125'
SERVER_PORT = 8080


def generate_data():
    """데이터 랜덤 생성하는 부분, 현장에서 측정한 데이터로 간주"""
    flow = round(random.uniform(0, 100), 2)
    impuritiesA = round(random.uniform(0, 10), 2)
    impuritiesB = round(random.uniform(0, 10), 2)
    time_str = datetime.now().isoformat()
    return flow, impuritiesA, impuritiesB, time_str


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print("서버 연결 완료.")

        try:
            while True:
                flow, impuritiesA, impuritiesB, time_str = generate_data()
                data = f"{flow},{impuritiesA},{impuritiesB},{time_str}"
                client_socket.sendall(data.encode())
                print(f"데이터 전송 완료 : {data}")
                time.sleep(1)  # Send data every second
        except KeyboardInterrupt:
            print("현장 시스템 정지.")


if __name__ == '__main__':
    main()
