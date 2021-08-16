import socket
import re
import asyncio
import time

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 50000        # Port to listen on (non-privileged ports are > 1023)

class TransmissionError(Exception):
    pass

class SocketBrokenError(Exception):
    pass


class MySocket:
    def __init__(self, name, host, port, chunk_size = 1024):
        self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        self.name = name    
        self.chunk_size = chunk_size
        self.host =''
        self.port =''
        self.retry_counter = 0
        self.retry_max=3
        self.con_to_reader_retry_cnt = 0
        self.con_to_reader_retry_lim = 100
        self.send_delimiter = b'END'
        self.rsvd_ok_msg = b'rsvdOK'
        self.bind(host, port)
        self.connected = False
        self.conn=''
        

    def bind(self, host, port):
        self.sock.bind((host, port))
        self.host = host
        self.port = port
        print(self.name+ f" bind at host {self.host} and port {self.port}")

    def listen(self):
        self.listen()

    def set_connection_with_sender(self):
        self.listen()
        self.conn, self.addr = self.sock.accept()
        #print(self.name+ f" connected with sender at {self.addr}")
        return True

    def connect_with_reader(self, host, port):
        try:
            self.sock.connect((host, port))
            self.connected = True
        except ConnectionRefusedError:
            if self.con_to_reader_retry_cnt <= self.con_to_reader_retry_lim:
                time.sleep(1)
                self.connect_with_reader(host, port)
                self.con_to_reader_retry_cnt+=1
            
        
    def listen(self):
        self.sock.listen(1)
        return True
    
    def send(self, msg):
            sent = self.sock.sendall(msg)
            if sent == 0:
                raise RuntimeError("socket connection broken")
            self.sock.send(self.send_delimiter)
            try:
                response = self.sock.recv(self.chunk_size)
                if response  != self.rsvd_ok_msg:
                    raise TransmissionError
                return 0
            except TransmissionError:
                self.retry_counter+=1
                if self.retry_counter<=self.retry_max:
                    self.send(msg)
                else:
                    return 1
        
        
            return None    

    def receive(self):
        chunks = []
        bytes_recd = 0
        chunk=b''
        try:
            while True:
                chunk = self.conn.recv(self.chunk_size)
                if chunk == b'':
                    raise SocketBrokenError
                elif chunk[-3:] == self.send_delimiter:
                    chunk = chunk[:-len(self.send_delimiter)]
                    chunks.append(chunk)
                    break
                chunks.append(chunk)
            self.conn.send(self.rsvd_ok_msg)
            return b''.join(chunks)
        except SocketBrokenError:
            return None
        except ConnectionResetError:
            return None

    def close(self):
        self.sock.close()
        if self.conn!='':
            self.conn.close()
            print("Close incoming ")
        
