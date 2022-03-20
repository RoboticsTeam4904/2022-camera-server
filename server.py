import numpy as np
import socket
import asyncio
from matplotlib import pyplot as plt
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import logging

HOST = "127.0.0.1" # Needs to be constantly updated except 127.0.0.1 which is auto local host
PATH = 'image_stream.jpg'
PORT = 8324

address = (HOST,PORT)
## CAST OPENCV image to byte array
## add some byte at the beginning/end that you can look for
## use opencv from byte array to image

class EventHandler(FileSystemEventHandler):
    def on_moved(event):
        print(event)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# handler = EventHandler()
handler = LoggingEventHandler()

observer = Observer()
observer.schedule(handler, '.')
observer.start()

try:
    while True:
        sleep(0.1)
finally:
    observer.stop()
    observer.join()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(address)
        s.listen()
        while True:
            conn, addr = s.accept()
            #### With connection
            with conn:
                print(f"Connected by {addr}")
                while True:
                    ### Data undergoes transformations from numpy array to bytes

                    # ret, frame = cap.read()
                    # if not ret:
                    #     print("something died i guess")
                    #     break


                    # print(cv.imencode(".jpg",data))
                    # print(data_byte.shape, type(data_byte))
                    data_byte = data_byte.tobytes()

                    print("sending image of", len(data_byte), type(data_byte))
                    data_byte = data_byte + b'ThisIsAnEndToken'
                    try:
                        conn.sendall(data_byte)
                        # input('sent an image!')
                        sleep(1/FRAMERATE)
                    except BrokenPipeError:
                        print("pipe broken ... did the client disconnect?")
                        break


                # if not data.all():
                #     print("hi data stopped coming")
                #     break


        # s.listen()
        # conn, addr = s.accept()
        # with conn:
        #     print(f"Connected by {addr}")
        #     while True:
        #         data = conn.recv(1024)
        #         if not data:
        #             break
        #         conn.sendall(data)
    # print(f"Received {data!r}")

    # cv.imshow("frame", gray)
    # if cv.waitKey(1) == ord('q'):
    #     break

cap.release()
cv.destroyAllWindows()



