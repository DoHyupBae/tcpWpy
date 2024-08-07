import socket
import psycopg2

# PostgreSQL DB 정보
DATABASE = 'waterCondition'  
USER = 'postgres'  #
PASSWORD = 'ecobdh0609'  
HOST_DB = 'localhost'  
PORT_DB = 5432  

# TCP 서버 정보, 현장 송신장비 IP 특정 가능함
HOST = '0.0.0.0'  # 연결 시도하는 모든 시스템에서 데이터 수신 가능
PORT = 8080


def connect_to_database():
    """PostgreSQL DB와 연결"""
    try:
        conn = psycopg2.connect(
            dbname=DATABASE,
            user=USER,
            password=PASSWORD,
            host=HOST_DB,
            port=PORT_DB
        )
        cursor = conn.cursor()
        print("DB 연결 성공")
        return conn, cursor
    except Exception as e:
        print(f"에러 발생 : {e}")
        return None, None


def insert_data(cursor, flow, impurities1, impurities2, time_str):
    """DB의 realtime 테이블에 전송받은 데이터 입력"""
    insert_query = """
    INSERT INTO realtime (flow, impurities1, impurities2, time)
    VALUES ( %s, %s, %s, %s);
    """
    try:
        cursor.execute(insert_query, (flow, impurities1, impurities2, time_str))
        cursor.connection.commit()
        print("데이터 입력 완료.")
    except Exception as e:
        print(f"데이터 입력 오류 : {e}")
        cursor.connection.rollback()


def handle_client(client_socket, cursor):
    """TCP 연결 및 데이터 수신 관리"""
    try:
        while True:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            print(f"Received: {data}")
            flow, impurities1, impurities2, time_str = data.split(',')
            insert_data(cursor, float(flow), float(impurities1), float(impurities2), time_str)
    except Exception as e:
        print(f"Error handling client: {e}")
    finally:
        client_socket.close()


def start_server():
    """서버 시작"""
    conn, cursor = connect_to_database()
    if cursor:

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((HOST, PORT))
            server_socket.listen()
            print(f"수신 대기중 {HOST}:{PORT}")

            while True:
                client_socket, addr = server_socket.accept()
                print(f"현장 접속 성공 : {addr}")
                handle_client(client_socket, cursor)

        # DB 연결 종료
        cursor.close()
        conn.close()


def main():
    start_server()


if __name__ == '__main__':
    main()