import numpy as np
import socket
import asyncio
from matplotlib import pyplot as plt
from time import sleep
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, LoggingEventHandler
import logging

HOST = "NUS15128-11-albhuan.local" # Needs to be constantly updated except 127.0.0.1 which is auto local host
PATH = 'image_stream.jpg'
PORT = 8324

address = (HOST,PORT)
## CAST OPENCV image to byte array
## add some byte at the beginning/end that you can look for
## use opencv from byte array to image


class EventHandler(FileSystemEventHandler):
    def __init__(self, obs):
        self.observer = obs
        self.image = b''

    def on_modified(self, event):
        if not event.src_path.endswith(PATH):
            return

        with open(event.src_path, 'rb') as img:
            data_byte = img.read()

        if len(data_byte) < 2e5:   # TODO: filtering for incomplete writes is jank
            return

        self.image = data_byte

    def send_image(self):
        """Raises BrokenPipeError if client has disconnected, and ValueError if there is no image to send."""
        if len(self.image) == 0: raise ValueError("no image to send")

        data_byte = self.image

        print("sending image of", len(data_byte), type(data_byte))
        data_byte = data_byte + b'ThisIsAnEndToken'

        conn.sendall(data_byte)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind(address)
    s.listen()
    while True:
        print("waiting for client...")
        conn, addr = s.accept()
        #### With connection
        with conn:
            print(f"Connected by {addr}")
            observer = Observer()
            handler = EventHandler(observer)
            observer.schedule(handler, '.')
            observer.start()

            try:
                while True:
                    try:
                        handler.send_image()
                    except ValueError:
                        print("no image to send!")
                        continue
                    sleep(0.05)
            except BrokenPipeError:
                print("client disconnected")
                observer.stop()
                observer.join()
            except ConnectionResetError:
                print("client disconnected")
                observer.stop()
                observer.join()


cap.release()
cv.destroyAllWindows()



