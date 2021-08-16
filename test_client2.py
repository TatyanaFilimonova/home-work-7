#'remote' copy of messenger

import socket
from classes import *
import asyncio
from body_client import *
from multiprocessing import Pool, Queue, Process

TARGET_HOST = '127.0.0.1'  
TARGET_READER_PORT = 5605
TARGET_SENDER_PORT = 5606

MY_HOST = '127.0.0.1'  
READER_PORT = 5603
SENDER_PORT = 5604

def main():
    futures = []
    queue = Queue()  
    socket_reader = MySocket('READER_SOCKET_CLIENT2', MY_HOST, READER_PORT)
    socket_sender = MySocket('SENDER_SOCKET_CLIENT2', MY_HOST, SENDER_PORT)
    sender_process = Process(target=bot_get_messages, args =(socket_reader,
                            TARGET_HOST, TARGET_SENDER_PORT, queue))
    reader_process = Process(target= bot_send_messages, args =(socket_sender, 
                            TARGET_HOST, TARGET_READER_PORT,
                                       message_dict, queue))
    sender_process.start()
    reader_process.start()
    sender_process.join()
    reader_process.join()
    socket_reader.close()
    socket_sender.close()
    print('All sockets are closed')
              
if __name__ == '__main__':
   main()
