import socket
from xml.etree.ElementInclude import DEFAULT_MAX_INCLUSION_DEPTH
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

HOST = "127.0.0.1"  # The server's hostname or IP address. This needs to be constantly updated
PORT =  8324 # The port used by the server
address = (HOST, PORT)

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect(address)
        s.sendall(b"Hello, world")
        beginning_buffer = b""
        while True:
            bytes_in = b""
            while True:
                data = s.recv(1024)
                print(type(data[0]))
                bytes_in = bytes_in+data
                # print(type(image))
                # print(type(image[-1]))
                # If end
                if b'ThisIsAnEndToken' in bytes_in:
                    bytes_in = bytes_in.replace(b'ThisIsAnEndToken', b'')
                    break

            print("recieved bytes of", len(bytes_in), type(bytes_in))
            # image = bytes(image)
            # image = list(image)
            # print(len(image))
            # print(type(image))

            np_jpeg = np.frombuffer(bytes_in, dtype='uint8')
            print('got jpg image of len', len(np_jpeg))
            img_rec = cv.imdecode(np_jpeg, cv.IMREAD_GRAYSCALE)
            print('got image of shape', img_rec.shape)
            # plt.imshow(img_rec)
            # plt.show()


            # numpy_image = np.array(bytes_in)
            # print(type(numpy_image))
            # # numpy_image = numpy_image.reshape(720,1280)
            # actual_image = cv.imdecode(numpy_image, cv.IMREAD_UNCHANGED)
            # print(type(actual_image))
            cv.imshow("frame", img_rec)
            print("finished showing fraem!")
            if cv.waitKey(1) == ord('q'):
                break


        print(data)
        # cv.imshow("frame", data)
        # if cv.waitKey(1) == ord('q'):y
        #     break



