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
    def __init__(self, obs):
        self.observer = obs

    def on_modified(self, event):
        print("event modified", event.src_path)
        # TODO: read image from file

        if not event.src_path.endswith(PATH):
            return

        with open(event.src_path, 'rb') as img:
            data_byte = img.read()


        # data_byte = data_byte.tobytes()

        print("sending image of", len(data_byte), type(data_byte))
        data_byte = data_byte + b'ThisIsAnEndToken'

        try:
            conn.sendall(data_byte)
            # input('sent an image!')
            # sleep(1/FRAMERATE)
        except BrokenPipeError:
            # TODO: how to hnadle broken pipe
            self.observer.stop()
            self.observer.join()
            print("pipe broken ... did the client disconnect?")
            raise NotImplementedError("don't know how to handle a broken pipe")



observer = Observer()
handler = EventHandler(observer)


# logging.basicConfig(level=logging.INFO,
#                     format='%(asctime)s - %(message)s',
#                     datefmt='%Y-%m-%d %H:%M:%S')


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(address)
    s.listen()
    while True:
        conn, addr = s.accept()
        #### With connection
        with conn:
            print(f"Connected by {addr}")
            observer.schedule(handler, '.')
            observer.start()

            try:
                while True:
                    sleep(0.05)
            finally:
                observer.stop()
                observer.join()


cap.release()
cv.destroyAllWindows()



