import time
from termcolor import colored

def send(socket, message, TARGET_HOST, TARGET_READER_PORT):
    if socket.connected != True:
        socket.connect_with_reader(TARGET_HOST, TARGET_READER_PORT)
    result = socket.send(message)
    if result == 0:
        print(f"Send: {str(message)}")
        time.sleep(1)
    else:
        pass
    return result    

def receive(socket, TARGET_HOST, TARGET_READER_PORT, queue):
    if socket.conn =='':
        socket.set_connection_with_sender()
    while True:
        res = socket.receive();
        print("Received: ",str(res))
        if res == b'Stop conversation': 
            queue.put(b'Stop conversation')
            return res
        elif res!=None:
            queue.put(res)
            time.sleep(1)
        else:
            return res
    

message_dict = {
    b'Hello!': b'Hi!',
    b'Hi!': b'How are you doing?', 
    b'How are you doing?': b'Fine, thank You!',
    b'Fine, thank You!': b'Do you have some ideas about home work?',
    b'Do you have some ideas about home work?':
        b'No I just take a days off and going to spent them lazy',
    b'No I just take a days off and going to spent them lazy':b'Good by',
    b'Good by':b'See you!',
    b'See you!':b'Stop conversation', 
    }


def bot_send_messages(socket, TARGET_HOST, TARGET_READER_PORT, message_dict, queue):
    values = list(message_dict.values())
    keys = list(message_dict.keys())              

    while True:
        if queue.empty():
           continue
        else:
            income_message =  queue.get()
            if income_message == b'Start conversation':
               outgoing_msg = keys[0]
            elif income_message in keys:
               outgoing_msg =  message_dict[income_message]
            elif income_message == b'Stop conversation':
               print("Communication channel was closed by remote peer")
               send(socket,income_message, TARGET_HOST, TARGET_READER_PORT)
               return 0
            else:
              continue
        result = send(socket,outgoing_msg, TARGET_HOST, TARGET_READER_PORT)
        if result == 1 or outgoing_msg == b'Stop conversation':
           return None
    return None

def bot_get_messages(socket, TARGET_HOST, TARGET_SENDER_PORT, queue):
    res = 0
    while res not in [None, b'Stop conversation', b'See you!']:
           res = receive(socket, TARGET_HOST, TARGET_SENDER_PORT, queue)

