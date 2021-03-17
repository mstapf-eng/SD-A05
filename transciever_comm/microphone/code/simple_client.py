import logging
from time import sleep
import numpy as np
from numpysocket import NumpySocket
import npy_arr_rec as rec

logger = logging.getLogger('simple client')
logger.setLevel(logging.INFO)

host_ip = 'Megans-MacBook-Pro.local'  # change me

npSocket = NumpySocket()
while(True):
    try:
        npSocket.startClient(host_ip, 9999)
        break
    except:
        logger.warning("connection failed, make sure `server` is running.")
        sleep(1)
        continue

logger.info("connected to server")

frame = np.arange(1000)
data = rec.record(3)
logger.info("sending numpy array:")
logger.info(data)
npSocket.send(data)

logger.info("array sent, closing connection")
try:
    npSocket.close()
except OSError as err:
    logging.error("client already disconnected")
