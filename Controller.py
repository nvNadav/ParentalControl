import math
import socket
import threading
import time
import numpy as np
import keyboard
import numpy as np
import cv2
import struct
import io

from pynput import mouse
from PIL import Image
from enum import Enum

import prot

keyboard_port = 60123
mouse_port = 60124
screen_port = 60125

class Action(str, Enum):
    keyboard = "keyboard"
    screen = "screen"
    mouse = "mouse"

def create_socket(port,*, host='0.0.0.0', family=socket.AF_INET, sock_type=socket.SOCK_STREAM):
    serv = socket.socket(family,sock_type)
    serv.bind((host, port))
    # if sock_type==socket.SOCK_DGRAM:
    #     print(f"Server is waiting for connection in port {port}")
    #     data, cli_addr = serv.recvfrom(1024)
    #     serv.connect(cli_addr)
    #     print(f"Server is connected with {cli_addr}")
    #     return serv
    
    serv.listen(1)
    print(f"Server is waiting for connection in port {port}")
    cli_sock, cli_addr = serv.accept()
    print(f"Server is connected with {cli_addr}")
    return serv,cli_sock,cli_addr

def send_message(action,message,socket):
    socket.send(prot.create_msg_with_header(f"{action} {message}").encode())

# -----------------------------
# keyboard section
# -----------------------------
def new_key(event,sock):
    if event.event_type == 'down':
        send_message(Action.keyboard,event.name,sock)
        #sock.send(prot.create_msg_with_header(event.name).encode())
    
def keyboard_actions(socket):
    try:           
        #serv,keyboard_socket,cli_addr=create_socket(keyboard_port)

        keyboard.hook(lambda e: new_key(e, socket))
        keyboard.wait('shift+esc')
        stop_all.set()
        #keyboard_socket.send(prot.create_msg_with_header("EXIT").encode())
    except Exception as error:
        print (str(error))
    finally:
        # keyboard_socket.close()
        # serv.close()
        keyboard.unhook_all()
        print ("keyboard closed...")
# -----------------------------
# mouse section
# -----------------------------

# Throttling variables
last_move_time = 0
last_position = (None, None)
move_interval = 0.05  
position_threshold = 3  # Only send if moved at least 3 pixels

def on_move(x, y,sock):
    if stop_all.is_set():
        return False
    global last_move_time, last_position
    
    current_time = time.time()
    
    # Time-based throttling
    if current_time - last_move_time < move_interval:
        return
    
    # Position-based throttling
    last_x, last_y = last_position
    if last_x is not None and last_y is not None:
        # Calculate distance moved
        distance = math.sqrt((x - last_x) ** 2 + (y - last_y) ** 2)
        if distance < position_threshold:
            return
    
    # Update tracking variables
    last_move_time = current_time
    last_position = (x, y)

    # Send the coordinates
    send_message(Action.mouse,f"MOVE {x} {y}",sock)
    #sock.send(prot.create_msg_with_header(f"MOVE {x} {y}").encode())

def on_click(x, y, button, pressed,sock):
    if stop_all.is_set():
        return False
    if pressed:
        send_message(Action.mouse,f"PRESS {button.name}",sock)
        #sock.send(prot.create_msg_with_header(f"PRESS {button.name}").encode())
    else:
        send_message(Action.mouse,f"RELEASE {button.name}",sock)
        #sock.send(prot.create_msg_with_header(f"RELEASE {button.name}").encode())

def on_scroll(x, y, dx, dy,sock):
    if stop_all.is_set():
        return False
    send_message(Action.mouse,f"SCROLL {dx} {dy}",sock)
    #sock.send(prot.create_msg_with_header(f"SCROLL {dx} {dy}").encode())


def mouse_actions(socket):
    try:
        #serv,mouse_socket,cli_addr=create_socket(mouse_port)

        with mouse.Listener(on_move=lambda x,y: on_move(x,y,socket),
                            on_click=lambda x,y,button,pressed:on_click(x,y,button,pressed,socket),
                            on_scroll=lambda x,y,dx,dy:on_scroll(x,y,dx,dy,socket)) as listener: 
            listener.join()
        #socket.send(prot.create_msg_with_header("EXIT").encode())
    except Exception as error:
        print (str(error))
    finally:
        # mouse_socket.close()
        # serv.close()
        print ("Mouse closed...")

# -----------------------------
# screen section
# -----------------------------
def receive_screenshot():
    try:
        screen_socket=create_socket(screen_port,sock_type=socket.SOCK_DGRAM)
        
        while True:
            if stop_all.is_set():
                return
            chunks = {}
            total_chunks = None
            while True:
                data = screen_socket.recv(2048)
                index, total = struct.unpack("!HH", data[:4])
                chunk_data = data[4:]

                chunks[index] = chunk_data
                total_chunks = total

                if len(chunks) == total_chunks:
                    break

            img_bytes = b''.join(chunks[i] for i in range(total_chunks))
            display_image(img_bytes)
    except Exception as error:
        print (str(error))

def display_image(img_bytes):
    try:
        # Convert bytes to numpy array
        nparr = np.frombuffer(img_bytes, np.uint8)
        # Decode image
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        
        # Display
        cv2.imshow('Screenshot Stream', img)
        cv2.waitKey(1)  # 1ms delay

    except Exception as error:
        print (str(error))



dic={"keyboard":keyboard_actions,"mouse":mouse_actions,"screen":receive_screenshot}
def start_remote_controll():
    serv,socket,cli_addr=create_socket(60123)
    dic[threading.current_thread().name](socket)


    socket.send(prot.create_msg_with_header("EXIT").encode())
    serv.close()
    socket.close()




stop_all = threading.Event()

keyboard_thread=threading.Thread(target=start_remote_controll,name="keyboard")
keyboard_thread.start()

mouse_thread=threading.Thread(target=start_remote_controll,name="mouse")
mouse_thread.start()


# screen_thread=threading.Thread(target=start_remote_controll,name="screen")
# screen_thread.start()

# screen_thread.join()
mouse_thread.join()
keyboard_thread.join()